from comform.cli import Options
from comform.comments import Chunk, Comment
from tests.cases import CaseData

_NAME = "Check multiline strings are kept."

_OPTIONS = Options(check=True, align=True, dividers=False, wrap=88, paths=[])

_OLD_TEXT = '''\
x = """This is a multi
line string"""
# comment
'''

_OLD_COMMENTS = [Comment(" comment", 3, 0, False)]

_NEW_TEXT = _OLD_TEXT

_OLD_CHUNKS = [Chunk(_OLD_COMMENTS)]

_NEW_CHUNKS = _OLD_CHUNKS

CASE = CaseData(
    _NAME, _OPTIONS, _OLD_TEXT, _OLD_COMMENTS, _OLD_CHUNKS, _NEW_CHUNKS, _NEW_TEXT
)