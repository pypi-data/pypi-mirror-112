.PHONY: clean lint format help tests coverage
.DEFAULT_GOAL := help

PYTHON := venv/bin/python

define PRINT_HELP_PYSCRIPT
import re, sys

for line in sys.stdin:
        match = re.match(r'^([a-zA-Z_-]+):.*?## (.*)$$', line)
        if match:
                target, help = match.groups()
                print("\033[36m%-15s\033[0m %s" % (target, help))
endef
export PRINT_HELP_PYSCRIPT

help:
	@$(PYTHON) -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)

clean: ## remove all build, test, coverage and Python artifacts
	rm -rf build dist .eggs *.egg-info
	find webdomains/ \
	  \( -name '*.py[co]' -o -name '__pycache__' \) -exec rm -rf {} +

tests: ## run tests quickly with the current Python
	$(PYTHON) -m pytest --cov --cov-report=term:skip-covered

coverage: tests ## check code coverage quickly with the current Python
	$(PYTHON) -m coverage html
	@echo open htmlcov/index.html

lint: ## check the Python code syntax and style
	$(PYTHON) -m flake8 webdomains tests

format: ## fix the Python code syntax and imports order
	$(PYTHON) -m isort webdomains tests
	$(PYTHON) -m black webdomains tests

release: dist ## package and upload a release
	twine upload dist/*

dist: clean ## builds source and wheel package
	$(PYTHON) setup.py sdist
	$(PYTHON) setup.py bdist_wheel
	ls -l dist
