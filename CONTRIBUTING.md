# Contributing Guide
Welcome! If you'd like to contribute to `pymonzo`, you came to right place. Hopefully,
everything noteworthy is mentioned, but if you still have some questions after reading
it all, don't hesitate to open up a [new issue][github new issue].

Please also note that this project is released with a [Contributor Code of Conduct].
By participating in this project you agree to abide by its terms.

## Tools used
**Language:** [Python 3.8+][python]  
**CI:** [GitHub Actions]  
**Testing:** [pytest], [nox]  
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
[contributor code of conduct]: ./.github/CODE_OF_CONDUCT.md
[github actions]: https://github.com/features/actions
[github new issue]: https://github.com/pawelad/pymonzo/issues/new/choose
[interrogate]: https://github.com/econchick/interrogate
[isort]: https://github.com/timothycrosley/isort
[nox]: https://nox.readthedocs.io/
[pytest]: https://pytest.org/
[python]: https://www.python.org/
[ruff]: https://github.com/charliermarsh/ruff
