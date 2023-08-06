from typing import (
    Generic,
    Iterable,
    Protocol,
    Type,
    TypeVar,
)

from click import Parameter


T = TypeVar("T", covariant=True)


class WithParameters(Generic[T], Protocol):
    """
    A type that supports creation from a `click` CLI command.

    """
    @classmethod
    def iter_parameters(cls: Type[T]) -> Iterable[Parameter]:
        return []

    @classmethod
    def from_parameters(cls: Type[T], *args, **kwargs) -> T:
        return cls()
