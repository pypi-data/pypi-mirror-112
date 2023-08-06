from dataclasses import dataclass, field
from typing import Any

from jinja2 import BaseLoader, Environment, StrictUndefined

from mend.protocols import Generator, Tree
from mend.templates import TemplateTree


@dataclass(frozen=True)
class TemplateGenerator(Generator):
    """
    Generate from templates.

    """
    loader: BaseLoader
    context: dict[str, Any] = field(default_factory=dict)

    def make_environment(self) -> Environment:
        return Environment(
            loader=self.loader,
            lstrip_blocks=True,
            trim_blocks=True,
            keep_trailing_newline=True,
            undefined=StrictUndefined,
        )

    def generate(self) -> Tree:
        environment = self.make_environment()

        return TemplateTree.from_environment(
            environment=environment,
            context=self.context,
        )
