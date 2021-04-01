import os


DEBUG = "NAUTILUS_TERMINAL_DEBUG" in os.environ


def log(*args):
    if not DEBUG:
        return
    print(
        "\x1B[1;34m[Nautilus Terminal]\x1B[36m[ LOG]\x1B[0m %s"
        % " ".join([str(item) for item in args])
    )


def warn(*args):
    if not DEBUG:
        return
    print(
        "\x1B[1;34m[Nautilus Terminal]\x1B[33m[WARN]\x1B[0m %s"
        % " ".join([str(item) for item in args])
    )


def error(*args):
    if not DEBUG:
        return
    print(
        "\x1B[1;34m[Nautilus Terminal]\x1B[31m[ ERR]\x1B[0m %s"
        % " ".join([str(item) for item in args])
    )
