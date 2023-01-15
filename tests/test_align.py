from comform.kernel import CodeLine, fix_align

TEST_KEY = "align"


def test_align() -> None:

    with open(Rf".\tests\examples\{TEST_KEY}_good.py") as fh:
        correct_text = fh.read()

    with open(Rf".\tests\examples\{TEST_KEY}_bad.py") as fh:
        text_lines = fh.readlines()
    code_lines = [CodeLine(line) for line in text_lines]
    fix_align(code_lines)

    assert correct_text == "".join(code_lines)
