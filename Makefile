#################################################################################
# GLOBALS                                                                       #
#################################################################################

PROJECT_NAME = pitsurf
PYTHON_VERSION = 3.12
PYTHON_INTERPRETER = python
VENV_DIR = venv_pit
DATA_DIR = data

#################################################################################
# ENVIRONMENT                                                                   #
#################################################################################

## Create venv (activate conda env, e.g. conda_312, before running this)
create_venv:
	$(PYTHON_INTERPRETER) -m venv $(VENV_DIR)
	@echo ">>> venv created. Activate with: source $(VENV_DIR)/bin/activate"

## Install package in editable mode with dev extras
requirements:
	$(PYTHON_INTERPRETER) -m pip install --upgrade pip
	$(PYTHON_INTERPRETER) -m pip install -e ".[dev]"

#################################################################################
# DATA                                                                          #
#################################################################################

## Fetch raw DEM tile into data/raw (no filtering here)
data_gen:
	$(PYTHON_INTERPRETER) data_gen.py --out-dir $(DATA_DIR)/raw

## Subsample DEM into sparse survey-style points -> data/processed
preprocess:
	$(PYTHON_INTERPRETER) preprocessing.py --in-dir $(DATA_DIR)/raw --out-dir $(DATA_DIR)/processed

#################################################################################
# QUALITY                                                                       #
#################################################################################

## Run tests
test:
	$(PYTHON_INTERPRETER) -m pytest -q

## Format with black
format:
	$(PYTHON_INTERPRETER) -m black pitsurf tests *.py

## Strip notebook outputs before committing
strip_notebooks:
	$(PYTHON_INTERPRETER) -m nbstripout notebooks/*.ipynb

## Remove caches and build artifacts
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	rm -rf build dist *.egg-info .pytest_cache

#################################################################################
# SELF DOCUMENTING COMMANDS                                                     #
#################################################################################

.DEFAULT_GOAL := help

help:
	@echo "Available targets:"
	@awk '/^## /{desc=substr($$0,4); next} /^[a-z_]+:/{split($$0,a,":"); printf "  \033[36m%-20s\033[0m %s\n", a[1], desc; desc=""}' $(MAKEFILE_LIST)

.PHONY: create_venv requirements data_gen preprocess test format strip_notebooks clean help
