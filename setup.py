#!/usr/bin/env python
# encoding: UTF-8

import os
from setuptools import setup, find_packages
from setuptools.command.install import install as _install

from nautilus_terminal import VERSION


class install(_install):
    def run(self):
        _install.run(self)

        is_root_user = os.getuid() == 0
        is_system_install = bool(self.root) or is_root_user
        is_user_install = not is_system_install
        data_prefix = "%s%s/share" % (
            (self.root if self.root else ""),
            self.install_base,
        )

        print("Installation parameters:")
        print("  is_root_user: %s" % str(is_root_user))
        print("  is_system_install: %s" % str(is_system_install))
        print("  is_user_install: %s" % str(is_user_install))
        print("  data_prefix: %s" % data_prefix)

        if is_system_install:
            os.environ["XDG_DATA_DIR"] = data_prefix

            from nautilus_terminal.install_nautilus_extension import (
                install_system,
            )

            install_system()
        elif is_user_install:
            from nautilus_terminal.install_nautilus_extension import (
                install_user,
            )

            install_user()


long_description = ""
if os.path.isfile("README.rst"):
    long_description = open("README.rst", "r").read()


setup(
    name="nautilus_terminal",
    version=VERSION,
    description="A terminal embedded in Nautilus, the GNOME's file browser",
    url="https://github.com/flozz/nautilus-terminal",
    license="GPL-3.0",
    long_description=long_description,
    author="Fabien LOISON",
    keywords="nautilus extension terminal gnome",
    platforms=["Linux", "BSD"],
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "psutil>=5.6.6",
    ],
    extras_require={
        "dev": [
            "nox",
            "flake8",
            "black",
        ],
    },
    cmdclass={"install": install},
    entry_points={
        "console_scripts": [
            "nautilus-terminal = nautilus_terminal.__main__:main",
        ]
    },
)
