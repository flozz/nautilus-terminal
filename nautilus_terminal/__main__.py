import sys
import argparse

from .debug import get_debug_info
from .install_nautilus_extension import is_system_extension_installed
from .install_nautilus_extension import is_user_extension_installed
from .install_nautilus_extension import is_nautilus_python_installed


_EPILOG = """
Please report any bug on Github: https://github.com/flozz/nautilus-terminal/issues
"""


class PrintDebugAction(argparse.Action):
    """Prints debug informations and exit."""

    def __call__(self, parser, namespace, value, option_string=None):
        print(get_debug_info())
        sys.exit(0)


class CheckExtensionAction(argparse.Action):
    """Check if the Nautilus extension is properly installed and exit."""

    def __call__(self, parser, namespace, value, option_string=None):
        if os.getuid() == 0:
            print(
                "E: You must run nautilus-terminal as regular user to perform an installation check."
            )
            sys.exit(1)

        result = ""
        retcode = 0

        result += "\x1B[1mNautilus Python:\x1B[0m "
        if is_nautilus_python_installed():
            result += "\x1B[1;32mInstalled\x1B[0m\n"
        else:
            retcode = 1
            result += "\x1B[1;31mAbsent\x1B[0m\n"
            result += "    Please install Nautilus Python. Please read the documentation:\n"
            result += "    https://github.com/flozz/nautilus-terminal\n"

        result += "\x1B[1mNautilus Terminal Extension:\x1B[0m "
        if (
            is_system_extension_installed()
            and not is_user_extension_installed()
        ) or (
            is_user_extension_installed()
            and not is_system_extension_installed()
        ):
            result += "\x1B[1;32mInstalled\x1B[0m\n"
        elif is_system_extension_installed() and is_user_extension_installed():
            retcode = 1
            result += "\x1B[1;31mError\x1B[0m\n"
            result += "    Nautilus Terminal extension is installed twice...\n"
            result += "    Please remove one of the installed extentions using one of the following commands:\n"
            result += "    \x1B[1;34mSystem-wide:\x1B[0m sudo nautilus-terminal --uninstall-system\n"
            result += "    \x1B[1;34mCurrent user:\x1B[0m nautilus-terminal --uninstall-user\n"
        else:
            retcode = 1
            result += "\x1B[1;31mAbsent\x1B[0m\n"
            result += "    Please install the Nautilus Extension with one of the following commands:\n"
            result += "    \x1B[1;34mSystem-wide:\x1B[0m sudo nautilus-terminal --install-system\n"
            result += "    \x1B[1;34mCurrent user:\x1B[0m nautilus-terminal --install-user\n"

        print(result)
        sys.exit(retcode)


def main(args=sys.argv[1:]):
    cli_parser = argparse.ArgumentParser(
        prog="nautilus-terminal",
        epilog=_EPILOG,
    )

    cli_parser.add_argument(
        "--print-debug",
        help="Prints debug informations and exit",
        nargs=0,
        action=PrintDebugAction,
    )

    cli_parser.add_argument(
        "--check-extension",
        help="Check if the Nautilus extension is properly installed and exit",
        nargs=0,
        action=CheckExtensionAction,
    )

    if len(args) == 0:
        cli_parser.parse_args(["--help"])
    else:
        cli_parser.parse_args(args)


if __name__ == "__main__":
    main()
