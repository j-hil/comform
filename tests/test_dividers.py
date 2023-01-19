from comform.codeline import CodeLines
from comform.kernel import fix_dividers

TEST_KEY = "dividers"


def test_dividers() -> None:

    with open(Rf".\tests\examples\{TEST_KEY}_good.py") as fh:
        correct_text = fh.read()

    code_lines = CodeLines(Rf".\tests\examples\{TEST_KEY}_bad.py")
    fix_dividers(code_lines)
    result = "".join(line.text for line in code_lines)

    # with open("temp.py", "w") as fh:
    #     fh.write(result)
    assert correct_text == result
