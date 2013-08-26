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

docspub: BRANCH=gh-pages
docspub: HTMLDIR=doc/build/html
docspub: docs
	git checkout $(BRANCH)
	git rm -rf . || :
	echo '/doc/build/html/.buildinfo' > .gitignore
	touch .nojekyll
	git add $(HTMLDIR) .gitignore .nojekyll
	git mv $(HTMLDIR)/* .
	if git commit -m'Webpage update' -s; then \
	  git push $(shell git config --get branch.$(BRANCH).remote) $(BRANCH); \
	fi
	git checkout '@{-1}'

docsclean:
	$(MAKE) -C doc clean
