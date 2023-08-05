from mend.protocols.parameters import WithParameters
from mend.protocols.tree import Tree


class Plugin(WithParameters["Plugin"]):

    def close(self) -> None:
        pass

    def apply(self, tree: Tree) -> None:
        raise NotImplementedError
