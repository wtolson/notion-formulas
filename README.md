# Notion Formulas

[![Build][badge-build]][build]
[![MIT License][badge-license]][MIT]
[![Version][badge-version]][PyPI]
[![Python Version][badge-python]][PyPI]

Notion Formulas is a Python library designed for composing and manipulating complex formulas for Notion programmatically. Enhance your Notion workspace by leveraging the power of Python to create and manage formulas.

## Installation

To get started with Notion Formulas, you can install the package using [pip][pip]:

```bash
pip install notion-formulas
```

## Usage

```python
from notion_formulas import Number, prop

x: Number = prop("x")
y: Number = prop("y")

print(x + y)  # Prints `prop("x") + prop("y")`
```

## API

The complete Notion Formulas API maintains consistency with the original names, with the following adjustments:

- Camel casing is converted to snake case (e.g., `replaceAll()` becomes `replace_all()`).
- Functions matching python keywords are modified with a trailing underscore: (i.g. `if()` becomes `if_()`).
- Constants are uppercased (i.g. `e` becomes `E`).

## Data types

The api is fully typed and defines following data types for expressions: `Boolean`, `Number`, `String`, and `Date`, allowing your formulas to be typed checked by [mypy][mypy].

## Examples

For a comprehensive example, refer to the code that generates a Taskwarrior style [urgency score][urgency-score] for a Notion task database in [examples/urgency.py](examples/urgency.py) and the associated output [examples/urgency.txt](examples/urgency.txt).

## Contributing

Contributions to Notion Formulas are welcome and appreciated. If you'd like to contribute, please follow these steps:

1. Fork the repository.
2. Create a new branch for your changes.
3. Make your changes and update the tests as needed.
4. Submit a pull request with your changes.

For major changes, please open an issue first to discuss what you would like to change.

## License

Notion Formulas is released under the [MIT][MIT] license, which allows for free and open use, modification, and distribution.


[badge-build]: https://img.shields.io/github/actions/workflow/status/wtolson/notion-formulas/test.yml
[badge-license]: https://img.shields.io/badge/license-MIT-green
[badge-python]: https://img.shields.io/pypi/pyversions/notion-formulas
[badge-version]: https://img.shields.io/pypi/v/notion-formulas
[build]: https://github.com/wtolson/notion-formulas/actions/workflows/test.yml
[MIT]: https://choosealicense.com/licenses/mit/
[mypy]: https://www.mypy-lang.org/
[pip]: https://pip.pypa.io/en/stable/
[PyPI]: https://pypi.org/project/notion-formulas/
[urgency-score]: https://taskwarrior.org/docs/urgency/
