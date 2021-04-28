Nautilus Terminal 3
===================

|Lint / Tests| |PYPI Version| |License| |Discord| |Black|

   A terminal embedded in Nautilus, the GNOME’s file browser

**Nautilus Terminal** is a terminal embedded into Nautilus, the GNOME’s
file browser. It is always opened in the current folder, and follows the
navigation (the ``cd`` command is automatically executed when you
navigate to another folder).

**NOTE:** This is a complete re-implementation of `my previous Nautilus
Terminal plugin <https://launchpad.net/nautilus-terminal>`__.

.. figure:: https://raw.githubusercontent.com/flozz/nautilus-terminal/master/screenshot.png
   :alt: Nautilus Terminal Screenshot

Main Features
-------------

* Embed a Terminal in each Nautilus tab / window,
* Follows the navigation: if you navigate in Nautilus, the ``cd``
  command is automatically executed in the terminal,
* Can be displayed / hidden using the ``F4`` key (configurable),
* Configurable: font, background and text color, terminal position (displayed
  at top or at bottom of the windows),...
* Supports copy / paste through contextual menu and
  ``Ctrl+Shift+C`` / ``Ctrl+Shift+V``,
* Supports drag & drop of file on the terminal,
* ...

If you want to read more about this project and its history, I wrote an
article on my blog (it is in French, but Google Translate should help) :
`Nautilus Terminal: The story of a complicated
project <https://blog.flozz.fr/2018/12/17/nautilus-terminal-lhistoire-dun-projet-complique/>`__.


Installing Nautilus Terminal
----------------------------

Requirements
~~~~~~~~~~~~

* A recent version of **Nautilus 3.x** or **Nautilus 40**,
* `nautilus-python <https://wiki.gnome.org/Projects/NautilusPython/>`__,
* `psutil <https://pypi.python.org/pypi/psutil/>`__,
* GLib 2 tools (``glib-compile-schemas``),
* dconf-editor (to configure the application; this will no more be required in
  the future).


Fedora Package
~~~~~~~~~~~~~~

::

   dnf copr enable tomaszgasior/mushrooms
   dnf install nautilus-terminal


Ubuntu
~~~~~~

There is no specific package for Ubuntu yet, so you will have to install it
from PyPI or from sources. But first you will have to install some dependencies
depending of your Ubuntu version.


Ubuntu 20.04 and later
^^^^^^^^^^^^^^^^^^^^^^

Install dependencies::

   sudo apt install python3-nautilus python3-psutil python3-pip libglib2.0-bin dconf-editor

Then follow the instructions to install it from PyPI or from sources.


Ubuntu 19.10 and earlier
^^^^^^^^^^^^^^^^^^^^^^^^

Install dependencies::

   sudo apt install python-nautilus python-psutil python-pip libglib2.0-bin dconf-editor

Then, follow the instructions to install it from PyPI or from sources,
but replace the ``pip3`` command by ``pip``.


From PyPI
~~~~~~~~~

User install::

   pip3 install --user nautilus_terminal

System-wide install::

   sudo pip3 install nautilus_terminal

Then kill Nautilus to allow it to load the new extension::

   nautilus -q


From sources
~~~~~~~~~~~~

Clone the repository and navigate to it::

   git clone git@github.com:flozz/nautilus-terminal.git
   cd nautilus-terminal

User install::

   pip3 install --user .

System-wide install::

   sudo pip3 install .

Then kill Nautilus to allow it to load the new extension::

   nautilus -q


Uninstalling (sources or PyPI packages)
---------------------------------------

User uninstall::

   python3 -m nautilus_terminal --uninstall-user
   pip3 uninstall nautilus-terminal

System-wide uninstall::

   sudo nautilus-terminal --uninstall-system
   sudo pip3 uninstall nautilus-terminal


Configuring
-----------

Nautilus Terminal can be configured, but there is no GUI to configure it
yet. Currently, configuration can be done through the **DConf Editor**
tool::

    dconf-editor /org/flozz/nautilus-terminal

.. figure:: ./dconf-editor.png
   :alt: dconf-editor


Trouble Shooting
----------------

Nautilus Terminal Doesn't show up? Here are a bunch of things to check before
opening an issue:

* Try to restart Nautilus::

        nautilus -q

* Try to restart Nautilus and keep it attached to a terminal to catch eventual
  error messages::

        nautilus -q && nautilus

* Check that the extension is properly installed with one of the following
  commands::

        nautilus-terminal --check
        python3 -m nautilus_terminal --check

  If everything is OK, the output should be::

        Nautilus Python: Installed
        Nautilus Terminal Extension: Installed

  If there is any error, you will have an help message similar to this one to
  tell you how to fix::

        Nautilus Python: Installed
        Nautilus Terminal Extension: Absent
            Please install the Nautilus Extension with one of the following commands:
            System-wide: sudo nautilus-terminal --install-system
            Current user: nautilus-terminal --install-user
            NOTE: you may need to replace the 'nautilus-terminal' command by 'python3 -m nautilus_terminal'.


