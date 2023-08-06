# sphinxext-mimic
![ci](https://github.com/wpilibsuite/sphinxext-mimic/workflows/ci/badge.svg)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Sphinx Extension to create a fake expandable table of contents. It is recommended to `:orphan:` any page where mimic is used to avoid any unexpected behavior.

## Installation

`python -m pip install sphinxext-mimic`

## Requirements

- Sphinx >= 3

## Usage
Add `sphinxext.mimic` to your extensions list in your `conf.py`

```python
extensions = [
   sphinxext.mimic,
]
```

Then use

```
.. mimictoc::
```

which is compatible with the default `.. toctree::` arguments.
