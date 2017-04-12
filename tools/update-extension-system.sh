#!/bin/sh
# Make the extension available to all users.
#
# The Python integration for Nautilus doesn't seem to respect /usr/local
# prefixes despite its docs saying it should. For now, global installs
# need the extension module to go in the /usr location only.

SRC=nautilus_terminal/nautilus_terminal_extension.py
TARGDIR=/usr/share/nautilus-python/extensions

bn=`basename "$SRC"`

case "$1" in
    install)
        mkdir -v -p -m 0755 "$TARGDIR"
        cp -v "$SRC" "$TARGDIR/$bn"
        chmod -c 0644 "$TARGDIR/$bn"
        ;;
    uninstall)
        rm -vf "$TARGDIR/$bn"
        ;;
    *)
        echo >&2 "usage: $0 {install|uninstall}"
        ;;
esac
