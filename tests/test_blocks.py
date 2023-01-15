from comform.kernel import CodeLine, fix_blocks

TEST_KEY = "blocks"


def test_blocks() -> None:

    with open(Rf".\tests\examples\{TEST_KEY}_good.py") as fh:
        correct_text = fh.read()

    with open(Rf".\tests\examples\{TEST_KEY}_bad.py") as fh:
        text_lines = fh.readlines()
    code_lines = [CodeLine(line) for line in text_lines]
    fix_blocks(code_lines)
    result = "".join(code_lines)

    # with open("temp.py", "w") as fh:
    #     fh.write(result)
    assert correct_text == result
