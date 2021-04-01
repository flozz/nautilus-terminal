from gi.repository import Gtk

from . import logger
from . import helpers
from .nautilus_terminal import create_or_update_natilus_terminal


class Crowbar(Gtk.EventBox):
    def __init__(self, uri, window):
        super(Crowbar, self).__init__()

        self.uri = uri
        self.nautilus_window = window
        self.nautilus_app = window.get_application()
        self.path = helpers.gvfs_uri_to_path(uri)

        self.connect_after("parent-set", self._on_parent_set)

    def _on_parent_set(self, widget, old_parent):
        if old_parent:
            self.destroy()
            return
        logger.log("Crowbar inserted at %s" % self.path)
        create_or_update_natilus_terminal(self)
