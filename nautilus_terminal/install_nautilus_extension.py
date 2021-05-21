import os
import shutil
import subprocess


XDG_DATA_DIR = os.environ.get("XDG_DATA_DIR", "/usr/share")
XDG_DATA_HOME = os.environ.get(
    "XDG_DATA_HOME", os.path.expanduser("~/.local/share")
)
ROOT = os.path.abspath(os.path.dirname(__file__))

EXTENSION_FILE = "nautilus_terminal_extension.py"
SYSTEM_EXTENSION_DIR = os.path.join(XDG_DATA_DIR, "nautilus-python/extensions")
USER_EXTENSION_DIR = os.path.join(XDG_DATA_HOME, "nautilus-python/extensions")

GLIB_SCHEMA_FILE = "org.flozz.nautilus-terminal.gschema.xml"
GLIB_SCHEMA_SOURCE = os.path.join(ROOT, "schemas", GLIB_SCHEMA_FILE)
SYSTEM_GLIB_SCHEMA_DIR = os.path.join(XDG_DATA_DIR, "glib-2.0/schemas")
USER_GLIB_SCHEMA_DIR = os.path.join(XDG_DATA_HOME, "glib-2.0/schemas")
GLIB_COMPILE_SCHEMA = "/usr/bin/glib-compile-schemas"


def is_packaged():
    return not os.path.isfile(os.path.join(ROOT, "not_packaged.py"))


def is_system_extension_installed():
    return os.path.isfile(
        os.path.join(SYSTEM_EXTENSION_DIR, EXTENSION_FILE)
    ) or os.path.isfile(
        os.path.join(SYSTEM_EXTENSION_DIR, EXTENSION_FILE + "c")  # .pyc
    )


def is_user_extension_installed():
    return os.path.isfile(
        os.path.join(USER_EXTENSION_DIR, EXTENSION_FILE)
    ) or os.path.isfile(
        os.path.join(USER_EXTENSION_DIR, EXTENSION_FILE + "c")  # .pyc
    )


def is_nautilus_python_installed():
    paths = [
        "/usr/lib/nautilus/extensions-3.0/libnautilus-python.so",
        "/usr/lib64/nautilus/extensions-3.0/libnautilus-python.so",
        "/usr/lib/x86_64-linux-gnu/nautilus/extensions-3.0/libnautilus-python.so",
    ]

    for path in paths:
        if os.path.isfile(path):
            return True

    return False


def is_glib_compile_schema_installed():
    return os.path.isfile(GLIB_COMPILE_SCHEMA)


def install_system():
    """Installs the Nautilus extension for a system-wide installation.

    .. WARNING::

       This must be run as root!
    """
    # Copy extension
    if not os.path.isdir(SYSTEM_EXTENSION_DIR):
        os.makedirs(SYSTEM_EXTENSION_DIR)
    shutil.copy(
        os.path.join(ROOT, EXTENSION_FILE),
        os.path.join(SYSTEM_EXTENSION_DIR, EXTENSION_FILE),
    )
    # Copy schemas
    if not os.path.isdir(SYSTEM_GLIB_SCHEMA_DIR):
        os.makedirs(SYSTEM_GLIB_SCHEMA_DIR)
    shutil.copy(
        GLIB_SCHEMA_SOURCE,
        os.path.join(SYSTEM_GLIB_SCHEMA_DIR, GLIB_SCHEMA_FILE),
    )
    # Compile schemas
    if is_glib_compile_schema_installed():
        subprocess.call([GLIB_COMPILE_SCHEMA, SYSTEM_GLIB_SCHEMA_DIR])
        print("GLib schema successfully compiled.")
    else:
        print(
            "GLib schema cannot be compiled. Please install GLib schema compiler and run the following command (as root):"
        )
        print(" ".join([GLIB_COMPILE_SCHEMA, SYSTEM_GLIB_SCHEMA_DIR]))
    #
    print("Nautilus Terminal extension successfully installed on the system.")


def uninstall_system():
    """Remove the Nautilus extension for a system-wide installation.

    .. WARNING::

       This must be run as root!
    """
    files = [
        os.path.join(SYSTEM_EXTENSION_DIR, EXTENSION_FILE),
        os.path.join(SYSTEM_EXTENSION_DIR, EXTENSION_FILE + "c"),  # .pyc
        os.path.join(SYSTEM_GLIB_SCHEMA_DIR, GLIB_SCHEMA_FILE),
    ]
    for file_ in files:
        if os.path.isfile(file_):
            os.remove(file_)
    if is_glib_compile_schema_installed():
        try:
            subprocess.call([GLIB_COMPILE_SCHEMA, SYSTEM_GLIB_SCHEMA_DIR])
        except Exception:
            print("An error occured while trying to recompile glib schemas")
    print(
        "Nautilus Terminal extension successfully uninstalled from the system."
    )


def install_user():
    """Installs the Nautilus extension for the current user.

    .. WARNING::

       This must be run as a regular user!
    """
    # Copy extension
    if not os.path.isdir(USER_EXTENSION_DIR):
        os.makedirs(USER_EXTENSION_DIR)
    shutil.copy(
        os.path.join(ROOT, EXTENSION_FILE),
        os.path.join(USER_EXTENSION_DIR, EXTENSION_FILE),
    )
    # Copy schemas
    if not os.path.isdir(USER_GLIB_SCHEMA_DIR):
        os.makedirs(USER_GLIB_SCHEMA_DIR)
    shutil.copy(
        GLIB_SCHEMA_SOURCE,
        os.path.join(USER_GLIB_SCHEMA_DIR, GLIB_SCHEMA_FILE),
    )
    # Compile schemas
    if is_glib_compile_schema_installed():
        subprocess.call([GLIB_COMPILE_SCHEMA, USER_GLIB_SCHEMA_DIR])
        print("GLib schema successfully compiled.")
    else:
        print(
            "GLib schema cannot be compiled. Please install GLib schema compiler and run the following command:"
        )
        print(" ".join([GLIB_COMPILE_SCHEMA, USER_GLIB_SCHEMA_DIR]))
    #
    print(
        "Nautilus Terminal extension successfully installed on the current user."
    )


def uninstall_user():
    """Remove the Nautilus extension for the current user.

    .. WARNING::

       This must be run as a regular user!
    """
    files = [
        os.path.join(USER_EXTENSION_DIR, EXTENSION_FILE),
        os.path.join(USER_EXTENSION_DIR, EXTENSION_FILE + "c"),  # .pyc
        os.path.join(USER_GLIB_SCHEMA_DIR, GLIB_SCHEMA_FILE),
    ]
    for file_ in files:
        if os.path.isfile(file_):
            os.remove(file_)
    if is_glib_compile_schema_installed():
        try:
            subprocess.call([GLIB_COMPILE_SCHEMA, USER_GLIB_SCHEMA_DIR])
        except Exception:
            print("An error occured while trying to recompile glib schemas")
    print(
        "Nautilus Terminal extension successfully uninstalled from the current user."
    )
