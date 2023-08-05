from click import command

from mend.cli.generators import GeneratorGroup


@command(cls=GeneratorGroup)
def main(*args, **kwargs) -> None:
    """
    Mend, update, and repair git respositories.

    """
    pass
