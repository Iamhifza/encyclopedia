# Developer entry points. Everything here is a thin wrapper over `enc`.

PYTHON ?= python3
VENV   := .venv
BIN    := $(VENV)/bin

.DEFAULT_GOAL := help

.PHONY: help
help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## ' $(MAKEFILE_LIST) \
	  | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-14s\033[0m %s\n", $$1, $$2}'

$(BIN)/python:
	$(PYTHON) -m venv $(VENV)

.PHONY: install
install: $(BIN)/python ## Create a virtualenv and install dependencies
	$(BIN)/pip install --upgrade pip
	$(BIN)/pip install -r requirements-dev.txt
	$(BIN)/pip install -e .

.PHONY: check
check: ## Validate the corpus (warnings are fatal)
	$(BIN)/python -m encyclopedia validate --strict

.PHONY: build
build: ## Generate build/docs and build/docs/api
	$(BIN)/python -m encyclopedia build

.PHONY: site
site: ## Render the static site into site/
	$(BIN)/python -m encyclopedia build --site

.PHONY: serve
serve: ## Live-reload preview at http://127.0.0.1:8000
	$(BIN)/python -m encyclopedia build --serve

.PHONY: batch
batch: ## Create seed entries from the backlog (BATCH=20 make batch)
	$(BIN)/python -m encyclopedia batch --limit $(or $(BATCH),20)
	$(BIN)/python -m encyclopedia validate --strict

.PHONY: todo
todo: ## Seed entries awaiting the full treatment, most connected first
	$(BIN)/python -m encyclopedia todo

.PHONY: stats
stats: ## Corpus and graph statistics
	$(BIN)/python -m encyclopedia stats

.PHONY: links
links: ## Check that every cited URL still resolves (needs network)
	$(BIN)/python -m encyclopedia lint-links

.PHONY: test
test: ## Run the test suite
	$(BIN)/python -m pytest -q

.PHONY: lint
lint: ## Lint the tooling
	$(BIN)/ruff check tools tests

.PHONY: clean
clean: ## Remove generated output
	rm -rf build site .pytest_cache .ruff_cache
	find . -name __pycache__ -type d -prune -exec rm -rf {} +