If none of the above worked, please `open an issue
<https://github.com/flozz/nautilus-terminal/issues>`_ with as much information
as possible:

* How did you installed Nautilus Terminal,
* What you tried,
* Any error message outputted during the installation or by Nautilus,
* When possible, please include the output of one of the following command::

        nautilus-terminal --print-debug
        python3 -m nautilus_terminal --print-debug


Hacking and Debug
-----------------

If you want work on this software, you will first have to install the
dependencies listed above.

This extension comes in two parts: a conventional Python module
(``nautilus_terminal``), and a small bit of bootstrap code that’s loaded
by ``python-nautilus`` when Nautilus starts up
(``nautilus_terminal_extension.py``). The bootstrap code must be
installed where ``python-nautilus`` can find it before you can start
making changes and testing them::

   python3 -m nautilus_terminal --install-user  # Current user only
   sudo python3 -m nautilus_terminal --install-system  # System-wide

When the bootstrap is loaded into Nautilus, it imports the Python module
from either the normal ``PYTHONPATH``, or from your working copy of this
repository if the right debug environment is set.

With the bootstrap installed, you can use the following script to test
new code in Nautilus without having to reinstall the module::

   tools/debug-in-nautilus.sh
   tools/debug-in-nautilus.sh --no-bg  # keep Nautilus attached to the console

When you start working on this extension, you will have to compile the
GSettings schema (and you will have to recompile it each time you modify the
``nautilus_terminal/schemas/org.flozz.nautilus-terminal.gschema.xml`` file)::

   glib-compile-schemas nautilus_terminal/schemas/

Running lint and tests::

   pip3 install nox
   python3 -m nox -s lint
   python3 -m nox -s test

Happy hacking! :)


Release
-------

Things to do before releasing a new version:

* Update version number in ``nautilus_terminal/__init__.py``
* Compile GSetting schema:
  ``glib-compile-schemas nautilus_terminal/schemas``


Supporting this project
-----------------------

Wanna support this project?

* `☕️ Buy me a coffee <https://www.buymeacoffee.com/flozz>`__,
* `❤️ sponsor me on Github <https://github.com/sponsors/flozz>`__,
* `💵️ or give me a tip on PayPal <https://www.paypal.me/0xflozz>`__.


Changelog
---------

* **4.0.0:**

  * Nautilus 40 support
  * New logo
  * Adds an "About" window
  * Adds a context menu to copy/paste, run dconf-editor and display the "About"
    window
  * Adds a CLI to check, install, uninstall, print debug,...
    (``nautilus-terminal -h``)
  * Fixes Nautilus Terminal stealing the focus in new Nautilus windows (@tkachen, #54)
  * Adds an option to clear the terminal after each navigation (@tkachen, #55)
  * WARNING: This will be the last version to support Python 2.7!

* **3.5.0:**

  * Fixes minimum height when the teminal is on the bottom (@tkachen, #52)
  * Allows to configure the font (@tkachen, #10, #53)
  * Drops Python 3.6 support
  * Coding style enforced using Black

* **3.4.2:** Fixes the PYPI package with an up to date version of the
  compiled gsettings schema
* **3.4.1:** Updates documentation and settings screenshot.
* **3.4.0:**

  * Allows to configure the terminal toggle shortcut (#50, #43)
  * Allows to configure terminal background and text color (#32)

* **3.3.0:**

  * New option to have the terminal at the bottom of the window (#35)

* **3.2.3:**

  * Fixes encoding with Python 3 (#29)

* **3.2.2:**

  * Fixes ``VteTerminal.feed_child()`` call (#12)
  * Improves child process searching (@l-deniau, #14)

* **3.2.1:** Add a missing dependency in setup.py
* **3.2.0:** Add settings to Nautilus Terminal (#3)
* **3.1.1:**

  * Allow user install instead of system-wide (#1)
  * Use the user’s default shell instead of the hardcoded zsh (#2)
  * Focus the terminal after drag & drop of file on it (#4)

* **3.1.0:**

  * File drag & drop support
  * Hide the terminal in virtual emplacements (trash,…)
  * Optimizations (do not spawn the shell / no “cd” if the shell is
    not visible)

* **3.0.1:** Script to convert the README to reStructuredText for PYPI
* **3.0.0:** Initial Nautilus Terminal 3 release (early development
  version)


.. |Lint / Tests| image:: https://github.com/flozz/nautilus-terminal/workflows/Lint%20and%20Tests/badge.svg
   :target: https://github.com/flozz/nautilus-terminal/actions
.. |PYPI Version| image:: https://img.shields.io/pypi/v/nautilus_terminal.svg
   :target: https://pypi.org/project/nautilus_terminal/
.. |License| image:: https://img.shields.io/pypi/l/nautilus_terminal.svg
   :target: https://github.com/flozz/nautilus-terminal/blob/master/COPYING
.. |Discord| image:: https://img.shields.io/badge/chat-Discord-8c9eff?logo=discord&logoColor=ffffff
   :target: https://discord.gg/P77sWhuSs4
.. |Black| image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :target: https://black.readthedocs.io/en/stable/
