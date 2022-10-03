import os
import signal
import sys

from . import logger
from . import helpers
from . import color_helpers
from . import nautilus_accels_helpers
from .about_dialog import AboutDialog

import gi

gi.require_version("Vte", "2.91")
from gi.repository import GLib, Gio, Gtk, Gdk, Vte, Pango  # noqa: E402


_EXPAND_WIDGETS = [
    "GtkOverlay",
    "NautilusCanvasView",
    "NautilusViewIconController",
    "NautilusListView",
]
_AUTO_CLEAN_SOFT = 1
_AUTO_CLEAN_HARD = 2


def _vte_terminal_feed_child(vte_terminal, text):
    if sys.version_info.major >= 3:
        text = text.encode("utf-8")
    try:
        # Old call
        return vte_terminal.feed_child(text, len(text) + 1)
    except TypeError:
        # Newer call
        return vte_terminal.feed_child(text)


def _find_nautilus_terminal_vpanel(crowbar):
    widget = crowbar
    while widget:
        if widget.get_name() == "GtkVPaned" and hasattr(
            widget, "_nt_instance"
        ):
            return widget
        widget = widget.get_parent()
    return None


def _find_parent_widget(widget, parent_widget_name):
    while widget:
        if widget.get_name() == parent_widget_name:
            return widget
        widget = widget.get_parent()
    return None


def create_or_update_natilus_terminal(crowbar):
    vpanel = _find_nautilus_terminal_vpanel(crowbar)

    # Nautilus Terminal already inserted in this tab, update its path
    if vpanel:
        logger.log("NautilusTerminal instance found: updating its path...")
        vpanel._nt_instance.change_directory(crowbar.path)
        # may update view
        vpanel._nt_instance.update_ui()
        return vpanel._nt_instance

    # New tab, a new Nautilus Terminal instance must be created
    logger.log(
        "No NautilusTerminal instance found (new tab): creating a new NautilusTerminal..."
    )
    nautilus_window_slot = _find_parent_widget(crowbar, "NautilusWindowSlot")

    if not nautilus_window_slot:
        logger.warn(
            "Unable to locate the NautilusWindowSlot widget: Nautilus Terminal will not be injected!"
        )
        return

    return NautilusTerminal(
        nautilus_window_slot,
        crowbar.nautilus_window,
        crowbar.nautilus_app,
        crowbar.path,
    )


