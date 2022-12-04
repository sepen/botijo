#!/bin/sh

PYTHON="$(/usr/bin/env python3)"
LIBDIR="/usr/lib/botijo"

cd $LIBDIR
$PYTHON botijo.pyc "$@"

# End of file