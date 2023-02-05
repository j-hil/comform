"""Unit tests for `comform.cli`."""

from argparse import Namespace
from io import StringIO
from unittest.mock import Mock, mock_open, patch

from comform.cli import get_parser, run

SCRIPT_POST = """\
# Block comment line 1 Block comment line 2

print("hello, world")  # inline comment 1
print("bye")  # inline comment 2

# Final comment
"""
LINES_POST = StringIO(SCRIPT_POST).readlines()


def test_get_parser() -> None:
    parser = get_parser().parse_args(
        "--check --align --dividers --wrap 101 file1 file2 file3".split()
    )

    assert parser.check
    assert parser.align
    assert parser.dividers
    assert parser.wrap == 101
    assert parser.paths == ["file1", "file2", "file3"]

    parser = get_parser().parse_args("file1 file2".split())
    assert not parser.check
    assert not parser.align
    assert not parser.dividers
    assert parser.wrap == 88
    assert parser.paths == ["file1", "file2"]


@patch("comform.cli.apply_fixes")
@patch("comform.cli.get_fixes")
@patch("comform.cli.to_chunks")
@patch("comform.cli.get_comments")
@patch("builtins.open", new_callable=mock_open)
@patch("comform.cli.ArgumentParser.parse_args")
@patch("comform.cli.print")
def test_run(
    mock_print: Mock,  # prevent writing to stdout during test
    mock_parse_args: Mock,
    mock_open: Mock,
    # mocking the functions form `comform.comments` makes this a true(r) unit test
    mock_get_comments: Mock,
    mock_to_chunks: Mock,
    mock_get_fixes: Mock,
    mock_apply_fixes: Mock,
) -> None:
    kwargs = {
        "check": False,
        "align": False,
        "dividers": False,
        "wrap": 88,
        "paths": ["file1.py"],
    }
    mock_parse_args.return_value = Namespace(**kwargs)

    fp1_mock = Mock()
    fp1_mock.__enter__ = Mock(return_value=fp1_mock)
    fp1_mock.__exit__ = Mock(return_value=False)
    mock_open.return_value = fp1_mock

    mock_apply_fixes.return_value = LINES_POST

    run()

    kwargs["check"] = True
    mock_parse_args.return_value = Namespace(**kwargs)
    run()

    # Should only have been called on the first run:
    fp1_mock.write.assert_called_once_with(SCRIPT_POST)


if __name__ == "__main__":
    test_get_parser()
    test_run()
