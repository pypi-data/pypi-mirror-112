from typing import Protocol


class Blob(Protocol):
    """
    A blob represents something that can be saved as a git blob (e.g. a file).

    """
    def read(self) -> bytes:
        """
        A blob supports reading its content as bytes.

        """
        raise NotImplementedError

    def close(self) -> None:
        """
        A blob may be closed.

        """
        pass
