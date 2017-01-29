# Nautilus Terminal 3

> A terminal embedded in Nautilus, the GNOME's file browser

**Nautilus Terminal** is a terminal embedded into Nautilus, the GNOME's file browser. It is always opened in the current folder, and follows the navigation (the `cd` command is automatically executed when you navigate to an other folder).

**NOTE:** This is a complete re-implementation of [my previous Nautilus Temrinal plugin][old-nterm].


## Hacking and Debug

If you want work on this software, you will first have to install the [nautilus-python][] package. On Debian / Ubuntu, you will find it in the `python-nautilus` package:

    sudo apt install python-nautilus

Then you have to copy the `nautilus_terminal_extension.py` file in the nautilus-python's extension folder (this script is just a minimal bootstrap that will import the `nautilus_terminal` module installed system wild or the one located in this repository if the right debug environment is set). This can be done by one of the script of the `tools/` folder:

    ./tools/update-locale-extention.sh

You can now hack Nautilus Terminal as you want and you can use the following script to test your code right into nautilus:

    ./tools/debug-in-nautilus.sh
    ./tools/debug-in-nautilus.sh --no-bg  # keep nautilus attached to the console

Happy hacking! :)


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
