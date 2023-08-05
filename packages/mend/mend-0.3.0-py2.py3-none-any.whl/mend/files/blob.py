from dataclasses import dataclass
from pathlib import Path
from typing import BinaryIO, Optional, Type

from mend.protocols import Blob, Tree


@dataclass(frozen=True)
class FileBlob(Blob):
    data: BinaryIO
    name: str

    def close(self) -> None:
        self.data.close()

    def as_tree(self) -> Tree:
        return {
            self.name: self.data,
        }

    @classmethod
    def open(
            cls: Type["FileBlob"],
            path: Path,
            name: Optional[str] = None,
    ) -> "FileBlob":
        return cls(
            data=open(path, "rb"),
            name=name or str(path),
        )
