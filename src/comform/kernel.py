import re

import mdformat

COL_MAX = 88


class CodeLine(str):
    """Representation of a line of code."""

    def __new__(cls, string) -> "CodeLine":
        self = super().__new__(cls, string)
        # TODO: this is too simplistic - adapt for strings with "#" in them and other
        # such cases. Perhaps use https://docs.python.org/3/library/tokenize.html
        # or similar
        self.comment_col = self.index("#") if "#" in self else -1
        self.prefix = self[: self.comment_col]
        self.comment = self[self.comment_col + 1 :]
        self.has_inline_comment = (self.comment_col > 0) and (self.prefix.strip() != "")
        self.has_own_line_comment = (self.comment_col == 0) and (
            self.prefix.strip() == ""
        )
        return self

    def move_comment(self, new_col):
        old_col = self.comment_col
        if new_col < old_col:
            raise ValueError("Tried to move a comment backward. Naughty")
        return self.prefix + " " * (new_col - old_col) + "#" + self.comment


def fix_align(code_lines: list[CodeLine]) -> None:

    batch = {}
    for n, code_line in enumerate(code_lines):
        if code_line.has_inline_comment:
            batch[n] = code_line
        elif batch:
            col = max(line.comment_col for line in batch.values())
            for n, commented_code in batch.items():
                code_lines[n] = commented_code.move_comment(col)
            batch = {}


def fix_blocks(code_lines: list[CodeLine]) -> None:
    batch = []

    n = 0
    while n < len(code_lines):
        code_line = code_lines[n]

        if code_line.has_own_line_comment:

            if not batch:
                batch_start_n = n
            batch.append(code_line)
        elif batch:
            col = batch[0].comment_col
            text = "".join(line.comment for line in batch)
            text = mdformat.text(text, options={"number": True, "wrap": COL_MAX - col})
            new_lines = text.split("\n")
            new_lines = ["# " + l + "\n" if l else "#\n" for l in new_lines]

            a, b = batch_start_n, batch_start_n + len(batch)
            code_lines[a:b] = new_lines
            n = batch_start_n + len(new_lines)
            batch = []

        n += 1


def fix_sections(code_lines: list[CodeLine]):

    for n, line in enumerate(code_lines):
        match = re.match(r"^# -+ (.+) -+ #", line)
        if match:
            prefix = "# --"
            text = mdformat.text(match.group(1), options={"wrap": "no"}).strip()
            suffix = "- #"
            dashes = "-" * (COL_MAX - len(prefix) - len(text) - len(suffix))
            code_lines[n] = prefix + f" {text} " + dashes + suffix + "\n"


def main():
    with open(R".\tests\examples\bad_sections.py") as fh:
        text_lines = fh.readlines()
    code_lines = [CodeLine(line) for line in text_lines]

    fix_sections(code_lines)
    print(*code_lines, sep="")


if __name__ == "__main__":
    main()
