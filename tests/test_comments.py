"""Unit tests for `comform.comments`."""

import tempfile
from io import StringIO

from comform.comments import Chunk, Comment, get_comments, to_chunks
from comform.fixes import _apply_fixes, _get_fixes

SCRIPT_PRE = """\
# Block comment line 1
# Block comment line 2

print("hello, world")  # inline comment 1
print("bye")  # inline comment 2

# Final comment
"""

SCRIPT_POST = """\
# Block comment line 1 Block comment line 2

print("hello, world")  # inline comment 1
print("bye")  # inline comment 2

# Final comment
"""

LINES_PRE = StringIO(SCRIPT_PRE).readlines()

COMMENTS = [
    Comment(" Block comment line 1", 1, 0, False),
    Comment(" Block comment line 2", 2, 0, False),
    Comment(" inline comment 1", 4, 23, True),
    Comment(" inline comment 2", 5, 14, True),
    Comment(" Final comment", 7, 0, False),
]


CHUNKS = [
    Chunk([COMMENTS[0], COMMENTS[1]]),
    Chunk([COMMENTS[2], COMMENTS[3]]),
    Chunk([COMMENTS[4]]),
]

FIXED_CHUNKS = [
    Chunk([Comment(" Block comment line 1 Block comment line 2", 1, 0, False)]),
    Chunk([COMMENTS[2], COMMENTS[3]]),
    Chunk([COMMENTS[4]]),
]

FIXES = list(zip(CHUNKS, FIXED_CHUNKS))


def test_comments_from_files() -> None:
    with tempfile.TemporaryFile(mode="r+") as fp:
        fp.write(SCRIPT_PRE)
        fp.seek(0)
        comments = list(get_comments(fp))  # type: ignore[arg-type]
    assert comments == COMMENTS


def test_chunking() -> None:
    assert to_chunks(COMMENTS) == CHUNKS


def test_chunk_fixer() -> None:
    assert _get_fixes(CHUNKS) == FIXES


def test_apply_fixes() -> None:
    new_lines = _apply_fixes(FIXES, LINES_PRE)
    assert SCRIPT_POST == "".join(new_lines)


if __name__ == "__main__":
    test_comments_from_files()
    test_chunking()
    test_chunk_fixer()
    test_apply_fixes()
