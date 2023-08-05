from typing import Protocol


class Blob(Protocol):

    def close(self) -> None:
        pass

    def read(self) -> bytes:
        raise NotImplementedError
