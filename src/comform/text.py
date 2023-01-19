from typing import Literal, overload

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


def format_as_md(text: str, /, **kwargs) -> str:
    return mdformat.text(text, options={**kwargs})
