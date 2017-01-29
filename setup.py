#!/usr/bin/env python
# encoding: UTF-8

import os
import shutil
from setuptools import setup, find_packages
from setuptools.command.install import install as _install

from nautilus_terminal import VERSION


NAUTILUS_PYTHON_EXTENSION_PATH = "/usr/share/nautilus-python/extensions"


class install(_install):
    def run(self):
        _install.run(self)
        print("Installing Nautilus Python extension...")
        if not os.path.isdir(NAUTILUS_PYTHON_EXTENSION_PATH):
            try:
                os.mkdir(NAUTILUS_PYTHON_EXTENSION_PATH)
            except OSError:
                print("WARNING: Nautilus Python extension have not been installed (%s cannot be created)" % NAUTILUS_PYTHON_EXTENSION_PATH)
                return
        try:
            shutil.copy("./nautilus_terminal/nautilus_terminal_extension.py", NAUTILUS_PYTHON_EXTENSION_PATH)
        except IOError:
            print("WARNING: Nautilus Python extension have not been installed (permission denied)")
            return
        print("Done!")


setup(
    name="nautilus_terminal",
    version=VERSION,
    description="A terminal embedded in Nautilus, the GNOME's file browser",
    url="https://github.com/flozz/nautilus-terminal",
    license="GPL-3.0",

    long_description=open("README.md").read(),

    author="Fabien LOISON",

    keywords="nautilus extension terminal gnome",
    platforms=["Linux", "BSD"],

    packages=find_packages(),

    cmdclass={"install": install}
)

