import os
import shutil

ROOT = os.path.abspath(os.path.dirname(__file__))

EXTENSION_FILE = "nautilus_terminal_extension.py"
SYSTEM_EXTENSION_DIR = "/usr/share/nautilus-python/extensions"
CURRENT_USER_EXTENSION_DIR = os.path.expanduser(
    "~/.local/share/nautilus-python/extensions/"
)

GSETTINGS_SCHEMA_FILE = "org.flozz.nautilus-terminal.gschema.xml"
SYSTEM_GSETTINGS_SCHEMA_DIR = "/usr/share/glib-2.0/schemas"
GLIB_COMPILE_SCHEMA = "/usr/bin/glib-compile-schemas"


def is_system_extension_installed():
    return os.path.isfile(
        os.path.join(SYSTEM_EXTENSION_DIR, EXTENSION_FILE)
    ) or os.path.isfile(
        os.path.join(SYSTEM_EXTENSION_DIR, EXTENSION_FILE + "c")  # .pyc
    )


def is_user_extension_installed():
    return os.path.isfile(
        os.path.join(CURRENT_USER_EXTENSION_DIR, EXTENSION_FILE)
    ) or os.path.isfile(
        os.path.join(CURRENT_USER_EXTENSION_DIR, EXTENSION_FILE + "c")  # .pyc
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
    if not os.path.isdir(SYSTEM_EXTENSION_DIR):
        os.makedirs(SYSTEM_EXTENSION_DIR)
    shutil.copy(
        os.path.join(ROOT, EXTENSION_FILE),
        os.path.join(SYSTEM_EXTENSION_DIR, EXTENSION_FILE),
    )
    print("Nautilus Terminal extension successfully installed on the system.")


def uninstall_system():
    """Remove the Nautilus extension for a system-wide installation.

    .. WARNING::

       This must be run as root!
    """
    files = [
        os.path.join(SYSTEM_EXTENSION_DIR, EXTENSION_FILE),
        os.path.join(SYSTEM_EXTENSION_DIR, EXTENSION_FILE + "c"),  # .pyc
    ]
    for file_ in files:
        if os.path.isfile(file_):
            os.remove(file_)
    print(
        "Nautilus Terminal extension successfully uninstalled from the system."
    )


def install_user():
    """Installs the Nautilus extension for the current user.

    .. WARNING::

       This must be run as a regular user!
    """
    if not os.path.isdir(CURRENT_USER_EXTENSION_DIR):
        os.makedirs(SYSTEM_EXTENSION_DIR)
    shutil.copy(
        os.path.join(ROOT, EXTENSION_FILE),
        os.path.join(SYSTEM_EXTENSION_DIR, EXTENSION_FILE),
    )
    print(
        "Nautilus Terminal extension successfully installed on the current user."
    )


def uninstall_user():
    """Remove the Nautilus extension for the current user.

    .. WARNING::

       This must be run as a regular user!
    """
    files = [
        os.path.join(CURRENT_USER_EXTENSION_DIR, EXTENSION_FILE),
        os.path.join(CURRENT_USER_EXTENSION_DIR, EXTENSION_FILE + "c"),  # .pyc
    ]
    for file_ in files:
        if os.path.isfile(file_):
            os.remove(file_)
    print(
        "Nautilus Terminal extension successfully uninstalled from the current user."
    )
