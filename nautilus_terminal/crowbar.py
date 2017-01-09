from gi.repository import GObject, Nautilus, Gtk, Gdk, Vte, GLib, Gio

class Crowbar(GObject.GObject, Nautilus.LocationWidgetProvider):

    def get_widget(self, uri, window):
        pass
