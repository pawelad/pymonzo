# Source: http://clarkgrubb.com/makefile-style-guide
MAKEFLAGS += --warn-undefined-variables
.DEFAULT_GOAL := help

.PHONY: install
install: ## Install pymonzo in editable mode
	python -m pip install --upgrade pip wheel
	python -m pip install --editable ".[dev]"

.PHONY: build
build: ## Build pumonzo
	python -m flit build

.PHONY: publish
publish: ## Pyblish pymonzo
	python -m flit publish

.PHONY: format
format: ## Format code
	black src tests && isort src tests

.PHONY: test
test: ## Run tests
	tox --parallel

.PHONY: clean
clean: ## Clean dev artifacts
	rm -rf dist/ .mypy_cache/ .pytest_cache/ .tox/

# Source: https://www.client9.com/self-documenting-makefiles/
.PHONY: help
help: ## Show help message
	@awk -F ':|##' '/^[^\t].+?:.*?##/ {\
	printf "\033[36m%-40s\033[0m %s\n", $$1, $$NF \
	}' $(MAKEFILE_LIST)
