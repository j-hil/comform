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
