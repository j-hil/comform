from comform.kernel import CodeLine, fix_blocks

CORRECT_TEXT = """\
# this is a really long piece of text. lets get some bad spacing some random short new
# lines as well as some lines which absolutely exceed any reasonable length with no
# consideration for people with small screens. we're not all rich maybe some bullets?
#
# - hey there person will this bullet be too long? oh nooooooo please keep it shorter so i
#   can read it ughhh
# - this bullet is shorter
#

print("hello, world")
"""


def test_blocks() -> None:
    with open(R".\tests\examples\bad_block.py") as fh:
        text_lines = fh.readlines()
    code_lines = [CodeLine(line) for line in text_lines]

    fix_blocks(code_lines)
    assert CORRECT_TEXT == "".join(code_lines)
