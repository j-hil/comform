"""Unit tests for `comform.cli`."""
from __future__ import annotations

from io import StringIO
from typing import Any
from unittest.mock import Mock, mock_open, patch

from comform import run
from comform.cli import Options, get_options

SCRIPT_POST = """\
# Block comment line 1 Block comment line 2

print("hello, world")  # inline comment 1
print("bye")  # inline comment 2

# Final comment
"""
LINES_POST = StringIO(SCRIPT_POST).readlines()


def test_get_options() -> None:
    parser = get_options(
        "--check --align --dividers --wrap 101 file1 file2 file3".split()
    )

    assert parser.check
    assert parser.align
    assert parser.dividers
    assert parser.wrap == 101
    assert parser.paths == ["file1", "file2", "file3"]

    parser = get_options("file1 file2".split())
    assert not parser.check
    assert not parser.align
    assert not parser.dividers
    assert parser.wrap == 88
    assert parser.paths == ["file1", "file2"]


@patch("comform.open", new_callable=mock_open)
@patch("comform.print")
@patch("comform.get_options")
@patch("comform.fix_text")
def test_run(
    mock_fix_text: Mock,
    mock_get_options: Mock,
    mock_print: Mock,  # prevent writing to stdout during test
    mock_open: Mock,
) -> None:
    kwargs: dict[str, Any] = {
        "check": False,
        "align": False,
        "dividers": False,
        "wrap": 88,
        "paths": ["file1.py"],
    }
    mock_get_options.return_value = Options(**kwargs)

    fp1_mock = Mock()
    fp1_mock.__enter__ = Mock(return_value=fp1_mock)
    fp1_mock.__exit__ = Mock(return_value=False)
    mock_open.return_value = fp1_mock

    mock_fix_text.return_value = LINES_POST, []
    run()

    kwargs["check"] = True
    mock_get_options.return_value = Options(**kwargs)
    run()

    # Should only have been called on the first run:
    fp1_mock.writelines.assert_called_once_with(LINES_POST)


if __name__ == "__main__":
    test_get_options()
    test_run()
