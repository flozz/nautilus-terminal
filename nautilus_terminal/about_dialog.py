import os

from gi.repository import Gtk
from gi.repository import GdkPixbuf

from . import APPLICATION_NAME
from . import VERSION


def find_data_path(path):
    root = os.path.abspath(os.path.dirname(__file__))
    return os.path.join(root, path)


class AboutDialog(Gtk.AboutDialog):
    def __init__(self, parent=None):
        Gtk.AboutDialog.__init__(
            self,
            parent=parent,
            program_name=APPLICATION_NAME,
            comments="A terminal embedded in Nautilus, the GNOME's file browser",
            version=VERSION,
            copyright="Copyright (c) 2010-2021 Fabien LOISON",
            website_label="github.com/flozz/nautilus-terminal",
            website="https://github.com/flozz/nautilus-terminal",
            license_type=Gtk.License.GPL_3_0,
        )

        logo = GdkPixbuf.Pixbuf.new_from_file(
            find_data_path("images/nautilus-terminal-logo.svg")
        )
        self.set_logo(logo)
