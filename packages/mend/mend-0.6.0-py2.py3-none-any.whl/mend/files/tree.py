from dataclasses import dataclass
from pathlib import Path

from mend.protocols import Blob, Tree


@dataclass(frozen=True)
class FileTree(Tree):
    blobs: dict[Path, Blob]
