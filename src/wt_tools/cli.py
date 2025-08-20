"""
Command-line interface for wt-tools.

This module provides the main CLI entry point for the wt-tools package using Click.
"""

import click
from rich.console import Console

from . import session, window

console = Console()


from typing import Any

class AliasedGroup(click.Group):
    """A click group that supports aliases for commands."""
    
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self._aliases: dict[str, str] = {}
    
    def add_command(self, cmd: click.Command, name: str | None = None, alias: str | None = None) -> None:
        """Add a command with an optional alias."""
        super().add_command(cmd, name)
        if alias:
            self._aliases[alias] = name or cmd.name or ""
    
    def get_command(self, ctx: click.Context, cmd_name: str) -> click.Command | None:
        """Get command by name or alias."""
        # First try the normal command lookup
        cmd = super().get_command(ctx, cmd_name)
        if cmd is not None:
            return cmd
        
        # Then try aliases
        if cmd_name in self._aliases:
            return super().get_command(ctx, self._aliases[cmd_name])
        
        return None


@click.group(cls=AliasedGroup)
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
@cli.group()
def session_group() -> None:
    """Session management commands (shortcuts: s)"""
    pass


session_group.add_command(session.new, 'new')
session_group.add_command(session.attach, 'attach')
session_group.add_command(session.list_sessions, 'list')
session_group.add_command(session.list_detailed, 'list-detailed')
session_group.add_command(session.kill, 'kill')
session_group.add_command(session.kill_all, 'kill-all')


# Window commands
@cli.group()
def window_group() -> None:
    """Window management commands (shortcuts: w)"""
    pass


window_group.add_command(window.new, 'new')
window_group.add_command(window.goto, 'goto')
window_group.add_command(window.close, 'close')
window_group.add_command(window.list_windows, 'list')


# Add aliases for command groups
cli.add_command(session_group, 'session', alias='s')
cli.add_command(window_group, 'window', alias='w')


def main() -> None:
    """Main CLI entry point."""
    cli()


if __name__ == "__main__":
    main()
