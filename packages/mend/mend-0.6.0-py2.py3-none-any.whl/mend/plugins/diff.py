from dataclasses import dataclass
from difflib import unified_diff
from pathlib import Path
from typing import (
    Iterable,
    Optional,
    Tuple,
    Type,
)

from click import (
    Argument,
    Parameter,
    Path as PathType,
    echo,
    style,
)

from mend.files import FileBlob
from mend.protocols import Blob, Plugin, Tree


@dataclass(frozen=True)
class DiffPlugin(Plugin):
    """
    Calculate difference between generated source and path.

    """
    blob: FileBlob

    def close(self) -> None:
        self.blob.close()

    def apply(self, right_tree: Tree) -> None:
        """
        Compute a diff over files in the local and generated trees.

        """
        left_tree = self.blob.as_tree()

        for path, left, right in self.iter_blobs(left_tree, right_tree):
            for item in self.diff(path, left, right):
                echo(item.strip("\n"))

    def iter_blobs(self, left_tree: Tree, right_tree: Tree) -> Iterable[Tuple[str, Optional[Blob], Optional[Blob]]]:
        left: Optional[Blob]
        right: Optional[Blob]

        if len(right_tree.blobs) == 1 and len(left_tree.blobs) == 1:
            # special case for single file comparison
            left = next(iter(left_tree.blobs.values()))
            right = next(iter(right_tree.blobs.values()))

            yield "file", left, right
        else:
            # directory comparison
            paths = left_tree.blobs.keys() | right_tree.blobs.keys()

            for path in paths:
                left = left_tree.blobs.get(path)
                right = right_tree.blobs.get(path)

                yield str(path), left, right

    def diff(self, path: str, left: Optional[Blob], right: Optional[Blob]) -> Iterable[str]:
        """
        Produce a single file diff, assuming text data.

        """
        left_lines = left.read().decode("utf-8").splitlines() if left else []
        right_lines = right.read().decode("utf-8").splitlines() if right else []
        left_name = f"{path} - original"
        right_name = f"{path} - generated"

        lines = unified_diff(left_lines, right_lines, left_name, right_name, lineterm="")

        for line in lines:
            if line.startswith("+"):
                yield style(line, fg="green")
            elif line.startswith("-"):
                yield style(line, fg="red")
            elif line.startswith("@"):
                yield style(line, fg="blue")
            else:
                yield line

    @classmethod
    def iter_parameters(cls: Type["DiffPlugin"]) -> Iterable[Parameter]:
        yield Argument(
            [
                "path",
            ],
            required=True,
            type=PathType(
                allow_dash=False,
                # TODO: support directories
                dir_okay=False,
                exists=True,
                file_okay=True,
                path_type=Path,
                readable=True,
                resolve_path=True,
                writable=False,
            ),
        )

    @classmethod
    def from_parameters(
            cls: Type["DiffPlugin"],
            *args,
            **kwargs,
    ) -> "DiffPlugin":
        path = kwargs["path"]

        return cls(
            blob=FileBlob.open(
                path=path,
            ),
        )
