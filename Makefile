#!/usr/bin/make
#
# This file is part of reclass (http://github.com/madduck/reclass)
#
# Copyright © 2007–13 martin f. krafft <madduck@madduck.net>
# Released under the terms of the Artistic Licence 2.0
#

PYTHON_DEFAULT = /usr/bin/python
PYTHON := $(shell which python)

IN_FILES = $(wildcard *.in adapters/*.in)
all: $(patsubst %.in,%,$(IN_FILES))
.PHONY: all

ifeq ($(PYTHON),$(PYTHON_DEFAULT))
REPLACE_PYTHON_SHEBANG = cat
else
REPLACE_PYTHON_SHEBANG = sed -e 's,$(PYTHON_DEFAULT),$(PYTHON),g'
endif

%: %.in ALWAYS_REDO
	$(REPLACE_PYTHON_SHEBANG) $< > $@
	chmod +x $@

ALWAYS_REDO:
	@:
