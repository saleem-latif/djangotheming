
help: ## display this help message
	@echo "Please use \`make <target>' where <target> is one of"
	@perl -nle'print $& if m{^[\.a-zA-Z_-]+:.*?## .*$$}' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m  %-25s\033[0m %s\n", $$1, $$2}'

clean: ## remove generated byte code, coverage reports, and build artifacts
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -rf {} +
	find . -name '*~' -exec rm -f {} +
	coverage erase
	rm -fr build/
	rm -fr dist/
	rm -fr *.egg-info

upgrade: ## update the requirements/*.txt files with the latest packages satisfying requirements/*.in
	pip install -q pip-tools
	pip-compile --upgrade -o requirements/base.txt requirements/base.in
	pip-compile --upgrade -o requirements/dev.txt requirements/base.in requirements/dev.in requirements/quality.in requirements/test.in
	pip-compile --upgrade -o requirements/test.txt requirements/base.in requirements/test.in
	pip-compile --upgrade -o requirements/quality.txt requirements/base.in requirements/quality.in requirements/test.in

requirements: ## Install requirements for the development environment
	pip install -qr requirements/dev.txt --exists-action w
	pip-sync requirements/base.txt requirements/dev.txt requirements/test.txt


quality: clean
	tox -e quality

test: clean ## run tests in the current virtualenv
	pip install -qr requirements/test.txt --exists-action w
	py.test


validate: quality test

.PHONY: clean help upgrade requirements validate test quality
