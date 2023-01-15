from comform.kernel import CodeLine, fix_sections

CORRECT_TEXT = """\
# -- this is a section divider --------------------------------------------------------- #

print("section 1")

# -- this is another with bad spacing -------------------------------------------------- #

print("section 2")

# -- finally here is one that's too long ----------------------------------------------- #
"""


def test_blocks() -> None:
    with open(R".\tests\examples\bad_sections.py") as fh:
        text_lines = fh.readlines()
    code_lines = [CodeLine(line) for line in text_lines]

    fix_sections(code_lines)
    assert CORRECT_TEXT == "".join(code_lines)
