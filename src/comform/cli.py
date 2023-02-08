"""Define the CLI."""

from __future__ import annotations

from argparse import ArgumentDefaultsHelpFormatter, ArgumentParser
from dataclasses import dataclass

import comform


@dataclass(frozen=True)
class FormatOptions:
    align: bool
    dividers: bool
    wrap: int


def get_options(args: list[str]) -> tuple[bool, FormatOptions, list[str]]:
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

    parsed_args = parser.parse_args(args)
    return (
        parsed_args.check,
        FormatOptions(parsed_args.align, parsed_args.dividers, parsed_args.wrap),
        parsed_args.paths,
    )
