import sys
import os.path
import platform

from . import VERSION
from .install_nautilus_extension import is_system_extension_installed
from .install_nautilus_extension import is_user_extension_installed
from .install_nautilus_extension import is_nautilus_python_installed
from .install_nautilus_extension import is_glib_compile_schema_installed


def _make_title(text):
    separator = "=" * len(text)
    return "\n%s\n%s\n" % (text.upper(), separator)


def _get_os_info():
    result = _make_title("Operating System")
    if platform.system() == "Linux":
        result += _get_os_linux_info()
    else:
        result += "OS: %s" % platform.system()
    return result


def _get_os_linux_info():
    result = ""
    result += "OS: %s\n" % platform.system()
    result += "Platform: %s\n" % platform.platform()
    result += "Version: %s\n" % platform.version()
    if os.path.isfile("/etc/issue"):
        try:
            with open("/etc/issue", "r") as distro_file:
                distro = distro_file.read().strip()
                result += "Distribution issue: %s\n" % distro
        except Exception:
            pass
    return result


def _get_nautilus_terminal_info():
    result = _make_title("Nautilus Terminal")
    result += "Version: %s\n" % VERSION
    result += "System-wide extension: %s\n" % (
        "Installed" if is_system_extension_installed() else "Absent"
    )
    result += "Current user extension: %s\n" % (
        "Installed" if is_user_extension_installed() else "Absent"
    )
    result += "Installation path: %s\n" % os.path.dirname(
        os.path.abspath(__file__)
    )
    return result


def _get_python_info():
    result = _make_title("Python")
    result += "Python version: %d.%d.%d\n" % sys.version_info[:3]
    return result


def _get_system_dependencies_info():
    result = _make_title("System Dependencies")
    result += "Nautilus Python: %s\n" % (
        "Installed" if is_nautilus_python_installed() else "Absent"
    )
    result += "GLib schemas compiler: %s\n" % (
        "Installed" if is_glib_compile_schema_installed() else "Absent"
    )
    return result


def get_debug_info():
    result = ""
    result += _get_nautilus_terminal_info()
    result += _get_os_info()
    result += _get_python_info()
    result += _get_system_dependencies_info()
    return result
