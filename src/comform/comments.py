"""Retrieval and processing of comments."""

from __future__ import annotations

import tokenize
from dataclasses import dataclass
from io import BufferedReader
from token import COMMENT, ENCODING, INDENT, NEWLINE, NL
from typing import Generator, List, Tuple

from comform.text import format_as_md


@dataclass(frozen=True)
class Comment:
    __slots__ = "text", "hash_row", "hash_col", "inline"

    text: str
    hash_row: int  # TODO: rename to lineno
    hash_col: int
    inline: bool


Chunk = List[Comment]
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
    curr_chunk = [prev_comment]
    i = 1

    while i < len(comments):
        curr_comment = comments[i]

        if (
            curr_comment.hash_row == prev_comment.hash_row + 1
            and prev_comment.inline == curr_comment.inline
        ):
            curr_chunk.append(curr_comment)
        else:
            chunks.append(curr_chunk)
            curr_chunk = [curr_comment]

        prev_comment = curr_comment
        i += 1
    chunks.append(curr_chunk)

    return chunks


def get_fixes(chunks: list[Chunk], /, col_max: int = 88) -> Fixes:
    fixes = []
    for old_chunk in chunks:
        chunk_inline = old_chunk[0].inline
        chunk_col = old_chunk[0].hash_col
        chunk_row = old_chunk[0].hash_row

        if chunk_inline:
            # currently do nothing to non-block comments
            fixes.append((old_chunk, old_chunk))
            continue

        text = format_as_md(
            text="\n".join(comment.text for comment in old_chunk),
            number=True,
            wrap=col_max - chunk_col - len("# "),
        ).strip()

        new_chunk = [
            Comment(f" {line}" if line else "", chunk_row + j, chunk_col, False)
            for j, line in enumerate(text.split("\n"))
        ]

        fixes.append((old_chunk, new_chunk))
    return fixes


def apply_fixes(fixes: Fixes, old_lines: list[bytes]) -> list[bytes]:
    new_lines = []

    prev_end_lineno = 0
    for fix in fixes:
        old_chunk, new_chunk = fix

        start_lineno = old_chunk[0].hash_row
        end_lineno = old_chunk[-1].hash_row
        chunk_inline = old_chunk[0].inline

        new_lines.extend(old_lines[prev_end_lineno : start_lineno - 1])
        if not chunk_inline:
            new_lines.extend(f"#{comment.text}\n".encode() for comment in new_chunk)
        else:
            new_lines.extend(old_lines[start_lineno - 1 : end_lineno])

        prev_end_lineno = end_lineno

    new_lines.append(b"")  # TODO: shouldn't be necessary?
    return new_lines
