from __future__ import annotations

from typing import List, TextIO, Tuple
from warnings import warn

from comform.cli import Options
from comform.comments import Chunk, Comment, get_comments, to_chunks
from comform.text import format_as_md

Fixes = List[Tuple[Chunk, Chunk]]


def _get_fixes(chunks: list[Chunk], /, col_max: int = 88) -> Fixes:
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


def _apply_fixes(fixes: Fixes, old_lines: list[str]) -> list[str]:
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


def fix_text(stream: TextIO, options: Options) -> tuple[list[str], list[str]]:
    old_comments = list(get_comments(stream))
    stream.seek(0)
    old_lines = stream.readlines()

    if options.align or options.dividers:
        warn("Options `align` & `dividers` are not yet implemented.")

    chunks = to_chunks(old_comments)
    fixes = _get_fixes(chunks, col_max=options.wrap)
    new_lines = _apply_fixes(fixes, old_lines)
    return new_lines, old_lines
