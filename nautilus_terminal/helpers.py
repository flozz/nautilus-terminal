from gi.repository import Gio
import psutil


def gvfs_uri_to_path(uri):
    gvfs = Gio.Vfs.get_default()
    return gvfs.get_file_for_uri(uri).get_path()


def process_has_child(pid):
    for process in psutil.process_iter():
        if process.ppid() == pid:
            return True
    return False


def escape_path_for_shell(path):
    return "'%s'" % path.replace("'", "'\\''")
