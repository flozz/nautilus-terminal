import nox


@nox.session
def lint(session):
    session.install("flake8")
    session.run("flake8", "--ignore", "E241,E402,E501", "nautilus_terminal", "noxfile.py")


@nox.session(python=["3.6", "3.7", "3.8", "3.9"])
def test(session):
    session.run("python", "-m", "doctest", "./nautilus_terminal/color_helpers.py")
