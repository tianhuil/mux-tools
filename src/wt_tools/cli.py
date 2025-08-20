"""
Command-line interface for wt-tools.

This module provides the main CLI entry point for the wt-tools package using Click.
"""

import click
from rich.console import Console

from . import session, window

console = Console()


@click.group()
@click.version_option(version='0.1.0', prog_name='wt-tools')
@click.option('-v', '--verbose', is_flag=True, help='Enable verbose output')
def cli(verbose: bool) -> None:
    """
    wt-tools - Tmux session and window management utilities.
    """
    if verbose:
        console.print("[bold blue]wt-tools[/bold blue] - Tmux utilities")
        console.print(f"Verbose mode: [green]enabled[/green]")


# Session commands
@cli.group(name='s')
def session_group() -> None:
    """Session management commands."""
    pass


session_group.add_command(session.new, 'new')
session_group.add_command(session.attach, 'attach')
session_group.add_command(session.list_sessions, 'list')
session_group.add_command(session.list_detailed, 'list-detailed')
session_group.add_command(session.kill, 'kill')
session_group.add_command(session.kill_all, 'kill-all')


# Window commands
@cli.group(name='w')
def window_group() -> None:
    """Window management commands."""
    pass


window_group.add_command(window.new, 'new')
window_group.add_command(window.goto, 'goto')
window_group.add_command(window.close, 'close')
window_group.add_command(window.list_windows, 'list')


def main() -> None:
    """Main CLI entry point."""
    cli()


if __name__ == "__main__":
    main()
