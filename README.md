# Nautilus Terminal 3

[![PYPI Version](https://img.shields.io/pypi/v/nautilus_terminal.svg)](https://pypi.python.org/pypi/nautilus_terminal)
[![License](https://img.shields.io/pypi/l/nautilus_terminal.svg)](https://github.com/flozz/nautilus-terminal/blob/master/COPYING)

> A terminal embedded in Nautilus, the GNOME's file browser

**Nautilus Terminal** is a terminal embedded into Nautilus, the GNOME's file browser. It is always opened in the current folder, and follows the navigation (the `cd` command is automatically executed when you navigate to an other folder).

**NOTE:** This is a complete re-implementation of [my previous Nautilus Temrinal plugin][old-nterm].

**NOTE²:** This is an early development version, some feature are missing (see below).

**Features:**

* Embed a Terminal in each Nautilus tab / window,
* Follow the navigation: if you navigate in Nautilus, the `cd` command is automatically executed in the terminal,
* Detects running process: if something is running in the terminal, the `cd` command is not send to the shell,
* Automatically respawn the shell if it exits,
* Supports copy / paste from / to the terminal using `Ctrl+Shift+C` / `Ctrl+Shift+V`,
* Can be displayed / hidden using the `F4` key,
* ~~Supports drag & drop of file on the terminal,~~ **TODO**
* ~~Allows to configure the shell~~ **TODO** (actually it is hardcoded to `/bin/zsh`),
* ~~Allows to configure the terminal appearance (colors, font,...).~~ **TODO**

**Requirements:**

* [nautilus-python][]
* [psutil][]

![Nautilus Temrinal Screenshot](./screenshot.png)


## Installing Nautilus Terminal

### From PYPI

Run the following command (as root):

    pip install nautilus_terminal

Then kill Nautilus to allow it to load the new extension:

    nautilus -q

### From sources

Clone the repositiory:

    git clone git@github.com:flozz/nautilus-terminal.git
    cd nautilus-terminal

Install Nautilus Terminal (as root):

    python setup.py install

Then kill Nautilus to allow it to load the new extension:

    nautilus -q

**NOTE:** if the setup fails to install the Nautilus Python extension script, you can copy it manually (as root):

    cp nautilus_terminal/nautilus_terminal_extension.py /usr/share/nautilus-python/extensions/


## Hacking and Debug

If you want work on this software, you will first have to install the [nautilus-python][] and [psutil][] packages. On Debian / Ubuntu, you will find it in the `python-nautilus` and `python-psutil` packages:

    sudo apt install python-nautilus python-psutil

Then you have to copy the `nautilus_terminal_extension.py` file in the nautilus-python's extension folder (this script is just a minimal bootstrap that will import the `nautilus_terminal` module installed system wild or the one located in this repository if the right debug environment is set). This can be done by one of the script of the `tools/` folder:

    ./tools/update-locale-extention.sh

You can now hack Nautilus Terminal as you want and you can use the following script to test your code right into nautilus:

    ./tools/debug-in-nautilus.sh
    ./tools/debug-in-nautilus.sh --no-bg  # keep Nautilus attached to the console

Happy hacking! :)


## Changelog

* **3.0.1:** Script to convert the README to reStructuredText for PYPI
* **3.0.0:** Initial Nautilus Temrinal 3 release (early development version)


## License GPLv3

    Nautilus Terminal - A terminal embedded in the Nautilus file browser
    Copyright (C) 2010-2017  Fabien LOISON <http://www.flozz.fr/>

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.


[old-nterm]: https://launchpad.net/nautilus-terminal
[nautilus-python]: https://wiki.gnome.org/Projects/NautilusPython/
[psutil]: https://pypi.python.org/pypi/psutil/
