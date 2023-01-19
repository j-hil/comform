import re
import tokenize
from pathlib import Path
from token import COMMENT
from tokenize import TokenInfo

from mdformat import text as format_as_md

from comform.codeline import CodeLine, CodeLine3, CodeLines

COL_MAX = 88
COMMENT_PREFIX_LEN = len("# ")


def fix_align(code_lines: CodeLines) -> None:

    batch: dict[int, CodeLine3] = {}
    for n, code_line in enumerate(code_lines):
        if code_line.has_inline_comment:
            batch[n] = code_line
        elif batch:
            col = max(line._comment_col for line in batch.values())
            for m, commented_code in batch.items():
                commented_code.comment_col = col
            batch = {}


def fix_blocks(code_lines: list[CodeLine]) -> None:
    batch: list[CodeLine] = []

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
            text = format_as_md(
                text,
                options={"number": True, "wrap": COL_MAX - col - COMMENT_PREFIX_LEN},
            ).strip()
            new_lines = [
                CodeLine(" " * col + "# " + l + "\n") if l else CodeLine("#\n")
                for l in text.split("\n")
            ]

            a, b = batch_start_n, batch_start_n + len(batch)
            code_lines[a:b] = new_lines
            n = batch_start_n + len(new_lines)
            batch = []

        n += 1


def fix_dividers(code_lines: list[CodeLine]) -> None:

    for n, line in enumerate(code_lines):
        match = re.match(r"^# -+ (.+) -+ #", line)
        if match:
            prefix = "# --"
            text = format_as_md(match.group(1), options={"wrap": "no"}).strip()
            suffix = "- #"
            dashes = "-" * (
                COL_MAX - len(prefix) - len(text) - len(suffix) - COMMENT_PREFIX_LEN
            )
            code_lines[n] = CodeLine(prefix + f" {text} " + dashes + suffix + "\n")


def run_all(filename: str | Path) -> str:

    with open(filename) as fh:
        text_lines = fh.readlines()
    code_lines = [CodeLine(line) for line in text_lines]

    fix_dividers(code_lines)
    fix_blocks(code_lines)
    fix_align(code_lines)

    return "".join(code_lines)


def _main() -> None:
    path = Path(__file__).parent.parent.parent / "tests" / "examples" / "align_bad.py"
    with tokenize.open(path) as fh:
        tokens = tokenize.generate_tokens(fh.readline)

        code_lines: list[list[TokenInfo]] = []
        comment_token: TokenInfo | None = None

        for token in tokens:
            if token.type == COMMENT:
                comment_token = token
            elif token.string == "\n":
                comment_col = (
                    comment_token.start[1] if comment_token else len(token.line)
                )
                code_lines.append(CodeLine3(token.line, comment_col))
                comment_token = None

    print("all lines:", *code_lines, sep="\n")
    # print(code_lines[6])

    fix_align(code_lines)
    print("post:", *code_lines, sep="\n")


if __name__ == "__main__":
    _main()
