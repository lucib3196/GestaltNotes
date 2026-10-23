"""Import model modules to register their tables with SQLModel metadata."""

import sys
from importlib import import_module
from pathlib import Path

import backend


def _import_model_modules() -> None:
    root = Path(next(iter(backend.__path__))).resolve()

    for path in sorted(root.rglob("*.py")):
        relative = path.relative_to(root)

        if not (
            path.stem in {"model", "models"}
            or {"model", "models"}.intersection(relative.parts[:-1])
        ):
            continue

        parts = relative.with_suffix("").parts
        if parts[-1] == "__init__":
            parts = parts[:-1]

        module_name = ".".join(("backend", *parts))
        if module_name not in sys.modules:
            import_module(module_name)


_import_model_modules()
