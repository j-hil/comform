"""Unit tests for `comform.cli`."""
from __future__ import annotations

from unittest.mock import patch

from comform.cli import get_options


@patch("comform.cli.Path")
def test_get_options_no_config(mocked_path_class) -> None:
    """Test getting options from CLI, no `pyproject.toml` present."""

    # Ensure a config is not accessed:
    mocked_path_class.cwd().__truediv__().is_file.return_value = False

    check, options, path_names = get_options(
        "--check --align --dividers --wrap 101 file1 file2 file3".split()
    )
    assert check
    assert options.align
    assert options.dividers
    assert options.wrap == 101
    assert path_names == ["file1", "file2", "file3"]

    check, options, path_names = get_options("file1 file2".split())
    assert not check
    assert not options.align
    assert not options.dividers
    assert options.wrap == 88
    assert path_names == ["file1", "file2"]


@patch("comform.cli.Path")
@patch("comform.cli.tomllib.load")
@patch("comform.cli.open")
def test_get_options_with_empty_config(
    mocked_open, mocked_tomllib_load, mocked_path_class
) -> None:
    """Test when `pyproject.toml` present, but no `tool.comform` section."""

    mocked_path_class.cwd().__truediv__().is_file.return_value = True
    mocked_tomllib_load.return_value = {}

    check, options, path_names = get_options(
        "--check --align --dividers --wrap 101 file1 file2 file3".split()
    )
    assert check
    assert options.align
    assert options.dividers
    assert options.wrap == 101
    assert path_names == ["file1", "file2", "file3"]

    check, options, path_names = get_options("file1 file2".split())
    assert not check
    assert not options.align
    assert not options.dividers
    assert options.wrap == 88
    assert path_names == ["file1", "file2"]


@patch("comform.cli.Path")
@patch("comform.cli.tomllib.load")
@patch("comform.cli.open")
def test_get_options_with_config(
    mocked_open, mocked_tomllib_load, mocked_path_class
) -> None:
    """Test when `pyproject.toml` present, but no `tool.comform` section."""

    mocked_path_class.cwd().__truediv__().is_file.return_value = True

    mocked_tomllib_load().get().get.return_value = {
        "check": False,
        "align": False,
        "dividers": False,
    }
    check, options, path_names = get_options(
        "--check --align --dividers --wrap 101 file1 file2 file3".split()
    )
    assert check
    assert options.align
    assert options.dividers
    assert options.wrap == 101
    assert path_names == ["file1", "file2", "file3"]

    mocked_tomllib_load().get().get.return_value = {
        "check": True,
        "align": True,
        "dividers": True,
        "wrap": 111,
    }
    check, options, path_names = get_options("file1 file2".split())
    assert check
    assert options.align
    assert options.dividers
    assert options.wrap == 111
    assert path_names == ["file1", "file2"]
