import os
import signal

from gi.repository import GLib, Gtk, Vte

from . import logger
from . import helpers
from . import nautilus_accels_helpers


def _find_nautilus_terminal_vpanel(crowbar):
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
    vpanel = _find_nautilus_terminal_vpanel(crowbar)

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
        nautilus_accels_helpers.backup_nautilus_accels(nautilus_app, nautilus_window)

        self._parent_widget = parent_widget  # NautilusWindowSlot
        self._nautilus_window = nautilus_window
        self._nautilus_app = nautilus_app
        self._cwd = cwd

        self._ui_vpanel = None
        self._ui_terminal = None
        self._shell_pid = 0

        self._build_ui()
        self._spawn_shell()

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
        # GtkPaned (vpanel) injection:
        #
        # To inject our terminal in Nautilus, we first have to empty the
        # NautilusWindowSlot widget (parent widget) of the current view to make
        # some free space to insert a GtkPaned widget. Then we will insert back
        # the Nautilus' widgets we removed in the bottom part of the GtkPaned.

        self._ui_vpanel = Gtk.VPaned(visible=True)
        self._ui_vpanel._nt_instance = self
        vbox = Gtk.VBox(visible=True)
        self._ui_vpanel.add2(vbox)
        for widget in self._parent_widget:
            self._parent_widget.remove(widget)
            expand = widget.get_name() in ["GtkOverlay", "NautilusCanvasView"]
            vbox.pack_start(widget, expand, expand, 0)
        self._parent_widget.pack_start(self._ui_vpanel, True, True, 0)

        # Terminal creation:
        #
        # We can now create our VteTerminal and insert it in the top part of
        # our GtkPaned.

        self._ui_terminal = Vte.Terminal(visible=True)  # FIXME visibility
        self._ui_vpanel.add1(self._ui_terminal)

        # Disabling Nautilus' accels when the temrinal is focused:
        #
        # When the terminal is focused, we MUST remove ALL Nautilus accels to
        # be able to use properly the terminal (else we cannot type some
        # characters like "/", "~",... because the actions of the corresponding
        # accels are called). Of course we have also to restore the accels when
        # the terminal is no more focused.

        self._ui_terminal.connect("focus-in-event", self._on_terminal_focus_in_event)
        self._ui_terminal.connect("focus-out-event", self._on_terminal_focus_out_event)

        # Kill the shell when the tab is closed:
        #
        # Finally, we have to listen to some events of our parent widget (the
        # NautilusWindowSlot) to guess when the tab is closed in order to
        # kill the shell (else we will have planty zombi shell running in
        # background).
        #
        # * When the tab (or the window) is closed, the "unrealize" event is
        #   called so we have to kill the shell when the parent widget emit
        #   this event...
        #
        # * BUT when the tab is drag & dropped outside of the window (to open
        #   it in a new window), this event is also emitted... and the the
        #   "realize" event is emitted. So we have to spawn a new shell if
        #   that happen...

        self._parent_widget.connect("unrealize", self._on_nautilus_window_slot_unrealized)
        self._parent_widget.connect("realize", self._on_nautilus_window_slot_realized)

    def _spawn_shell(self):
        if self._shell_pid:
            logger.warn("_spawn_shell: Cannot swpawn a new shell: there is already a shell running...")
            return
        shell = "/bin/zsh"  # TODO make this configurable
        _, self._shell_pid = self._ui_terminal.spawn_sync(
                Vte.PtyFlags.DEFAULT, self._cwd, [shell],
                None, GLib.SpawnFlags.SEARCH_PATH, None, None)
        logger.log("Shell spawned (%s), PID: %i." % (shell, self._shell_pid))

    def _kill_shell(self):
        if not self._shell_pid:
            logger.warn("_kill_shell: Cannot kill the shell: there is no shell to kill...")
            return
        try:
            os.kill(self._shell_pid, signal.SIGTERM)
            os.kill(self._shell_pid, signal.SIGKILL)
        except OSError:
            logger.error("_kill_shell: An error occured when killing the shell %i" % self._shell_pid)
            self._shell_pid = 0
        logger.log("Shell %i killed." % self._shell_pid)
        self._shell_pid = 0

    def _on_nautilus_window_slot_unrealized(self, widget):
        logger.log("The tab have (probably) been closed: killing the shell %i" % self._shell_pid)
        self._kill_shell()

    def _on_nautilus_window_slot_realized(self, widget):
        logger.log("Oops, the tab have NOT been closed: spawning a new shell")
        self._spawn_shell()

    def _on_terminal_focus_in_event(self, widget, event):
        nautilus_accels_helpers.remove_nautilus_accels(self._nautilus_app)

    def _on_terminal_focus_out_event(self, widget, event):
        nautilus_accels_helpers.restore_nautilus_accels(self._nautilus_app)
