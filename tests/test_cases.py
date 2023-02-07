"""Test Short Cases.

For a number of small examples we test (nearly) every function of the `comform` program.
This allows for quick and easy identification of exactly which cases are failing, and/or
which functions have been broken.

The information for each test case `N` is in `tests.case.caseN`. Adding a new test case
is simple - copy an existing case and edit the `_*` variables as appropriate. Then
extend the `CASES_MODULES` constant in this file.
"""
from __future__ import annotations

from io import StringIO

import pytest

from comform.comments import get_comments, to_chunks
from comform.fixes import _apply_fixes, _get_fixes, fix_text
from tests.cases import CaseData, case1, case2, case3

CASES_MODULES = [case1, case2, case3]
pytestmark = pytest.mark.parametrize("data", [case.CASE for case in CASES_MODULES])


def test_get_comments(data: CaseData) -> None:
    actual_old_comments = list(get_comments(StringIO(data.old_text)))
    assert data.old_comments == actual_old_comments


def test_to_chunks(data: CaseData) -> None:
    actual_old_chunks = to_chunks(data.old_comments)
    assert data.old_chunks == actual_old_chunks


def test_get_fixes(data: CaseData) -> None:
    actual_fixes = _get_fixes(data.old_chunks, data.options)
    assert data.fixes == actual_fixes


def test_apply_fixes(data: CaseData) -> None:
    actual_new_lines = _apply_fixes(data.fixes, data.old_lines)
    assert data.new_lines == actual_new_lines


def test_fix_text(data: CaseData) -> None:
    actual_new_lines, actual_old_lines = fix_text(StringIO(data.old_text), data.options)
    assert actual_new_lines == data.new_lines
    assert actual_old_lines == data.old_lines


if __name__ == "__main__":
    pytest.main([__file__])
