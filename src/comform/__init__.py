"""API and metadata."""

from __future__ import annotations

import sys
from pathlib import Path

from comform.cli import get_options
from comform.fixes import fix_text

__version__ = "0.0.2"

# TODO: add fix_str(x: TextIO | str) function and give funcs in API docstrings


def run(args: list[str] | None = None) -> None:
    if args is None:
        args = sys.argv[1:]

    options = get_options(args)

    altered = []
    for path_name in options.paths:
        path = Path(path_name)
        file_paths = path.glob("**/*.py") if path.is_dir() else [path]

        for file in file_paths:
            with open(file, encoding="utf-8") as fp:
                new_lines, old_lines = fix_text(fp, options)

            if new_lines == old_lines:
                continue
            altered.append(str(file))

            if options.check:
                print(f"*** Changes to {path_name}:", "-" * 99, sep="\n")
                print(*new_lines, "\n")
                continue
            with open(file, "w", encoding="utf-8") as fp:
                fp.writelines(new_lines)

    header = "*** Altered Files:" if not options.check else "*** Failed files:"
    print(header, *(altered if altered else ["\b(None)"]), sep="\n")
