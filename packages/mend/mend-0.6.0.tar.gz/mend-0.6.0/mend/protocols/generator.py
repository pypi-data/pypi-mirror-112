from mend.protocols.parameters import WithParameters
from mend.protocols.tree import Tree


class Generator(WithParameters["Generator"]):
    """
    A generator supports producing a tree.

    """
    def generate(self) -> Tree:
        """
        Generate a `Tree`.

        """
        raise NotImplementedError

    def close(self) -> None:
        """
        A generator may be closed.

        """
        pass
