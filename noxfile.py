"""pymonzo Nox sessions."""
import nox

nox.options.reuse_existing_virtualenvs = True
nox.options.error_on_external_run = True

DEFAULT_PATHS = ["src/", "tests/", "noxfile.py"]


@nox.session(python=["3.8", "3.9", "3.10", "3.11", "3.12"])
def tests(session: nox.Session) -> None:
    """Run tests."""
    dirs = session.posargs or ["tests/"]

    session.install(".[tests]")

    session.run("coverage", "run", "-m", "pytest", *dirs)

    session.notify("coverage_report")


@nox.session()
def coverage_report(session: nox.Session) -> None:
    """Report test coverage. Can only be run after `tests` session."""
    session.install("coverage[toml]")

    session.run("coverage", "combine")
    session.run("coverage", "report")


@nox.session()
def docs(session: nox.Session) -> None:
    """Build docs."""
    session.install(".[docs]")

    session.run("mkdocs", "build", "--strict")


@nox.session()
def code_style_checks(session: nox.Session) -> None:
    """Check code style."""
    dirs = session.posargs or DEFAULT_PATHS

    session.install("black", "isort", "ruff", "interrogate")

    session.run("black", "--check", "--diff", *dirs)
    session.run("isort", "--check", "--diff", *dirs)
    session.run("ruff", "check", "--diff", *dirs)
    session.run("interrogate", *dirs)


@nox.session()
def type_checks(session: nox.Session) -> None:
    """Run type checks."""
    dirs = session.posargs or DEFAULT_PATHS

    session.install(".[dev]")

    session.run("mypy", *dirs)
