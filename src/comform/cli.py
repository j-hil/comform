"""Command line interface and entry point `run` function."""

from __future__ import annotations

from argparse import ArgumentDefaultsHelpFormatter, ArgumentParser
from dataclasses import dataclass

import comform


@dataclass(frozen=True)
class Options:
    check: bool
    align: bool
    dividers: bool
    wrap: int
    paths: list[str]


def get_options(args: list[str]) -> Options:
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

    parsed_args = parser.parse_args(args)
    return Options(
        parsed_args.check,
        parsed_args.align,
        parsed_args.dividers,
        parsed_args.wrap,
        parsed_args.paths,
    )
