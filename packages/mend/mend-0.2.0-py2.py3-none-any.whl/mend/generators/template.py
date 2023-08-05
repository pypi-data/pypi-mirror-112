from dataclasses import dataclass, field
from io import BytesIO
from typing import Any, Callable

from jinja2 import BaseLoader, Environment, StrictUndefined

from mend.protocols import Generator, Tree


def is_temporary(path: str) -> bool:
    return not path.endswith("~")


FilterFunc = Callable[[str], bool]


@dataclass(frozen=True)
class TemplateGenerator(Generator):
    """
    Generate from templates.

    """
    loader: BaseLoader
    context: dict[str, Any] = field(default_factory=dict)
    filter_func: FilterFunc = is_temporary

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

        paths = environment.list_templates(
            filter_func=self.filter_func,  # type: ignore
        )

        templates = {
            path: environment.get_template(path)
            for path in paths
        }

        return {
            path: BytesIO(template.render(self.context).encode("utf-8"))
            for path, template in templates.items()
        }
