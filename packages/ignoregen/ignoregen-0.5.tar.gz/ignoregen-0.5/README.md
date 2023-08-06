# ignoregen by Richard Cook

[![View on PyPI](https://img.shields.io/pypi/v/ignoregen.svg)](https://pypi.python.org/pypi/ignoregen)
[![Licence](https://img.shields.io/badge/license-MIT-blue.svg)](https://raw.githubusercontent.com/rcook/ignoregen/master/LICENSE)

Python tool with virtual environment wrappers

## Typical usage

From a Linux/Unix-style shell:

```
ignoregen gen > ~/.git/info/exclude
```

From PowerShell

```
ignoregen gen | Out-File -Encoding ASCII -FilePath ~\.git\info\exclude
```

## Clone repository

```
git clone https://github.com/rcook/ignoregen.git
```

## Developer notes

Various package properties are defined in `ignoregen/__init__py`:

* `__project_name__`
* `__version__`
* `__description__`

When publishing a new build of the package, ensure that `__version__` is incremented as appropriate.

## Build and publish

```
cd /path/to/ignoregen
python setup.py sdist
twine upload dist/*
```

## Licence

Released under [MIT License][licence]

[licence]: LICENSE
[pypi]: https://pypi.python.org/pypi
