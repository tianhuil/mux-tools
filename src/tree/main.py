"""
Tree command entry point.

This module provides the main CLI entry point for the tree command.
"""

import asyncio

import click
from rich.console import Console

from .env import start

console = Console()

@click.group()
def main() -> None:
    """Tree command for environment management and visualization."""
    pass


@main.command()
@click.option('--config', '-c', type=str, help='Path to configuration file')
def start_env(config: str | None) -> None:
    """Start development environment with tmux and Docker."""
    try:
        asyncio.run(start(config))
        console.print("[green]Environment started successfully![/green]")
    except Exception as e:
        console.print(f"[red]Error starting environment: {e}[/red]")
        import sys
        sys.exit(1)


@main.command()
def sample() -> None:
    """Tree command for environment management and visualization."""
    click.echo("Running sample command")

if __name__ == "__main__":
    main()