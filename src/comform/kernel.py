import re
from pathlib import Path

from mdformat import text as format_as_md

from comform.codeline import CodeLine

COL_MAX = 88
COMMENT_PREFIX_LEN = len("# ")


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
    with open(R"\comform\temp.py", "w") as fh:
        fh.write(run_all(R".\tests\examples\bad_all.py"))


if __name__ == "__main__":
    _main()
