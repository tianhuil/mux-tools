.PHONY: help install install-dev test test-cov lint format type-check clean build run setup

# Default target
help:
	@echo "Available commands:"
	@echo "  install      - Install production dependencies"
	@echo "  install-dev  - Install development dependencies"
	@echo "  test         - Run tests"
	@echo "  test-cov     - Run tests with coverage"
	@echo "  lint         - Run linting (flake8)"
	@echo "  format       - Format code (black + isort)"
	@echo "  type-check   - Run type checking (mypy)"
	@echo "  clean        - Clean build artifacts"
	@echo "  build        - Build package"
	@echo "  run          - Run the main module"
	@echo "  setup        - Initial project setup"

# Install production dependencies
install:
	uv pip install -e .

# Install development dependencies
install-dev:
	uv pip install -e ".[dev]"

# Run tests
test:
	uv run pytest

# Run tests with coverage
test-cov:
	uv run pytest --cov=src --cov-report=html --cov-report=term-missing

# Run linting
lint:
	uv run flake8 src/ tests/

# Format code
format:
	uv run black src/ tests/
	uv run isort src/ tests/

# Run type checking
type-check:
	uv run mypy src/

# Clean build artifacts
clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	rm -rf htmlcov/
	rm -rf .coverage
	find . -type d -name __pycache__ -delete
	find . -type f -name "*.pyc" -delete

# Build package
build:
	uv run python -m build

# Run the main module
run:
	uv run python -m your_project_name.main

# Initial project setup
setup: install-dev
	@echo "Setting up pre-commit hooks..."
	uv run pre-commit install
	@echo "Project setup complete!"

# Quick quality check
check: format lint type-check test

# Install pre-commit hooks
pre-commit-install:
	uv run pre-commit install

# Update dependencies
update:
	uv lock --upgrade
	uv pip install -e ".[dev]"

# Show dependency tree
deps:
	uv tree

# Run security check
security:
	uv run bandit -r src/ -f json -o bandit-report.json

# Create new virtual environment
venv:
	uv venv --python 3.10

# Activate virtual environment (macOS/Linux)
activate:
	@echo "Run: source .venv/bin/activate"

# Activate virtual environment (Windows)
activate-win:
	@echo "Run: .venv\Scripts\activate"
