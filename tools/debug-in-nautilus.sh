#!/bin/bash

nautilus -q

export GDK_DEBUG=interactive
export NAUTILUS_TERMINAL_DEBUG=true
export NAUTILUS_TERMINAL_DEBUG_PACKAGE_PATH="$PWD"

nautilus "$PWD" &
