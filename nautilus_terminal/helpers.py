from gi.repository import Gio

def gvfs_uri_to_path(uri):
    gvfs = Gio.Vfs.get_default()
    return gvfs.get_file_for_uri(uri).get_path()

