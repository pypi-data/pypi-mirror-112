from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Type

from click import (
    Argument,
    Parameter,
    Path as PathType,
    echo,
)

from mend.protocols import Plugin, Tree


@dataclass(frozen=True)
class CopyPlugin(Plugin):
    directory: Path

    def apply(self, tree: Tree) -> None:
        for path, blob in tree.blobs.items():
            destination = self.directory / path.name
            echo(f"Copying data to: {destination}")

            destination.parent.mkdir(parents=True, exist_ok=True)

            with open(destination, "wb") as fileobj:
                fileobj.write(blob.read())

    @classmethod
    def iter_parameters(cls: Type["CopyPlugin"]) -> Iterable[Parameter]:
        yield Argument(
            [
                "directory",
            ],
            required=True,
            type=PathType(
                allow_dash=False,
                dir_okay=True,
                exists=False,
                file_okay=False,
                path_type=Path,
                readable=True,
                resolve_path=True,
                writable=True,
            ),
        )

    @classmethod
    def from_parameters(
            cls: Type["CopyPlugin"],
            *args,
            **kwargs,
    ) -> "CopyPlugin":
        directory = kwargs["directory"]

        return cls(
            directory=directory,
        )
