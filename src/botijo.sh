#!/bin/sh

PYTHON=/usr/bin/python

PREFIX=/usr

cd $PREFIX/lib/botijo
$PYTHON botijo.pyc "$@"
cd -

# End of file
