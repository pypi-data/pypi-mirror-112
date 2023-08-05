from contextlib import closing
from inspect import cleandoc
from pkg_resources import get_entry_map
from typing import List, Optional, Type

from click import Command, Context, MultiCommand

from mend.cli.plugins import PluginGroup
from mend.protocols import Generator, Plugin


def load_generators() -> dict[str, Type[Generator]]:
    return {
        name: module.load()
        for name, module in get_entry_map("mend", "mend.generators").items()
    }


class GeneratorGroup(MultiCommand):
    """
    Generate a group of commands based on available generators.

    """
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.generators = load_generators()

    def list_commands(self, context: Context) -> List[str]:
        return list(sorted(self.generators))

    def get_command(self, context: Context, name: str) -> Optional[Command]:
        try:
            cls = self.generators[name]
        except KeyError:
            return None

        def execute(plugin: Plugin, **kwargs):
            with closing(plugin):
                generator = cls.from_parameters(**kwargs)

                with closing(generator):
                    tree = generator.generate()
                    plugin.apply(tree)

        return PluginGroup(
            help=cleandoc(cls.__doc__) if cls.__doc__ else None,
            name=name,
            params=list(cls.iter_parameters()),
            result_callback=execute,
        )
