# Source: http://clarkgrubb.com/makefile-style-guide
MAKEFLAGS += --warn-undefined-variables
.DEFAULT_GOAL := help

.PHONY: install
install: ## Install pymonzo in editable mode
	python -m pip install --upgrade pip wheel
	python -m pip install --editable ".[dev]"

.PHONY: format
format: ## Format code
	black src tests && isort src tests

.PHONY: test
test: ## Run tests
	tox --parallel

.PHONY: docs-build
docs-build: ## Build docs
	mkdocs build

.PHONY: docs-serve
docs-serve: ## Serve docs
	mkdocs serve

.PHONY: build
build: ## Build pymonzo
	python -m flit build

.PHONY: publish
publish: ## Publish pymonzo
	python -m flit publish

.PHONY: clean
clean: ## Clean dev artifacts
	rm -rf .mypy_cache/ .pytest_cache/ .tox/ dist/ site/

# Source: https://www.client9.com/self-documenting-makefiles/
.PHONY: help
help: ## Show help message
	@awk -F ':|##' '/^[^\t].+?:.*?##/ {\
	printf "\033[36m%-40s\033[0m %s\n", $$1, $$NF \
	}' $(MAKEFILE_LIST)