class NautilusTerminal(object):
    def __init__(self, parent_widget, nautilus_window, nautilus_app, cwd):
        self._parent_widget = parent_widget  # NautilusWindowSlot
        self._nautilus_window = nautilus_window
        self._nautilus_app = nautilus_app
        self._vbox = None
        self._cwd = cwd

        self._settings = helpers.get_application_settings()
        # Allows settings to be defined in dconf-editor even if
        # the schema is not installed...
        helpers.set_all_settings(self._settings)

        self._ui_vpanel = None
        self._ui_terminal = None
        self._terminal_requested_visibility = self._settings.get_boolean(
            "default-show-terminal"
        )
        self._terminal_focus_on_init = self._settings.get_boolean(
            "default-focus-terminal"
        )
        self._terminal_bottom = self._settings.get_boolean("terminal-bottom")
        self._auto_clean = self._settings.get_enum("auto-clean")
        self._auto_cut_user_input = self._settings.get_boolean(
            "auto-cut-user-input"
        )
        self._nterm_action_group = None
        self._ntermwin_action_group = None
        self._shell_pid = 0
        self._shell_killed = False

        nautilus_accels_helpers.backup_nautilus_accels(
            nautilus_app, nautilus_window
        )
        self._build_and_inject_ui()
        self._build_actions()
        self._insert_ntermwin_action_group_in_current_window()
        self._build_accels()

        # Set if the terminal should be visible by default.
        # Will spawn the shell automatically if the terminal is visible
        self.set_terminal_visible(
            self._terminal_requested_visibility, self._terminal_focus_on_init
        )

    def change_directory(self, path):
        # "virtual" location (trash:///, network:///,...)
        # No cd & hide the Terminal
        if not path:
            logger.log(
                'NautilusTerminal.change_directory: terminal hidden: navigating to a "virtual" location'
            )
            self._ui_terminal.set_visible(False)
            return

        self._cwd = path

        # Makes the terminal visible again if it was hidden by navigating to a
        # "virtual" location
        if (
            self.get_terminal_visible()
            != self.get_terminal_requested_visibility()
        ):
            self.set_terminal_visible(focus=False)

        # Do not navigate if the terminal is not visible
        if not self.get_terminal_visible():
            logger.log(
                "NautilusTerminal.change_directory: current directory NOT changed to %s (terminal not visible)"
                % path
            )
            return

        # Do not "cd" if the shell's cwd is already the same as the targeted path
        if helpers.get_process_cwd(self._shell_pid) == path:
            return

        logger.log(
            "NautilusTerminal.change_directory: current directory changed to %s"
            % path
        )

        command = " cd %s " % helpers.escape_path_for_shell(self._cwd)
        if self.get_auto_clean() == _AUTO_CLEAN_HARD:
            command += "&& clear "

        self._inject_command(command)

        if self.get_auto_clean() == _AUTO_CLEAN_SOFT:
            self._emit_key_press("l", Gdk.ModifierType.CONTROL_MASK)

    def stash_current_termianl_content(self):
        # move to the end of line in terminal
        self._emit_key_press("e", Gdk.ModifierType.CONTROL_MASK)
        # cut all content in line to the left
        self._emit_key_press("u", Gdk.ModifierType.CONTROL_MASK)

    def get_auto_cut_user_input(self):
        return self._auto_cut_user_input

    def get_auto_clean(self):
        return self._auto_clean

    def get_terminal_requested_visibility(self):
        """Does the user requested the terminal to be visible?

        This state can be different to the terminal widget real state, for
        example the terminal can be requested visible by the user but hidden
        because navigating to the trash)?
        """
        return self._terminal_requested_visibility

    def get_terminal_visible(self):
        """Does the terminal widget is visible?"""
        return self._ui_terminal.get_visible()

    def set_terminal_visible(self, visible=None, focus=True):
        if visible is None:
            visible = self._terminal_requested_visibility

        self._ui_terminal.set_visible(visible)
        self._terminal_requested_visibility = visible

        # Spawn a shell if it is not yet spawned (if the terminal has never
        # been visible before)
        if visible and not self._shell_pid:
            self._spawn_shell()

        # Update the directory as the terminal does not "cd" when it is hidden
        if visible:
            self.change_directory(self._cwd)

        # Focus the terminal
        if visible and focus:
            self._ui_terminal.grab_focus()

    def shell_is_busy(self):
        return helpers.process_has_child(self._shell_pid)

    def _inject_command(self, command):
        # Do not inject the command if the shell has something running in
        if self.shell_is_busy():
            logger.warn(
                "NautilusTerminal._inject_command: command '%s' not injected (shell busy)"
                % command
            )
            return
        logger.log("NautilusTerminal._inject_command: %s" % command)

        # Remove any user inputs before injecting the command
        if self.get_auto_cut_user_input():
            self.stash_current_termianl_content()

        _vte_terminal_feed_child(self._ui_terminal, "%s\n" % command)

    def _emit_key_press(self, key, state=0):
        event = Gdk.Event().new(Gdk.EventType.KEY_PRESS)
        event.state = state
        event.keyval = Gdk.keyval_from_name(key)
        event.window = self._ui_terminal.get_window()
        event.send_event = True
        self._ui_terminal.emit("key-press-event", event)

    def update_ui(self):
        for widget in self._parent_widget:
            if widget.get_name() in _EXPAND_WIDGETS:
                self._parent_widget.remove(widget)
                self._vbox.pack_start(widget, True, True, 0)

    def _build_and_inject_ui(self):
        # GtkPaned (vpanel) injection:
        #
        # To inject our terminal in Nautilus, we first have to empty the
        # NautilusWindowSlot widget (parent widget) of the current view to make
        # some free space to insert a GtkPaned widget. Then we will insert back
        # the Nautilus' widgets we removed in the bottom part of the GtkPaned.

        self._ui_vpanel = Gtk.VPaned(visible=True)
        self._ui_vpanel._nt_instance = self
        self._vbox = Gtk.VBox(visible=True)
        if self._terminal_bottom:
            self._ui_vpanel.pack1(self._vbox, resize=True, shrink=True)
        else:
            self._ui_vpanel.pack2(self._vbox, resize=True, shrink=True)

        for widget in self._parent_widget:
            self._parent_widget.remove(widget)
            expand = widget.get_name() in _EXPAND_WIDGETS
            self._vbox.pack_start(widget, expand, expand, 0)
        self._parent_widget.pack_start(self._ui_vpanel, True, True, 0)

        # Terminal creation:
        #
        # We can now create our VteTerminal and insert it in the top part of
        # our GtkPaned.

        self._ui_terminal = Vte.Terminal()

        settings_font = self._settings.get_string("custom-font")
        self._ui_terminal.set_font(Pango.FontDescription(settings_font))

        self._ui_terminal.set_audible_bell(False)

        self._ui_terminal.connect(
            "child-exited", self._on_terminal_child_existed
        )
        if self._terminal_bottom:
            self._ui_vpanel.pack2(
                self._ui_terminal, resize=False, shrink=False
            )
        else:
            self._ui_vpanel.pack1(
                self._ui_terminal, resize=False, shrink=False
            )

        TERMINAL_CHAR_HEIGHT = self._ui_terminal.get_char_height()
        TERMINAL_BORDER_WIDTH = 1
        TERMINAL_MIN_HEIGHT = self._settings.get_uint("min-terminal-height")

        self._ui_terminal.set_property(
            "height-request",
            TERMINAL_CHAR_HEIGHT * TERMINAL_MIN_HEIGHT
            + TERMINAL_BORDER_WIDTH * 2,
        )

        # Terminal foreground and background colors

        fg_color = (255, 255, 255)
        bg_color = (0, 0, 0)

        settings_fg_color = self._settings.get_string("foreground-color")
        settings_bg_color = self._settings.get_string("background-color")

        if color_helpers.is_color(settings_fg_color):
            fg_color = color_helpers.parse_color_string(settings_fg_color)

        if color_helpers.is_color(settings_bg_color):
            bg_color = color_helpers.parse_color_string(settings_bg_color)

        foreground = Gdk.RGBA(
            fg_color[0] / 255.0,
            fg_color[1] / 255.0,
            fg_color[2] / 255.0,
            1,
        )
        background = Gdk.RGBA(
            bg_color[0] / 255.0,
            bg_color[1] / 255.0,
            bg_color[2] / 255.0,
            1,
        )

        # Terminal color palette

        settings_color_palette = self._settings.get_strv("color-palette")

        palette_colors = []
        if any(settings_color_palette) and len(settings_color_palette) in (
            8,
            16,
            232,
            256,
        ):
            for color_code in settings_color_palette:
                if not color_helpers.is_color(color_code):
                    color_code = "White"  # Invalid colors default to white

                color = color_helpers.parse_color_string(color_code)
                color_rgba = Gdk.RGBA(
                    color[0] / 255.0,
                    color[1] / 255.0,
                    color[2] / 255.0,
                    1,
                )
                palette_colors.append(color_rgba)

        self._ui_terminal.set_colors(foreground, background, palette_colors)

        # Highlight colors

        foreground_hl_color = None
        background_hl_color = None

        settings_fg_hl_color = self._settings.get_string(
            "foreground-highlight-color"
        )
        settings_bg_hl_color = self._settings.get_string(
            "background-highlight-color"
        )

        if color_helpers.is_color(settings_fg_hl_color):
            fg_hl_color = color_helpers.parse_color_string(
                settings_fg_hl_color
            )
            foreground_hl_color = Gdk.RGBA(
                fg_hl_color[0] / 255.0,
                fg_hl_color[1] / 255.0,
                fg_hl_color[2] / 255.0,
                1,
            )

        if color_helpers.is_color(settings_bg_hl_color):
            bg_hl_color = color_helpers.parse_color_string(
                settings_bg_hl_color
            )
            background_hl_color = Gdk.RGBA(
                bg_hl_color[0] / 255.0,
                bg_hl_color[1] / 255.0,
                bg_hl_color[2] / 255.0,
                1,
            )

        self._ui_terminal.set_color_highlight_foreground(foreground_hl_color)
        self._ui_terminal.set_color_highlight(background_hl_color)

        # Bold text as bright

        self._ui_terminal.set_bold_is_bright(
            self._settings.get_boolean("bold-is-bright")
        )

        # File drag & drop support

        self._ui_terminal.drag_dest_set(
            Gtk.DestDefaults.MOTION
            | Gtk.DestDefaults.HIGHLIGHT
            | Gtk.DestDefaults.DROP,
            [Gtk.TargetEntry.new("text/uri-list", 0, 0)],
            Gdk.DragAction.COPY,
        )
        self._ui_terminal.drag_dest_add_uri_targets()
        self._ui_terminal.connect(
            "drag-data-received", self._on_terminal_drag_data_received
        )

        # Disabling Nautilus' accels when the terminal is focused:
        #
        # When the terminal is focused, we MUST remove ALL Nautilus accels to
        # be able to use properly the terminal (else we cannot type some
        # characters like "/", "~",... because the actions of the corresponding
        # accels are called). Of course we have also to restore the accels when
        # the terminal is no more focused.

        self._ui_terminal.connect(
            "focus-in-event", self._on_terminal_focus_in_event
        )
        self._ui_terminal.connect(
            "focus-out-event", self._on_terminal_focus_out_event
        )
        # Register the window-level action group of the currently displayed
        # terminal
        #
        # When the active tab changes, we have to register on the nautilus
        # window the corresponding action group to allow related accels to work
        # properly. The "map" event of the NautilusWindowSlot (our parent
        # widget) is called when its tab become active.

        self._parent_widget.connect(
            "map", self._on_nautilus_window_slot_mapped
        )

        # Kill the shell when the tab is closed:
        #
        # Finally, we have to listen to some events of our parent widget (the
        # NautilusWindowSlot) to guess when the tab is closed in order to
        # kill the shell (else we will have plenty zombie shell running in
        # background).
        #
        # * When the tab (or the window) is closed, the "unrealize" event is
        #   called so we have to kill the shell when the parent widget emit
        #   this event...
        #
        # * BUT when the tab is drag & dropped outside of the window (to open
        #   it in a new window), this event is also emitted... and the
        #   "realize" event is emitted right after. So we have to spawn a new
        #   shell if that happen...

        self._parent_widget.connect(
            "unrealize", self._on_nautilus_window_slot_unrealized
        )
        self._parent_widget.connect(
            "realize", self._on_nautilus_window_slot_realized
        )

        # Terminal Context Menu

        self._ui_menu = Gtk.Menu()

        menu_item = Gtk.ImageMenuItem.new_from_stock("gtk-copy", None)
        menu_item.connect_after(
            "activate", lambda w: self._ui_terminal.copy_clipboard()
        )
        self._ui_menu.add(menu_item)

        menu_item = Gtk.ImageMenuItem.new_from_stock("gtk-paste", None)
        menu_item.connect_after(
            "activate", lambda w: self._ui_terminal.paste_clipboard()
        )
        self._ui_menu.add(menu_item)

        self._ui_menu.add(Gtk.SeparatorMenuItem())

        menu_item = Gtk.ImageMenuItem.new_from_stock("gtk-preferences", None)
        menu_item.connect_after("activate", self._on_menu_preferences_activate)
        self._ui_menu.add(menu_item)

        menu_item = Gtk.ImageMenuItem.new_from_stock("gtk-about", None)
        menu_item.connect_after("activate", self._on_menu_about_activate)
        self._ui_menu.add(menu_item)

        self._ui_menu.show_all()
        self._ui_terminal.connect(
            "button-release-event", self._on_terminal_popup_menu
        )

    def _build_actions(self):
        # nterm action group
        self._nterm_action_group = Gio.SimpleActionGroup()
        self._ui_terminal.insert_action_group(
            "nterm", self._nterm_action_group
        )

        copy_action = Gio.SimpleAction(name="copy")
        copy_action.connect("activate", self._on_nterm_copy_action_activated)
        self._nterm_action_group.add_action(copy_action)

        paste_action = Gio.SimpleAction(name="paste")
        paste_action.connect("activate", self._on_nterm_paste_action_activated)
        self._nterm_action_group.add_action(paste_action)

        # ntermwin action group
        self._ntermwin_action_group = Gio.SimpleActionGroup()

        terminal_visible_action = Gio.SimpleAction(name="terminal-visible")
        terminal_visible_action.connect(
            "activate", self._on_ntermwin_terminal_visible_action_activated
        )
        self._ntermwin_action_group.add_action(terminal_visible_action)

    def _insert_ntermwin_action_group_in_current_window(self):
        self._nautilus_window.insert_action_group(
            "ntermwin", self._ntermwin_action_group
        )

    def _build_accels(self):
        # nterm
        self._nautilus_app.set_accels_for_action(
            "nterm.copy", ["<Primary><Shift>c"]
        )
        self._nautilus_app.set_accels_for_action(
            "nterm.paste", ["<Primary><Shift>v"]
        )

        # ntermwin
        accel = self._settings.get_string("toggle-shortcut")
        self._nautilus_app.set_accels_for_action(
            "ntermwin.terminal-visible", [accel]
        )

    def _spawn_shell(self):
        if self._shell_pid:
            logger.warn(
                "NautilusTerminal._spawn_shell: Cannot spawn a new shell: there is already a shell running."
            )
            return
        shell = helpers.get_user_default_shell()
        if self._settings.get_boolean("use-custom-command"):
            shell = self._settings.get_string("custom-command")
        _, self._shell_pid = self._ui_terminal.spawn_sync(
            Vte.PtyFlags.DEFAULT,
            self._cwd,
            [shell],
            ["INSIDE_NAUTILUS_PYTHON=1"],
            GLib.SpawnFlags.SEARCH_PATH,
            None,
            None,
        )
        self._shell_killed = False
        logger.log(
            "NautilusTerminal._spawn_shell: Shell spawned (%s), PID: %i."
            % (shell, self._shell_pid)
        )

    def _kill_shell(self):
        if not self._shell_pid:
            logger.warn(
                "NautilusTerminal._kill_shell: Cannot kill the shell: there is no shell to kill..."
            )
            return
        self._shell_killed = True
        try:
            os.kill(self._shell_pid, signal.SIGTERM)
            os.kill(self._shell_pid, signal.SIGKILL)
        except OSError:
            logger.error(
                "NautilusTerminal._kill_shell: An error occured when killing the shell %i"
                % self._shell_pid
            )
            self._shell_pid = 0
        logger.log("Shell %i killed." % self._shell_pid)
        self._shell_pid = 0

    def _on_nautilus_window_slot_mapped(self, widget):
        logger.log("The active tab has changed.")
        self._insert_ntermwin_action_group_in_current_window()

    def _on_nautilus_window_slot_unrealized(self, widget):
        logger.log(
            "The tab have (probably) been closed: killing the shell %i"
            % self._shell_pid
        )
        self._kill_shell()
        self._nautilus_window = None

    def _on_nautilus_window_slot_realized(self, widget):
        logger.log("Oops, the tab have NOT been closed: spawning a new shell")
        self._spawn_shell()
        self._nautilus_window = _find_parent_widget(widget, "NautilusWindow")
        self._insert_ntermwin_action_group_in_current_window()

    def _on_terminal_focus_in_event(self, widget, event):
        nautilus_accels_helpers.remove_nautilus_accels(self._nautilus_app)

    def _on_terminal_focus_out_event(self, widget, event):
        nautilus_accels_helpers.restore_nautilus_accels(self._nautilus_app)

    def _on_terminal_child_existed(self, widget, arg1):
        self._shell_pid = 0
        if not self._shell_killed:
            self._spawn_shell()

    def _on_terminal_drag_data_received(
        self, widget, context, x, y, data, info, time
    ):
        for uri in data.get_uris():
            path = helpers.escape_path_for_shell(helpers.gvfs_uri_to_path(uri))
            _vte_terminal_feed_child(self._ui_terminal, "%s " % path)
        self._ui_terminal.grab_focus()

    def _on_terminal_popup_menu(self, widget, event):
        if event.type == Gdk.EventType.BUTTON_RELEASE and event.button != 3:
            return
        self._ui_menu.popup(None, None, None, None, 3, 0)

    def _on_menu_preferences_activate(self, widget):
        self._inject_command("dconf-editor /org/flozz/nautilus-terminal")

    def _on_menu_about_activate(self, widget):
        about_dialog = AboutDialog(parent=self._nautilus_window)
        about_dialog.run()
        about_dialog.destroy()

    def _on_nterm_copy_action_activated(self, action, parameter):
        logger.log("nterm.copy action activated")
        self._ui_terminal.copy_clipboard()

    def _on_nterm_paste_action_activated(self, action, parameter):
        logger.log("nterm.paste action activated")
        self._ui_terminal.paste_clipboard()

    def _on_ntermwin_terminal_visible_action_activated(
        self, action, parameter
    ):
        logger.log("ntermwin.terminal-visible action activated")
        self.set_terminal_visible(not self.get_terminal_visible())
