from comform.cli import Options
from comform.comments import Chunk, Comment
from tests.cases import CaseData

_NAME = "Check inline comments align."

_OPTIONS = Options(check=True, align=True, dividers=False, wrap=88, paths=[])

_OLD_TEXT = """\
print("hello, world")  # inline comment 1
print("bye")  # inline comment 2
"""

_OLD_COMMENTS = [
    Comment(" inline comment 1", 1, 23, True),
    Comment(" inline comment 2", 2, 14, True),
]

_NEW_TEXT = """\
print("hello, world")  # inline comment 1
print("bye")           # inline comment 2
"""

_OLD_CHUNKS = [Chunk(_OLD_COMMENTS)]

_NEW_CHUNKS = [
    Chunk(
        [
            Comment(" inline comment 1", 1, 23, True),
            Comment(" inline comment 2", 2, 23, True),
        ]
    )
]

CASE = CaseData(
    _NAME, _OPTIONS, _OLD_TEXT, _OLD_COMMENTS, _OLD_CHUNKS, _NEW_CHUNKS, _NEW_TEXT
)