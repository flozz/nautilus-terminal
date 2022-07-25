import nox


PYTHON_FILES = [
    "nautilus_terminal",
    "noxfile.py",
    "setup.py",
]


@nox.session(reuse_venv=True)
def lint(session):
    session.install("flake8", "black")
    session.run("flake8", *PYTHON_FILES)
    session.run("black", "--check", "--diff", "--color", *PYTHON_FILES)


@nox.session(python=["3.7", "3.8", "3.9", "3.10"], reuse_venv=True)
def test(session):
    session.run(
        "python", "-m", "doctest", "./nautilus_terminal/color_helpers.py"
    )
