SHELL=/bin/bash
PYTHON=python3
PYTHON_ENV=env

.PHONY: clean shell test sdist _release


all: test

clean:
	rm -rf $(PYTHON_ENV)

$(PYTHON_ENV): pyproject.toml
	rm -rf $(PYTHON_ENV) && \
	$(PYTHON) -m venv $(PYTHON_ENV) && \
	. $(PYTHON_ENV)/bin/activate && \
	pip install pip --upgrade && \
	pip install -e .[dev]

shell: | $(PYTHON_ENV)
	. $(PYTHON_ENV)/bin/activate && \
	rlpython $(args)

test: | $(PYTHON_ENV)
	. $(PYTHON_ENV)/bin/activate && \
	python test.py $(args)

sdist: | $(PYTHON_ENV)
	. $(PYTHON_ENV)/bin/activate && \
	rm -rf dist *.egg-info && \
	python -m build

_release: sdist
	. $(PYTHON_ENV)/bin/activate && \
	twine upload --config-file ~/.pypirc.fscherf dist/*
