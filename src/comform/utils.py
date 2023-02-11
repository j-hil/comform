"""Orphan utility functions.

For functions which are not explicitly part of the project structure but which are used
non-the-less. Includes:
- `zip_padded`; a generalization of `zip_longest`
- `format_as_md` & `format_line`; both wrappers around `mdformat.text`
"""

from __future__ import annotations

from itertools import zip_longest
from typing import Any, Generator, Iterable, Literal

import mdformat

_SENTINEL = object()


def zip_padded(
    *args: Iterable[Any], fillvals: Iterable[Any]
) -> Generator[list[Any], None, None]:
    for row in zip_longest(*args, fillvalue=_SENTINEL):
        yield tuple(v if v is not _SENTINEL else fillvals[i] for i, v in enumerate(row))


def format_as_md(
    text: str,
    *,
    wrap: int | Literal["keep", "no"] = "keep",
    number: bool = False,
    eol: Literal["lf", "crlf", "keep"] = "lf",
) -> str:
    options = {"wrap": wrap, "number": number, "end-of-line": eol}
    return mdformat.text(text, options=options).strip()


def format_line(text: str) -> str:
    return format_as_md(text, wrap="no").strip()
