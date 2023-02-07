"""API and metadata."""

from __future__ import annotations

import sys
from io import StringIO
from pathlib import Path
from typing import TextIO

from comform.cli import Options, get_options
from comform.fixes import fix_text

__version__ = "0.0.3"

# TODO:
# * other todos
# * format one line comments with mdformat
# * don't change non python files


def format_comments(
    # NOTE: keep in line with `comform.cli`
    text: str | TextIO,
    align: bool = False,
    dividers: bool = False,
    wrap: int = 88,
) -> list[str]:
    """Format python comments in a string or text stream.

    :param text: Text to be formatted
    :param align: Align inline comments if true.
    :param dividers: Expand/shrink 'divider' comments if true.
    :param wrap: Column at which to wrap comments.
    :return: Formatted text.
    """
    if isinstance(text, str):
        text = StringIO(text)
    options = Options(False, align, dividers, wrap, [])
    new_lines, _ = fix_text(text, options)
    return new_lines


def run(args: list[str] | None = None) -> None:
    """Entry point for `comform`.

    :param args: Command line arguments, defaults to reading from `sys.argv[1:]` but can
        be passed manually - see `comform -h` for usage.
    """
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
