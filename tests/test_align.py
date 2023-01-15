from comform.kernel import CodeLine, fix_align

CORRECT_TEXT = """\
from unittest.mock import Mock

my_func = Mock()
arg1 = woah_another_arg = wow_its_really_unclear_what_each_arg_does = arg4 = Mock()

thing = my_func(
    arg1,                                       # this is a comment
    woah_another_arg,                           # this arg is really important
    wow_its_really_unclear_what_each_arg_does,  # people should implement kwargs :/
    arg4,                                       # last but not least
)
"""


def test_blocks() -> None:
    with open(R".\tests\examples\bad_align.py") as fh:
        text_lines = fh.readlines()
    code_lines = [CodeLine(line) for line in text_lines]

    fix_align(code_lines)
    assert CORRECT_TEXT == "".join(code_lines)
