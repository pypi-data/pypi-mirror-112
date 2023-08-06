from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Type

from jinja2 import Environment

from mend.protocols import Blob, Tree
from mend.templates.blob import TemplateBlob


def default_filter_func(value: str) -> bool:
    path = Path(value)

    # NB: ignore temporary files
    if path.name.endswith("~"):
        return False

    # NB: ignore internal files
    if path.name.startswith("_"):
        return False

    return True


FilterFunc = Callable[[str], bool]


@dataclass(frozen=True)
class TemplateTree(Tree):
    blobs: dict[Path, Blob]

    @classmethod
    def from_environment(
            cls: Type["TemplateTree"],
            environment: Environment,
            context: dict[str, Any],
            filter_func: FilterFunc = default_filter_func,
    ) -> "TemplateTree":
        paths = environment.list_templates(
            filter_func=filter_func,
        )

        blobs = [
            TemplateBlob(
                context=context,
                path=Path(path),
                template=environment.get_template(path),
            )
            for path in paths
        ]

        return cls({
            blob.path: blob
            for blob in blobs
        })
