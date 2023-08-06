from pathlib import Path
from typing import Protocol

from mend.protocols.blob import Blob


class Tree(Protocol):
    """
    A tree represents a collection of Blob indexed by Path.

    """
    blobs: dict[Path, Blob]

    def close(self) -> None:
        """
        A blob may be closed.

        """
        for blob in self.blobs.values():
            blob.close()
