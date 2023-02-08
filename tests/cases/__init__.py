from __future__ import annotations

from dataclasses import dataclass
from io import StringIO

from comform.cli import FormatOptions
from comform.comments import Chunk, Comment


@dataclass
class CaseData:
    test_case_name: str

    options: FormatOptions
    old_text: str
    old_comments: list[Comment]
    old_chunks: list[Chunk]
    new_chunks: list[Chunk]
    new_text: str

    def __post_init__(self) -> None:
        self.old_lines = StringIO(self.old_text).readlines()
        self.new_lines = StringIO(self.new_text).readlines()
        self.fixes = list(zip(self.old_chunks, self.new_chunks))
