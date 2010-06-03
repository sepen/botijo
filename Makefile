#
# Makefile
#

PYTHON=/usr/bin/python

DESTDIR=
PREFIX=/usr

.PHONY: all install clean

all: clean src/botijo.pyc src/botijo

src/botijo.pyc: src/botijo.py
	@$(PYTHON) ./build.py && rm -f ./build.pyc

src/botijo: src/botijo.sh
	@sed -e "s|PYTHON=.*|PYTHON=$(PYTHON)|" \
	     -e "s|PREFIX=.*|PREFIX=$(PREFIX)|" \
	     src/botijo.sh > src/botijo

install: all
	@install -d $(DESTDIR)/$(PREFIX)/{bin,lib/botijo}
	@install -m 0755 src/botijo $(DESTDIR)/$(PREFIX)/bin
	@install -m 0644 src/*.pyc $(DESTDIR)/$(PREFIX)/lib/botijo

clean:
	@rm -f src/*.pyc src/botijo

# End of file
