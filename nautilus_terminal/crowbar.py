from gi.repository import GObject, Gtk, Gdk, Vte, GLib, Gio

from . import logger
from . import helpers


class Crowbar(Gtk.EventBox):

    def __init__(self, uri, window):
        super(Crowbar, self).__init__()

        self._uri = uri
        self._window = window
        self._path = helpers.gvfs_uri_to_path(uri)
        self._app = window.get_application()

        self.connect_after("parent-set", self._on_parent_set)

    def _on_parent_set(self, widget, old_parent):
        if old_parent:
            self.destroy()
            return
        logger.log("Crowbar inserted at %s" % self._path)
