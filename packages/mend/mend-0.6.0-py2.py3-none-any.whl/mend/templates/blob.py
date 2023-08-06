from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from jinja2 import Template

from mend.protocols import Blob


@dataclass(frozen=True)
class TemplateBlob(Blob):
    path: Path
    template: Template
    context: dict[str, Any] = field(default_factory=dict)

    def close(self) -> None:
        pass

    def read(self) -> bytes:
        return self.template.render(self.context).encode("utf-8")
