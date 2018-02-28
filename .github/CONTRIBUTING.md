# Contributing
First of all - thanks for contributing (or thinking about it)! Honestly, that's
really nice of you - there's a lot of other, _way_ more fun things you could've
been doing instead so thank you : -)

This document is mainly to help you to get started by codifying tribal
knowledge and expectations and make it more accessible to everyone. But don't
be afraid to open half-finished PRs and ask questions if something is unclear!

Please also note that this project is released with a
[Contributor Code of Conduct][code of conduct]. By participating in this
project you agree to abide by its terms.

## Main guidelines
- No contribution is too small! Please submit as many fixes for typos and
  grammar bloopers as you can!
- Try to limit each pull request to one change only.
- Always add tests and docstrings for your code.
- Make sure your changes pass our CI.
- Remember to add a changelog entry that sums up what you did.

## Code style
- When in doubt, default to [PEP 8][pep8], [PEP 257][pep257] and
  [Django code style guide][django code style] (when applicable).
- Use [reST style docstring format][docstring format].

---

This document was loosely based on [attrs contributing guide][attrs contributing guide]
by [Hynek Schlawack][hynek].


[attrs contributing guide]: https://github.com/python-attrs/attrs/blob/master/.github/CONTRIBUTING.rst
[code of conduct]: https://github.com/pawelad/pymonzo/blob/master/.github/CODE_OF_CONDUCT.md
[django code style]: https://docs.djangoproject.com/en/dev/internals/contributing/writing-code/coding-style/
[docstring format]: https://thomas-cokelaer.info/tutorials/sphinx/docstring_python.html
[hynek]: https://hynek.me/about/
[pep257]:  https://www.python.org/dev/peps/pep-0257/
[pep8]: https://www.python.org/dev/peps/pep-0008/
[pyenv]: https://github.com/pyenv/pyenv
[tox]: https://tox.readthedocs.io/
