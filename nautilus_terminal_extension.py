# This file is a part of the Nautilus Temrinal package

import os
import sys

if "NAUTILUS_TERMINAL_DEBUG_PACKAGE_PATH" in os.environ:
    sys.path.insert(0, os.environ["NAUTILUS_TERMINAL_DEBUG_PACKAGE_PATH"])

if "NAUTILUS_TERMINAL_DEBUG" in os.environ:
    print("\x1B[1;34m#### Starting Nautilus Terminal [DEBUG] ####\x1B[0m")
    print("* PYTHON_PATH: %s" % ":".join(sys.path))
else:
    print("* Starting Nautilus Terminal")

from nautilus_terminal.crowbar import Crowbar as NautilusTerminalLocationWidgetProvider
