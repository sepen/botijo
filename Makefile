#
# Makefile
#

PYTHON=/usr/bin/python

DESTDIR=

PREFIX=/usr
LIBDIR=$(PREFIX)/lib/botijo

.PHONY: all install clean

all: clean src/botijo.pyc src/botijo

src/botijo.pyc: src/botijo.py
	@$(PYTHON) ./build.py && rm -f ./build.pyc

src/botijo: src/botijo.sh
	@sed -e "s|PYTHON=.*|PYTHON=$(PYTHON)|" \
	     -e "s|LIBDIR=.*|LIBDIR=$(LIBDIR)|" \
	     src/botijo.sh > src/botijo
	@chmod +x src/botijo

install: all
	@install -d -m 0755 $(DESTDIR)/$(PREFIX)/bin
	@install -m 0755 src/botijo $(DESTDIR)/$(PREFIX)/bin
	@install -d -m 0755 $(DESTDIR)/$(LIBDIR)
	@install -m 0644 src/*.pyc $(DESTDIR)/$(LIBDIR)

clean:
	@rm -f src/*.pyc src/botijo

# End of file
