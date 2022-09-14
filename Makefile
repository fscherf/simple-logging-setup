SHELL=/bin/bash
PYTHON=python3

PYTHON_ENV_ROOT=envs
PYTHON_DEVELOPMENT_ENV=$(PYTHON_ENV_ROOT)/$(PYTHON)-development
PYTHON_PACKAGING_ENV=$(PYTHON_ENV_ROOT)/$(PYTHON)-packaging

.PHONY: clean doc sdist shell freeze test

all: test

# environments ################################################################
# development
$(PYTHON_DEVELOPMENT_ENV): REQUIREMENTS.development.txt setup.py
	rm -rf $(PYTHON_DEVELOPMENT_ENV) && \
	$(PYTHON) -m venv $(PYTHON_DEVELOPMENT_ENV) && \
	. $(PYTHON_DEVELOPMENT_ENV)/bin/activate && \
	pip install pip --upgrade && \
	pip install -r ./REQUIREMENTS.development.txt

# packaging
$(PYTHON_PACKAGING_ENV): REQUIREMENTS.packaging.txt setup.py
	rm -rf $(PYTHON_PACKAGING_ENV) && \
	$(PYTHON) -m venv $(PYTHON_PACKAGING_ENV) && \
	. $(PYTHON_PACKAGING_ENV)/bin/activate && \
	pip install --upgrade pip && \
	pip install -r REQUIREMENTS.packaging.txt

clean:
	rm -rf $(PYTHON_ENV_ROOT)

shell: | $(PYTHON_DEVELOPMENT_ENV)
	. $(PYTHON_DEVELOPMENT_ENV)/bin/activate && \
	rlpython

freeze: | $(PYTHON_DEVELOPMENT_ENV)
	. $(PYTHON_DEVELOPMENT_ENV)/bin/activate && \
	pip freeze

dev-env: | $(PYTHON_DEVELOPMENT_ENV)

# testing #####################################################################
test: | $(PYTHON_DEVELOPMENT_ENV)
	. $(PYTHON_DEVELOPMENT_ENV)/bin/activate && \
	python test.py

# packaging ###################################################################
sdist: | $(PYTHON_PACKAGING_ENV)
	. $(PYTHON_PACKAGING_ENV)/bin/activate && \
	rm -rf dist *.egg-info && \
	./setup.py sdist

_release: sdist
	. $(PYTHON_PACKAGING_ENV)/bin/activate && \
	twine upload --config-file ~/.pypirc.fscherf dist/*
