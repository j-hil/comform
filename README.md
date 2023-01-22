# ComForm: Python Comment Conformity Formatter

[![code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)

An auto-formatter for pretty and readable comment formatting in python.

WARNING: `comform` is made for my own usage; it has minimal testing, compatibility, and
consideration of edge cases. Use it on your own code at peril `;)`.

Block comments (the only type formatted by default) are formatted as if they were
markdown text using the fantastic
[`mdformat`](https://github.com/executablebooks/mdformat) package. Treating comments as
markdown has drawbacks, but I've found these to be overwhelmingly outweighed.

## Usage

This package can be installed from PyPI as usual via `pip install comform` and is meant
to be used as a command line tool. It can also be used as a `pre-commit` hook, but only
with a local copy installed (known issue, see
[here](https://github.com/j-hil/comform/issues/2)). However `comform` is used I
recommend running `black` first; it was developed for this use-case.

The interface is:

```ps1
comform [-h] [--version] [--check] [--align] [--dividers] [--wrap N] paths [paths ...]
```

## Development

Too see my development process see [development.md](./docs/development.md).
