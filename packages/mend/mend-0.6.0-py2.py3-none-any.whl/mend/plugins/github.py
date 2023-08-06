from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Type

from click import (
    BadParameter,
    Option,
    Parameter,
    echo,
)
from github import Github
from github.Branch import Branch
from github.GitCommit import GitCommit
from github.GithubException import GithubException
from github.InputGitTreeElement import InputGitTreeElement
from github.PullRequest import PullRequest
from github.Repository import Repository

from mend.protocols import Plugin, Tree


# See: https://git-scm.com/book/en/v2/Git-Internals-Git-Objects
NORMAL_FILE_MODE = "100644"


def normalize_path(path: Path) -> str:
    return str(path.relative_to(Path.cwd()))


@dataclass(frozen=True)
class GitHubPlugin(Plugin):
    """
    Create a GitHub pull request.

    """
    repository: Repository
    base_branch: str
    target_branch: str
    title: str

    def apply(self, tree: Tree) -> None:
        """
        Create a pull request, apply the generated tree.

        """
        branch = self.create_branch()
        self.create_commit(branch, tree)
        pull_request = self.create_pull_request()

        echo(f"Created pull request: {pull_request.number}")

    def create_branch(self) -> Branch:
        """
        Create a remote branch.

        """
        echo(f"Creating branch: {self.target_branch} off of {self.base_branch}.")

        base_branch = self.repository.get_branch(self.base_branch)
        try:
            self.repository.create_git_ref(
                ref=f"refs/heads/{self.target_branch}",
                sha=base_branch.commit.sha,
            )
        except GithubException as error:
            if error.status == 404:
                raise Exception(
                    f"Unable to create branch {self.target_branch}; please confirm that your "
                    "access token has write access to this repository."
                )

            if error.status != 422:
                raise

            # Branch should exist already, pass through to make sure
            pass

        git_branch = self.repository.get_branch(self.target_branch)

        echo(f"Created branch: {self.target_branch}.")

        return git_branch

    def create_commit(self, branch: Branch, tree: Tree) -> GitCommit:
        echo(f"Finding base tree for {branch.name}.")

        base_tree = self.repository.get_git_tree(branch.commit.sha)

        echo(f"Creating {len(tree.blobs)} git blob(s).")

        git_blobs = {
            path: self.repository.create_git_blob(
                content=blob.read().decode("utf-8"),
                encoding="utf-8",
            )
            for path, blob in tree.blobs.items()
        }

        echo("Creating a new git tree from blob(s).")

        git_tree = self.repository.create_git_tree(
            tree=[
                InputGitTreeElement(
                    path=normalize_path(path),
                    mode=NORMAL_FILE_MODE,
                    type="blob",
                    sha=blob.sha,
                )
                for path, blob in git_blobs.items()
            ],
            base_tree=base_tree,
        )

        echo(f"Creating git commit from tree: {git_tree.sha}.")

        git_commit = self.repository.create_git_commit(
            message=(
                f"""mend: applying changes to ${len(tree.blobs)} files

                Includes:
                """
                "\n".join(
                    f" - {path}"
                    for path in sorted(tree.blobs.keys())
                )
            ),
            tree=git_tree,
            parents=[
                branch.commit.commit,
            ],
        )

        echo(f"Updating git ref {self.target_branch} to: {git_commit.sha}")

        git_ref = self.repository.get_git_ref(f"heads/{self.target_branch}")
        git_ref.edit(git_commit.sha)

        return git_commit

    def create_pull_request(self) -> PullRequest:
        echo(f"Creating pull request from {self.target_branch} onto {self.base_branch}.")

        try:
            # create a PR of the release branch into head
            return self.repository.create_pull(
                title=self.title,
                body=f"Merge mend changes into {self.base_branch}.",
                base=self.base_branch,
                head=self.target_branch,
            )
        except GithubException as error:
            if error.status != 422:
                raise

            if any((
                "No commits between" in error.get("message", "")
                for error in error.data.get("errors", ())
                if isinstance(error, dict)
            )):
                # NB: maybe we should delete the branch here?
                raise Exception("Skipping pull request; no changes.")

            # PR should exist already; make sure
            pull_requests = self.repository.get_pulls(
                base=self.base_branch,
                head=self.target_branch,
            )

            if not pull_requests:
                raise

            return pull_requests[0]

    @classmethod
    def iter_parameters(cls: Type["GitHubPlugin"]) -> Iterable[Parameter]:
        yield Option(
            [
                "--token",
                "--github-token",
            ],
            envvar="GITHUB_TOKEN",
            help=(
                "A GitHub API access token, either provided via the GITHUB_TOKEN "
                "environment variable or via a CLI prompt."
            ),
            hide_input=True,
            prompt=True,
            required=True,
        )
        yield Option(
            [
                "--organization",
                "--org",
                "-o",
            ],
            help=(
                "The name of the target Github organization name, which may be "
                "omitted if the repository name is fully-qualified."
            ),
            required=False,
        )
        yield Option(
            [
                "--repository",
                "--repo",
                "-r",
            ],
            help=(
                "The name of the target Github repository name."
            ),
            required=True,
        )
        yield Option(
            [
                "--branch",
                "--branch-name",
                "-b",
            ],
            help="The name of the branch to create",
            required=True,
        )
        yield Option(
            [
                "--branch-prefix",
            ],
            help="The prefix to apply to the branch",
            default="mend"
        )
        yield Option(
            [
                "--base",
                "--base-branch",
            ],
            help="The name of the base branch to use; uses the default branch if omitted",
        )
        yield Option(
            [
                "--title",
            ],
            help="The pull request title",
        )

    @classmethod
    def from_parameters(
            cls: Type["GitHubPlugin"],
            *args,
            **kwargs,
    ) -> "GitHubPlugin":
        github_token = kwargs["token"]
        organization_name = kwargs["organization"]
        repository_name = kwargs["repository"]
        branch_name = kwargs["branch"]
        branch_prefix = kwargs["branch_prefix"]
        base_branch = kwargs["base"]
        title = kwargs["title"]

        if organization_name is None:
            if "/" not in repository_name:
                raise BadParameter(
                    message="Expected 'organization/repository' when --organization is omitted.",
                    param_hint="repository",
                )
        else:
            repository_name = f"{organization_name}/{repository_name}"

        github = Github(github_token)
        repository = github.get_repo(repository_name)

        return cls(
            repository=repository,
            base_branch=base_branch or repository.default_branch,
            target_branch=f"{branch_prefix}/{branch_name}" if branch_prefix else branch_name,
            title=title or f"Mend {branch_name}",
        )
