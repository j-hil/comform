class CodeLine(str):
    """Representation of a line of code."""

    def __new__(cls, string) -> "CodeLine":
        self = super().__new__(cls, string)
        # TODO: this is too simplistic - adapt for strings with "#" in them and other
        # such cases
        self.comment_col = self.index("#") if "#" in self else None
        self.has_inline_comment = self.comment_col is not None
        return self

    def move_comment(self, new_col):
        old_col = self.comment_col
        if new_col < old_col:
            raise ValueError("Tried to move a comment backward. Naughty")
        prefix = self[:old_col]
        suffix = self[old_col:]
        return prefix + " " * (new_col - old_col) + suffix


def fix_align(code_lines: list[CodeLine]) -> None:

    batch = {}
    for n, code_line in enumerate(code_lines):
        if code_line.has_inline_comment:
            batch[n] = code_line
        elif batch:
            col = max(line.comment_col for line in batch.values())  # type: ignore
            for n, commented_code in batch.items():
                code_lines[n] = commented_code.move_comment(col)
            batch = {}


def main():
    with open(R".\tests\examples\bad_align.py") as fh:
        text_lines = fh.readlines()
    code_lines = [CodeLine(line) for line in text_lines]

    fix_align(code_lines)

    print(*code_lines)


if __name__ == "__main__":
    main()
