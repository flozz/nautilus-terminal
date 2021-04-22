import os
import sys


EXTENSION_FILE = "nautilus_terminal_extension.py"
SYSTEM_EXTENSION_DIR = "/usr/share/nautilus-python/extensions"
CURRENT_USER_EXTENSION_DIR = os.path.expanduser(
    "~/.local/share/nautilus-python/extensions/"
)

GSETTINGS_SCHEMA_FILE = "org.flozz.nautilus-terminal.gschema.xml"
SYSTEM_GSETTINGS_SCHEMA_DIR = "/usr/share/glib-2.0/schemas"
GLIB_COMPILE_SCHEMA = "/usr/bin/glib-compile-schemas"


def is_system_extension_installed():
    return os.path.isfile(os.path.join(SYSTEM_EXTENSION_DIR, EXTENSION_FILE))


def is_user_extension_installed():
    return os.path.isfile(
        os.path.join(CURRENT_USER_EXTENSION_DIR, EXTENSION_FILE)
    )


def is_nautilus_python_installed():
    return os.path.isfile(
        "/usr/lib/x86_64-linux-gnu/nautilus/extensions-3.0/libnautilus-python.so"
    )


def is_glib_compile_schema_installed():
    return os.path.isfile(GLIB_COMPILE_SCHEMA)


def install_system():
    """Installs the Nautilus extension for a system-wide installation.

    .. WARNING::

       This must be run as root!
    """
    if os.getuid() != 0:
        print(
            "E: You must run nautilus-terminal as root to perform a system-wide installation."
        )
        sys.exit(2)
    pass


def uninstall_system():
    """Remove the Nautilus extension for a system-wide installation.

    .. WARNING::

       This must be run as root!
    """
    if os.getuid() != 0:
        print(
            "E: You must run nautilus-terminal as root to perform a system-wide uninstallation."
        )
        sys.exit(2)
    pass


def install_user():
    """Installs the Nautilus extension for the current user."""
    pass


def uninstall_user():
    """Remove the Nautilus extension for the current user."""
    pass
