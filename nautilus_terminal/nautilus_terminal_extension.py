# This file is a part of the Nautilus Temrinal package

# This file is the Nautilus extension itself, it must be placed
# in one of the following folder to make allow the extension to work:
#
# * /usr/share/nautilus-python/extensions/
# * ~/.local/share/nautilus-python/extensions/

import os
import sys

from gi.repository import GObject, Nautilus


DEBUG = "NAUTILUS_TERMINAL_DEBUG_PACKAGE_PATH" in os.environ


if DEBUG:
    sys.path.insert(0, os.environ["NAUTILUS_TERMINAL_DEBUG_PACKAGE_PATH"])


from nautilus_terminal.crowbar import Crowbar  # noqa


if DEBUG:
    print("\x1B[1;34m#### Starting Nautilus Terminal [DEBUG] ####\x1B[0m")
    print("PYTHON_PATH: %s\n" % ":".join(sys.path))
else:
    print("* Starting Nautilus Terminal")


class NautilusTerminalLocationWidgetProvider(
    GObject.GObject, Nautilus.LocationWidgetProvider
):
    def get_widget(self, uri, window):
        return Crowbar(uri, window)
