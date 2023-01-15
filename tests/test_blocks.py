from comform.kernel import CodeLine, fix_blocks

TEST_KEY = "blocks"


def test_align() -> None:

    with open(Rf".\tests\examples\{TEST_KEY}_good.py") as fh:
        correct_text = fh.read()

    with open(Rf".\tests\examples\{TEST_KEY}_bad.py") as fh:
        text_lines = fh.readlines()
    code_lines = [CodeLine(line) for line in text_lines]
    fix_blocks(code_lines)

    assert correct_text == "".join(code_lines)
