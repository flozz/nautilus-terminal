def create_or_update_natilus_terminal(crowbar):
    pass  # TODO Search for an existing nautilus terminal or create a new one

class NatilusTerminal(object):

    def __init__(self, nautilus_window, nautilus_app, cwd):
        self._nautilus_window = nautilus_window
        self._nautilus_app = nautilus_app
        self._cwd = cwd

        self._ui_vpanel = None
        self._ui_vte = None
        self._shell_pid = None

        self._build_ui()
        self._run_shell()

    def change_directory(self, path=None):
        if path:
            self._cwd = path
        else:
            path = self._cwd
        pass  # TODO

    def shell_is_busy(self):
        pass  # TODO

    def _build_ui(self):
        pass  # TODO

    def _run_shell(self):
        pass  # TODO
