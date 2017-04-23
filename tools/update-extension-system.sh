#!/bin/sh

# Make the extension available to all users.
#
# The Python integration for Nautilus doesn't seem to respect /usr/local
# prefixes despite its docs saying it should. For now, global installs
# need the extension module to go in the /usr location only.
#
# This script also compiles GSettings schemas

SRC=nautilus_terminal/nautilus_terminal_extension.py
TARGDIR=/usr/share/nautilus-python/extensions

SCHEMASDIR=/usr/local/share/glib-2.0/schemas
SCHEMAFILE=org.flozz.nautilus-terminal.gschema.xml

bn=`basename "$SRC"`

case "$1" in
    install)
        mkdir -v -p -m 0755 "$TARGDIR"
        cp -v "$SRC" "$TARGDIR/$bn"
        chmod -c 0644 "$TARGDIR/$bn"
        glib-compile-schemas $SCHEMASDIR
        ;;
    uninstall)
        rm -vf "$TARGDIR/$bn"
        rm -vf $SCHEMASDIR/$SCHEMAFILE
        glib-compile-schemas $SCHEMASDIR
        ;;
    *)
        echo >&2 "usage: $0 {install|uninstall}"
        ;;
esac
