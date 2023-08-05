from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Type

from click import Option, Parameter, Path as PathType

from mend.protocols import Plugin, Tree


@dataclass(frozen=True)
class CopyPlugin(Plugin):
    path: Path

    def apply(self, tree: Tree) -> None:
        for name, blob in tree.items():
            path = self.path / name
            path.parent.mkdir(parents=True, exist_ok=True)

            with open(path, "wb") as fileobj:
                fileobj.write(blob.read())

    @classmethod
    def iter_parameters(cls: Type["CopyPlugin"]) -> Iterable[Parameter]:
        yield Option(
            [
                "--path",
            ],
            required=True,
            type=PathType(
                allow_dash=False,
                dir_okay=True,
                exists=True,
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
        path = kwargs["path"]

        return cls(
            path=path,
        )
