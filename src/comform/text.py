"""Wrapper around `mdformat`."""

from typing import Any, Literal, overload

import mdformat


@overload
def format_as_md(
    text: str,
    /,
    *,
    wrap: int | Literal["keep", "no"] = "keep",
    number: bool = False,
    eol: Literal["lf", "crlf", "keep"] = "lf",
) -> str:
    ...


# duplicative signature necessary as mypy doesn't support only 1 overload. See
# `https://github.com/python/mypy/issues/5047` for discussion.
@overload
def format_as_md(text: str, /, **kwargs: Any) -> str:
    ...


def format_as_md(text: str, /, **kwargs: Any) -> str:
    return mdformat.text(text, options={**kwargs})
