#
# Makefile
#

PYTHON = /usr/bin/env python3

DESTDIR =
PREFIX = /usr
LIBDIR = $(PREFIX)/lib/botijo

.PHONY: clean botijo install

all: clean botijo

src/botijo.pyc: src/botijo.py
	@$(PYTHON) ./build.py && rm -f ./build.pyc

src/botijo: src/botijo.sh
	@sed -e "s|PYTHON=.*|PYTHON=$(PYTHON)|" \
	     -e "s|LIBDIR=.*|LIBDIR=$(LIBDIR)|" \
	     src/botijo.sh > src/botijo
	@chmod +x src/botijo

src/botijo.rc: src/botijo.rc.in
	@sed -e "s|{PYTHON}|$(PYTHON)|" \
		-e "s|{PREFIX}|$(PREFIX)|" \
		src/botijo.rc.in > src/botijo.rc

botijo: src/botijo.pyc src/botijo src/botijo.rc


install: clean botijo
	@install -d -m 0755 $(DESTDIR)/$(PREFIX)/bin
	@install -m 0755 src/botijo $(DESTDIR)/$(PREFIX)/bin
	@install -d -m 0755 $(DESTDIR)/$(LIBDIR)
	@install -m 0644 src/*.pyc $(DESTDIR)/$(LIBDIR)
	@install -D -m 0644 src/botijo.conf $(DESTDIR)/$(PREFIX)/etc/botijo.conf
	@install -D -m 0755 src/botijo.rc $(DESTDIR)/etc/rc.d/botijo

clean:
	@rm -f src/*.pyc src/botijo src/botijo.rc


# End of file
