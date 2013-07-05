#
# This file is part of reclass (http://github.com/madduck/reclass)
#
# Copyright © 2007–13 martin f. krafft <madduck@madduck.net>
# Released under the terms of the Artistic Licence 2.0
#
PYFILES = $(shell find -name .git -o -name dist -o -name build -prune -o -name '*.py' -print)

lint:
	@echo pylint --rcfile=.pylintrc $(ARGS) …
	@pylint --rcfile=.pylintrc $(ARGS) $(PYFILES)
.PHONY: lint

lint-errors: ARGS=--errors-only
lint-errors: lint
.PHONY: lint-errors

lint-report: ARGS=--report=y
lint-report: lint
.PHONY: lint-report
