"""Unit tests for `comform.cli`."""
from __future__ import annotations

from comform.cli import get_options


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


if __name__ == "__main__":
    test_get_options()
