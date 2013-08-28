#
# This file is part of reclass (http://github.com/madduck/reclass)
#
# Copyright © 2007–13 martin f. krafft <madduck@madduck.net>
# Released under the terms of the Artistic Licence 2.0
#
PYFILES = $(shell find -name .git -o -name dist -o -name build -prune -o -name '*.py' -print)

tests:
	python ./run_tests.py
.PHONY: tests

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

coverage: .coverage
	python-coverage -r -m
.PHONY: coverage
.coverage: $(PYFILES)
	python-coverage -x setup.py nosetests

docs:
	$(MAKE) -C doc man html

GH_BRANCH=gh-pages
HTMLDIR=doc/build/html
docspub:
ifeq ($(shell git branch --list $(GH_BRANCH)-base),)
	@echo "Please fetch the $(GH_BRANCH)-base branch from Github to be able to publish documentation:" >&2
	@echo "  git branch gh-pages-base origin/gh-pages-base" >&2
	@false
else
	$(MAKE) docs
	git checkout $(GH_BRANCH) || git checkout -b $(GH_BRANCH) $(GH_BRANCH)-base
	git reset --hard $(GH_BRANCH)-base
	git add $(HTMLDIR)
	git mv $(HTMLDIR)/* .
	git commit -m'Webpage update'
	git push -f $(shell git config --get branch.$(GH_BRANCH)-base.remote) $(GH_BRANCH)
	git checkout '@{-1}'
endif

docsclean:
	$(MAKE) -C doc clean
