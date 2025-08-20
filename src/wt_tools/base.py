"""
Base CLI configuration for wt-tools.

This module provides the main CLI group using ClickAliasedGroup for alias support.
"""

import click
from click_aliases import ClickAliasedGroup
from rich.console import Console

console = Console()


@click.group(cls=ClickAliasedGroup)
@click.version_option(version='0.1.0', prog_name='wt-tools')
@click.option('-v', '--verbose', is_flag=True, help='Enable verbose output')
def cli(verbose: bool) -> None:
    """
    wt-tools - Tmux session and window management utilities.
    """
    if verbose:
        console.print("[bold blue]wt-tools[/bold blue] - Tmux utilities")
        console.print(f"Verbose mode: [green]enabled[/green]")


def main() -> None:
    """Main CLI entry point."""
    # Import CLI module to register command groups
    from . import cli as cli_module
    cli()


if __name__ == "__main__":
    main()
