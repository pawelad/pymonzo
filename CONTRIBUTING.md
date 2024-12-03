# Contributing Guide
Welcome! If you'd like to contribute to `pymonzo`, you came to right place. Hopefully,
everything noteworthy is mentioned, but if you still have some questions after reading
it all, don't hesitate to open up a [new issue][github new issue].

Please also note that this project is released with a [Contributor Code of Conduct].
By participating in this project you agree to abide by its terms.

## Tools used
**Language:** [Python 3.9+][python]  
**CI:** [GitHub Actions]  
**Docs:** [mkdocs], [mkdocs-material], [mkdocstrings], [Read The Docs]  
**Testing:** [pytest], [nox]  
**Coverage:** [Coverage.py], [Codecov]  
**Type checks:** [mypy]  
**Code style:** [black], [isort], [ruff], [interrogate]  
**Other:** Makefile  

## Code style
All code is formatted with the amazing `black`, `isort` and `ruff` tools via
`make format` helper command.

## Tests
Tests are written with help of [pytest] and run via [nox] (alongside other checks).
To run the test suite yourself, all you need to do is run:

```console
$ # Install nox
$ python -m pip install nox
$ # Run nox
$ make test
```

## Makefile
Available `make` commands:

```console
$ make help
install                                   Install package in editable mode
format                                    Format code
test                                      Run the test suite
docs-build                                Build docs
docs-serve                                Serve docs
build                                     Build package
publish                                   Publish package
clean                                     Clean dev artifacts
help                                      Show help message
```


[black]: https://black.readthedocs.io/
[codecov]: https://codecov.io/
[contributor code of conduct]: ./.github/CODE_OF_CONDUCT.md
[coverage.py]: https://coverage.readthedocs.io
[github actions]: https://github.com/features/actions
[github new issue]: https://github.com/pawelad/pymonzo/issues/new/choose
[interrogate]: https://github.com/econchick/interrogate
[isort]: https://github.com/timothycrosley/isort
[mkdocs-material]: https://squidfunk.github.io/mkdocs-material/
[mkdocs]: https://www.mkdocs.org/
[mkdocstrings]: https://mkdocstrings.github.io/
[mypy]: https://mypy-lang.org/
[nox]: https://nox.readthedocs.io/
[pytest]: https://pytest.org/
[python]: https://www.python.org/
[read the docs]: https://readthedocs.com/
[ruff]: https://docs.astral.sh/ruff
