from comform.kernel import run_all

TEST_KEY = "align"


def test_blocks() -> None:
    with open(Rf".\tests\examples\{TEST_KEY}_good.py") as fh:
        correct_text = fh.read()
    assert correct_text == run_all(Rf".\tests\examples\{TEST_KEY}_bad.py")
