# Installation

`multinets` needs Python 3.9 or newer. It depends on
[igraph](https://python.igraph.org) and [numpy](https://numpy.org), which pip
installs with it:

```bash
pip install multinets
```

Optional extras add support for other libraries:

```bash
pip install "multinets[networkx]"  # use networkx graphs
pip install "multinets[plot]"      # plot with igraph.plot() and matplotlib
```

## Development version

To work on `multinets` itself, install it from a clone of the repository in
editable mode, with the test dependencies:

```bash
git clone https://github.com/neylsoncrepalde/multinets-py
cd multinets-py
python -m venv .venv
.venv/bin/pip install -e ".[test]"
.venv/bin/python -m pytest
```

To build this documentation:

```bash
.venv/bin/pip install -e ".[docs]"
.venv/bin/sphinx-build -W --keep-going -d docs/_build/doctrees docs docs/_build/html
```

Then open `docs/_build/html/index.html`.
