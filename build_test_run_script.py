"""
Костыль ибо у меня проблемы со скопами во время запуска тестов последовательно
"""

import importlib
import inspect
import os
from pathlib import Path


def process_file(file_path: Path) -> list[str]:
    module = importlib.import_module(str(file_path).replace("\\", ".")[:-3])
    funcs = inspect.getmembers(module, inspect.isfunction)
    return [
        f"{file_path}::{name}".replace("\\", "/")
        for name, _ in funcs
        if name.startswith("test_")
    ]


def process(path: Path):
    paths = []
    for root, _, files in os.walk(path):
        for file in files:
            if file.endswith(".py") and file.startswith("test_"):
                paths.extend(process_file(Path(root) / file))
    return paths


def build(base: Path = Path(__file__).parent):
    path = base / "tests"
    path = path.relative_to(base)

    paths = process(path)
    with open(base / "run_tests.sh", "w", encoding="utf8") as file:
        file.write(
            '#!/bin/bash\n\n{}\n\necho "Finish"\nsleep 2'.format(
                "\n".join(map(lambda p: f"echo $(poetry run pytest {p})", paths))
            )
        )


if __name__ == "__main__":
    build()
