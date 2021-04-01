import os
import pwd

from gi.repository import Gio
import psutil

from . import APPLICATION_ID


def gvfs_uri_to_path(uri):
    gvfs = Gio.Vfs.get_default()
    return gvfs.get_file_for_uri(uri).get_path()


def process_has_child(pid):
    return len(psutil.Process(pid).children()) > 0


def get_process_cwd(pid):
    return psutil.Process(pid).cwd()


def escape_path_for_shell(path):
    return "'%s'" % path.replace("'", "'\\''")


def get_user_default_shell():
    return pwd.getpwuid(os.getuid()).pw_shell


def get_package_schemas_directory():
    """Returns the directory of the package's schemas."""
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), "schemas")


def gsettings_schema_installed(schemas_id):
    """Checks if the schema with the given id is installed or not."""
    default_schemas_source = Gio.SettingsSchemaSource.get_default()
    schema_list = default_schemas_source.list_schemas(True)

    if schemas_id in schema_list.non_relocatable:
        return True

    if schemas_id in schema_list.relocatable:
        return True

    return False


def get_settings(schema_id, schemas_directory=None):
    """Get the settings for the given schema id.

    If the schema is not installed and a schema directory is provided, the
    schemas of the given directory will be loaded.
    """

    if gsettings_schema_installed(schema_id):
        settings = Gio.Settings.new(schema_id)
        return settings

    if schemas_directory:
        source = Gio.SettingsSchemaSource.new_from_directory(
            schemas_directory, Gio.SettingsSchemaSource.get_default(), True
        )
        schema = source.lookup(schema_id, True)
        settings = Gio.Settings.new_full(schema, None, None)
        return settings


def set_all_settings(settings):
    """Sets a value (the default one if not modified) for each setting.
    This allow settings to be visible in dconf-editor even if the schema
    is not installed.
    """
    for key in settings.list_keys():
        settings.set_value(key, settings.get_value(key))


def get_application_settings():
    """Get Nautilus Terminal settings"""
    return get_settings(APPLICATION_ID, get_package_schemas_directory())
