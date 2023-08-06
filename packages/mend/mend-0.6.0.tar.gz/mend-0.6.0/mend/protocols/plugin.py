from mend.protocols.parameters import WithParameters
from mend.protocols.tree import Tree


class Plugin(WithParameters["Plugin"]):
    """
    A plugin supports applying a generated `Tree` in some way.

    """
    def apply(self, tree: Tree) -> None:
        """
        Apply the plugin to a `Tree`.

        """
        raise NotImplementedError

    def close(self) -> None:
        """
        A plugin may be closed.

        """
        pass
