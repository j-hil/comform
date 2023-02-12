"""Orphan utility functions.

For functions which are not explicitly part of the project structure but which are used
non-the-less. Includes:
- `zip_padded`; a generalization of `zip_longest`
- `format_as_md` & `format_line`; both wrappers around `mdformat.text`
"""

from __future__ import annotations

from itertools import zip_longest
from typing import Any, Generator, Iterable, Literal, TypeVar, overload

import mdformat

_SENTINEL = object()

T = TypeVar("T")
U = TypeVar("U")
V = TypeVar("V")


@overload
def zip_padded(
    arg1: Iterable[T],
    arg2: Iterable[U],
    arg3: Iterable[V],
    /,
    *,
    fillvals: tuple[T, U, V],
) -> Generator[tuple[T, U, V], None, None]:
    ...


@overload
def zip_padded(
    arg1: Iterable[T], arg2: Iterable[U], /, *, fillvals: tuple[T, U]
) -> Generator[tuple[T, U], None, None]:
    ...


def zip_padded(
    *args: Iterable[Any], fillvals: Iterable[Any]
) -> Generator[tuple[Any, ...], None, None]:
    for row in zip_longest(*args, fillvalue=_SENTINEL):
        yield tuple(v if v is not _SENTINEL else f for v, f in zip(row, fillvals))


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
