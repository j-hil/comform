"""Command line interface and entry point `run` function."""

from __future__ import annotations

import sys
from argparse import ArgumentDefaultsHelpFormatter, ArgumentParser
from pathlib import Path
from warnings import warn

import comform
from comform.comments import apply_fixes, get_comments, get_fixes, to_chunks


def get_parser() -> ArgumentParser:
    parser = ArgumentParser(
        prog="comform",
        description="Python Comment Conformity Formatter",
        formatter_class=ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--version",
        "-v",
        action="version",
        help="print the version number",
        version=comform.__version__,
    )
    # TODO: check, align and dividers are just for show now...
    parser.add_argument(
        "--check", "-c", action="store_true", help="do not write to files."
    )
    parser.add_argument(
        "--align", "-a", action="store_true", help="align in-line comments"
    )
    parser.add_argument(
        "--dividers", "-d", action="store_true", help="correct section divider comments"
    )
    parser.add_argument(
        "--wrap",
        "-w",
        default=88,
        type=int,
        help="Column at which to wrap comments",
        metavar="N",
    )
    parser.add_argument(
        "paths", nargs="+", help="folders/files to re-format (recursively)"
    )

    return parser


def run(args: list[str] | None = None) -> None:
    if args is None:
        args = sys.argv[1:]

    options = get_parser().parse_args(args)

    altered = []
    for path_name in options.paths:
        path = Path(path_name)
        file_paths = path.glob("**/*.py") if path.is_dir() else [path]

        for file in file_paths:
            with open(file, "rb") as fp:
                old_lines = fp.readlines()
                fp.seek(0)
                old_comments = list(get_comments(fp))

            if options.align or options.dividers:
                warn("Options `align` & `dividers` are not yet implemented.")

            chunks = to_chunks(old_comments)
            fixes = get_fixes(chunks, col_max=options.wrap)
            new_lines = apply_fixes(fixes, old_lines)

            if new_lines == old_lines:
                continue

            result = b"".join(new_lines)
            altered.append(str(file))

            if options.check:
                print(f"*** Changes to {path_name}:", "-" * 99, sep="\n")
                print(result.decode(), "", sep="\n")
                continue

            with open(file, "wb") as fp:
                fp.write(result)

    header = "*** Altered Files:" if not options.check else "*** Failed files:"
    print(header, *(altered if altered else ["\b(None)"]), sep="\n")
