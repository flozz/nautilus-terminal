#!/bin/bash

if [ ! -x /usr/share/pandoc ] ; then
    echo "Pandoc is required to convert the README to reStructuredText"
    exit 1
fi

pandoc -f markdown -t rst -o README.rst README.md
sed -i "s#./screenshot.png#https://raw.githubusercontent.com/flozz/nautilus-terminal/master/screenshot.png#" README.rst
