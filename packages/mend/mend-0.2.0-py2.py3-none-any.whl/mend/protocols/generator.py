from mend.protocols.parameters import WithParameters
from mend.protocols.tree import Tree


class Generator(WithParameters["Generator"]):

    def close(self) -> None:
        pass

    def generate(self) -> Tree:
        raise NotImplementedError
