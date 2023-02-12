"""Unit tests for `comform.utils`."""

from comform.utils import zip_padded


def test_zip_padded() -> None:
    actual = list(zip_padded("abc", [1, 2, 3, 4, 5], (11, 12), fillvals=("x", 0, 11)))
    expected = [("a", 1, 11), ("b", 2, 12), ("c", 3, 11), ("x", 4, 11), ("x", 5, 11)]
    assert actual == expected
