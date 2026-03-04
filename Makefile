.PHONY: setup install-uv install update test
UV ?= $(HOME)/.local/bin/uv

setup: install-uv install

install-uv:
	@if ! command -v uv >/dev/null 2>&1; then \
		echo "UV not installed. Installing UV..."; \
		curl -LsSf https://astral.sh/uv/install.sh | sh; \
		echo "UV installed at $(UV)."; \
	else \
		echo "UV is already installed: $$(uv --version)"; \
	fi
	@uv --version
install:
	@uv sync --all-extras && uv pip install -e .

update:
	@rm -f uv.lock
	@uv lock --upgrade && uv sync --all-extras && uv pip install -e .

test:
	@uv run pytest tests/unit_tests/ -v
