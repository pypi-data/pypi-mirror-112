from inspect import cleandoc
from pkg_resources import iter_entry_points
from typing import List, Optional, Type

from click import Command, Context, MultiCommand

from mend.protocols import Plugin


def load_plugins() -> dict[str, Type[Plugin]]:
    return {
        entry_point.name: entry_point.load()
        for entry_point in iter_entry_points("mend.plugins")
    }


class PluginGroup(MultiCommand):
    """
    Generate a group of commands based on available plugins.

    """
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.plugins = load_plugins()

    def list_commands(self, context: Context) -> List[str]:
        return list(sorted(self.plugins))

    def get_command(self, context: Context, name: str) -> Optional[Command]:
        try:
            cls = self.plugins[name]
        except KeyError:
            return None

        return Command(
            callback=cls.from_parameters,
            help=cleandoc(cls.__doc__) if cls.__doc__ else None,
            name=name,
            params=list(cls.iter_parameters()),
        )
