from dataclasses import dataclass
from difflib import unified_diff
from pathlib import Path
from typing import Iterable, Optional, Type

from click import (
    Option,
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

        names = left_tree.keys() | right_tree.keys()

        for name in names:
            left = left_tree.get(name)
            right = right_tree.get(name)

            for item in self.diff(name, left, right):
                echo(item.strip("\n"))

    def diff(self, name: str, left: Optional[Blob], right: Optional[Blob]) -> Iterable[str]:
        """
        Produce a single file diff, assuming text data.

        """
        left_lines = left.read().decode("utf-8").splitlines() if left else []
        right_lines = right.read().decode("utf-8").splitlines() if right else []
        left_name = f"{name} - original"
        right_name = f"{name} - generated"

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
        yield Option(
            [
                "--path",
            ],
            required=True,
            type=PathType(
                allow_dash=False,
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
                name="file",
            ),
        )
