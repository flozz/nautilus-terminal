from gi.repository import GLib, Gtk, Vte

from . import logger
from . import helpers


def _find_vpanel(crowbar):
    widget = crowbar
    while widget:
        if widget.get_name() == "GtkVPaned" and hasattr(widget, "_nt_instance"):
            return widget
        widget = widget.get_parent()
    return None


def _find_nautilus_window_slot(crowbar):
    widget = crowbar
    while widget:
        if widget.get_name() == "NautilusWindowSlot":
            return widget
        widget = widget.get_parent()
    return None


def create_or_update_natilus_terminal(crowbar):
    vpanel = _find_vpanel(crowbar)

    # Nautilus Terminal already inserted in this tab, update its path
    if vpanel:
        logger.log("NautilusTerminal instance found: updating its path...")
        vpanel._nt_instance.change_directory(crowbar.path)
        return vpanel._nt_instance

    # New tab, a new Nautilus Temrinal instance must be created
    logger.log("No NautilusTerminal instance found (new tab): creating a new NautilusTemrinal...")
    nautilus_window_slot = _find_nautilus_window_slot(crowbar)

    if not nautilus_window_slot:
        logger.warn("Unable to locate the NautilusWindowSlot widget: Nautilus Temrinal will not be injected!")
        return

    return NautilusTerminal(nautilus_window_slot, crowbar.nautilus_window,
            crowbar.nautilus_app, crowbar.path)


class NautilusTerminal(object):

    def __init__(self, parent_widget, nautilus_window, nautilus_app, cwd):
        self._parent_widget = parent_widget
        self._nautilus_window = nautilus_window
        self._nautilus_app = nautilus_app
        self._cwd = cwd

        self._ui_vpanel = None
        self._ui_terminal = None
        self._shell_pid = None

        self._build_ui()
        self._run_shell()

    def change_directory(self, path=None):
        if path:
            self._cwd = path
        else:
            path = self._cwd
        if not self.shell_is_busy():
            logger.log("NautilusTerminal.change_directory: curent directory changed to %s" % path)
            self._inject_command(" cd %s" % helpers.escape_path_for_shell(self._cwd))
        else:
            logger.log("NautilusTerminal.change_directory: curent directory NOT changed to %s (shell busy)" % path)

    def get_visible(self):
        pass  # TODO

    def set_visible(self, visible):
        pass  # TODO

    def toggle_visible(self):
        pass  # TODO

    def shell_is_busy(self):
        return helpers.process_has_child(self._shell_pid)

    def _inject_command(self, command):
        logger.log("NautilusTerminal._inject_command: %s" % command)
        self._ui_terminal.feed_child("%s\n" % command, len(command)+1)

    def _build_ui(self):
        # vpanel injection
        self._ui_vpanel = Gtk.VPaned(visible=True)
        self._ui_vpanel._nt_instance = self
        vbox = Gtk.VBox(visible=True)
        self._ui_vpanel.add2(vbox)
        for widget in self._parent_widget:
            self._parent_widget.remove(widget)
            expand = widget.get_name() in ["GtkOverlay", "NautilusCanvasView"]
            vbox.pack_start(widget, expand, expand, 0)
        self._parent_widget.pack_start(self._ui_vpanel, True, True, 0)

        # Terminal
        self._ui_terminal = Vte.Terminal(visible=True)
        self._ui_vpanel.add1(self._ui_terminal)

    def _run_shell(self):
        shell = "/bin/zsh"  # TODO make this configurable
        _, self._shell_pid = self._ui_terminal.spawn_sync(
                Vte.PtyFlags.DEFAULT, self._cwd, [shell],
                None, GLib.SpawnFlags.SEARCH_PATH, None, None)
        logger.log("Shell spawned (%s), PID: %i." % (shell, self._shell_pid))
