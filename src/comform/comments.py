"""Retrieval and processing of comments."""

from __future__ import annotations

import tokenize
from dataclasses import dataclass
from io import BufferedReader
from token import COMMENT, ENCODING, INDENT, NEWLINE, NL
from typing import Generator, Iterable, List, Tuple

from comform.text import format_as_md


@dataclass(frozen=True)
class Comment:
    __slots__ = "text", "lineno", "hash_col", "inline"

    text: str
    lineno: int
    hash_col: int
    inline: bool


class Chunk(List[Comment]):
    def __init__(self, _iterable: Iterable[Comment]) -> None:
        if not _iterable:
            raise ValueError("Do not allow an empty `Chunk`.")
        super().__init__(_iterable)

        repr_comment = self[0]
        self.start_lineno = repr_comment.lineno
        self.hash_col = repr_comment.hash_col
        self.inline = repr_comment.inline


Fixes = List[Tuple[Chunk, Chunk]]


def get_comments(fp: BufferedReader) -> Generator[Comment, None, None]:
    inline = False
    for token in tokenize.tokenize(fp.readline):
        if token.type in [NL, NEWLINE]:
            inline = False
        elif token.type is COMMENT:
            yield Comment(token.string[1:], *token.start, inline)
        elif token.type not in [INDENT, ENCODING]:
            inline = True


def to_chunks(comments: list[Comment]) -> list[Chunk]:
    if not comments:
        return []

    chunks = []
    prev_comment = comments[0]
    curr_chunk = Chunk([prev_comment])
    i = 1

    while i < len(comments):
        curr_comment = comments[i]

        if (
            curr_comment.lineno == prev_comment.lineno + 1
            and prev_comment.inline == curr_comment.inline
        ):
            curr_chunk.append(curr_comment)
        else:
            chunks.append(curr_chunk)
            curr_chunk = Chunk([curr_comment])

        prev_comment = curr_comment
        i += 1
    chunks.append(curr_chunk)

    return chunks


def get_fixes(chunks: list[Chunk], /, col_max: int = 88) -> Fixes:
    fixes = []
    for chunk in chunks:
        if chunk.inline:
            # currently do nothing to non-block comments
            fixes.append((chunk, chunk))
            continue

        text = format_as_md(
            text="\n".join(comment.text for comment in chunk),
            number=True,
            wrap=col_max - chunk.hash_col - len("# "),
        ).strip()

        new_chunk = Chunk(
            Comment(f" {line}".rstrip(), chunk.start_lineno + j, chunk.hash_col, False)
            for j, line in enumerate(text.split("\n"))
        )

        fixes.append((chunk, new_chunk))
    return fixes


def apply_fixes(fixes: Fixes, old_lines: list[str]) -> list[str]:
    new_lines = []

    prev_end_lineno = 0
    for fix in fixes:
        old_chunk, new_chunk = fix
        end_lineno = old_chunk[-1].lineno

        new_lines.extend(old_lines[prev_end_lineno : old_chunk.start_lineno - 1])
        if not old_chunk.inline:
            new_lines.extend(f"#{comment.text}\n" for comment in new_chunk)
        else:
            new_lines.extend(old_lines[old_chunk.start_lineno - 1 : end_lineno])

        prev_end_lineno = end_lineno

    new_lines.append("")
    return new_lines
