from dataclasses import dataclass
from pathlib import Path
from typing import BinaryIO, Type

from mend.files.tree import FileTree
from mend.protocols import Blob, Tree


@dataclass(frozen=True)
class FileBlob(Blob):
    data: BinaryIO
    path: Path

    def close(self) -> None:
        self.data.close()

    def as_tree(self) -> Tree:
        return FileTree({
            self.path: self.data,
        })

    @classmethod
    def open(
            cls: Type["FileBlob"],
            path: Path,
    ) -> "FileBlob":
        return cls(
            data=open(path, "rb"),
            path=path,
        )
