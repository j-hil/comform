import tokenize
from pathlib import Path
from tokenize import TokenInfo

COMMENT = 61


class CodeLine(str):
    """Representation of a line of code."""

    # NOTE: early declarations needed due to mypy issue. see:
    # https://github.com/python/mypy/issues/1021
    comment_col: int
    prefix: str
    comment: str
    has_inline_comment: bool
    has_own_line_comment: bool

    def __new__(cls, string: str) -> "CodeLine":
        self = super().__new__(cls, string)
        # TODO: this is too simplistic - adapt for strings with "#" in them and other
        # such cases. Perhaps use https://docs.python.org/3/library/tokenize.html
        # or similar

        # the logic surrounding `comment_col`, `prefix` and `comment` all rely on how
        # python handles indexing & slicing for too large indices
        self.comment_col = self.index("#") if "#" in self else len(self)
        self.prefix = self[: self.comment_col]
        self.comment = self[self.comment_col + 1 :]

        self.has_inline_comment = (self.prefix.strip() != "") and self.comment
        self.has_own_line_comment = (self.prefix.strip() == "") and self.comment

        return self

    def move_comment(self, new_col: int) -> "CodeLine":
        old_col = self.comment_col
        if new_col < old_col:
            raise ValueError("Tried to move a comment backward. Naughty")
        return CodeLine(self.prefix + " " * (new_col - old_col) + "#" + self.comment)


class CodeLine3:
    def __init__(self, text, comment_col) -> None:
        self._text = text
        # TODO: rename to hash_col or similar
        self._comment_col = comment_col

        self._prefix = self._text[: self._comment_col]
        # TODO: or self.comment.string?
        self._comment = self._text[self._comment_col + 1 :]

        # TODO: make these functions so they don't need to be updated.
        self.has_inline_comment = (self.prefix.strip() != "") and self.comment
        # TODO: rename to has_blocky_comment or similar
        self.has_own_line_comment = (self.prefix.strip() == "") and self.comment

    @property
    def text(self) -> str:
        return self._text

    @property
    def comment_col(self) -> int:
        return self._comment_col

    @comment_col.setter
    def comment_col(self, new_col: int) -> None:
        if new_col < self._comment_col:
            # NOTE: If you run `black` first I don't think it should ever be necessary.
            raise ValueError("Not allowing decreasing of comments, for now.")
        self._text = (
            self.prefix + " " * (new_col - self._comment_col) + "#" + self.comment
        )
        self._comment_col = new_col

    @property
    def prefix(self) -> str:
        return self._prefix

    @property
    def comment(self) -> str:
        return self._comment

    @comment.setter
    def comment(self, value: str) -> None:
        self._text = self._prefix + "#" + value
        self._comment = value

    def __repr__(self):
        return self.__class__.__qualname__ + f"({self._text!r})"


class CodeLines(list[CodeLine3]):
    def __init__(self, path: Path | str):
        self.path = Path(path)

        with tokenize.open(path) as fh:
            tokens = tokenize.generate_tokens(fh.readline)

            comment_token: TokenInfo | None = None
            for token in tokens:
                if token.type == COMMENT:
                    comment_token = token
                elif token.string == "\n":
                    comment_col = (
                        comment_token.start[1] if comment_token else len(token.line)
                    )
                    self.append(CodeLine3(token.line, comment_col))
                    comment_token = None


def main():

    path = Path(__file__).parent.parent.parent / "tests" / "examples" / "align_bad.py"
    code_lines = CodeLines(path)
    print("all lines:", *code_lines, sep="\n")
    # print(code_lines[6])


if __name__ == "__main__":
    main()
