#!/usr/bin/env python3
"""
Setup script for mux-tools development environment.
"""

import subprocess
import sys
from pathlib import Path


def run_command(cmd: str, check: bool = True) -> subprocess.CompletedProcess:
    """Run a shell command."""
    print(f"Running: {cmd}")
    result = subprocess.run(cmd, shell=True, check=check)
    return result


def main():
    """Set up the development environment."""
    print("Setting up mux-tools development environment...")
    
    # Check if uv is installed
    try:
        run_command("uv --version")
    except subprocess.CalledProcessError:
        print("Error: uv is not installed. Please install it first:")
        print("curl -LsSf https://astral.sh/uv/install.sh | sh")
        sys.exit(1)
    
    # Create virtual environment
    print("\nCreating virtual environment...")
    run_command("uv venv --python 3.10")
    
    # Install dependencies
    print("\nInstalling dependencies...")
    run_command("uv pip install -e .[dev]")
    
    # Install pre-commit hooks
    print("\nInstalling pre-commit hooks...")
    run_command("uv run pre-commit install")
    
    # Run tests to verify setup
    print("\nRunning tests to verify setup...")
    run_command("uv run pytest")
    
    print("\n✅ Setup complete!")
    print("\nNext steps:")
    print("1. Activate the virtual environment: source .venv/bin/activate")
    print("2. Try the CLI: uv run mux --help")
    print("3. Run the demo: uv run mux demo")


if __name__ == "__main__":
    main()
