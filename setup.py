#!/usr/bin/env python
# encoding: UTF-8

import os
from setuptools import setup, find_packages
from setuptools.command.install import install as _install

from nautilus_terminal import VERSION
from nautilus_terminal.install_nautilus_extension import install_system
from nautilus_terminal.install_nautilus_extension import install_user


class install(_install):
    def run(self):
        _install.run(self)

        if os.getuid() == 0:
            install_system()
        else:
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
