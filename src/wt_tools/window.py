"""
Window management commands for wt-tools.

This module provides Click commands for managing tmux windows.
"""

import sys

import click
from click_aliases import ClickAliasedGroup
import libtmux
from rich.console import Console

from .util import get_current_session

console = Console()



@click.command()
def new() -> None:
    """Create a new window in the current session."""
    try:
        current_session = get_current_session()
        if not current_session:
            console.print("[red]Not in a tmux session[/red]")
            sys.exit(1)
        
        new_win = current_session.new_window()
        console.print(f"[green]Created and switched to new window '{new_win.window_name}' (index: {new_win.window_index})[/green]")
        new_win.select_window()
        
    except Exception as e:
        console.print(f"[red]Error creating new window: {e}[/red]")
        sys.exit(1)


@click.command()
@click.argument('window_index', type=int)
def goto(window_index: int) -> None:
    """Go to a specific window by index."""
    try:
        server = libtmux.Server()
        
        # Find the currently attached session
        attached_sessions = server.sessions.filter(session_attached=True)
        if not attached_sessions:
            console.print("[red]Not in a tmux session[/red]")
            sys.exit(1)
        
        current_session = attached_sessions[0]
        
        # Find window by index
        window = current_session.find_where({"window_index": window_index})
        if not window:
            console.print(f"[red]Window {window_index} not found[/red]")
            console.print("[yellow]Available windows:[/yellow]")
            for w in current_session.windows:
                console.print(f"  {w.window_index}: {w.window_name}")
            sys.exit(1)
        
        window.select_window()
        console.print(f"[green]Switched to window {window_index}: {window.window_name}[/green]")
        
    except Exception as e:
        console.print(f"[red]Error switching to window: {e}[/red]")
        sys.exit(1)


@click.command()
def close() -> None:
    """Close the current window."""
    try:
        server = libtmux.Server()
        
        # Find the currently attached session
        attached_sessions = server.sessions.filter(session_attached=True)
        if not attached_sessions:
            console.print("[red]Not in a tmux session[/red]")
            sys.exit(1)
        
        current_session = attached_sessions[0]
        current_window = current_session.active_window
        window_name = current_window.window_name
        window_index = current_window.window_index
        
        # Check if this is the last window
        if len(current_session.windows) == 1:
            console.print("[yellow]This is the last window. Closing will end the session.[/yellow]")
            response = input("Continue? (y/N): ")
            if response.lower() != 'y':
                console.print("[yellow]Window close cancelled[/yellow]")
                return
        
        current_window.kill()
        console.print(f"[green]Closed window {window_index}: {window_name}[/green]")
        
    except Exception as e:
        console.print(f"[red]Error closing window: {e}[/red]")
        sys.exit(1)


@click.command()
def list() -> None:
    """List all windows in the current session."""
    try:
        server = libtmux.Server()
        
        # Find the currently attached session
        attached_sessions = server.sessions.filter(session_attached=True)
        if not attached_sessions:
            console.print("[red]Not in a tmux session[/red]")
            sys.exit(1)
        
        current_session = attached_sessions[0]
        console.print(f"[bold]Windows in session '{current_session.session_name}':[/bold]")
        for window in current_session.windows:
            status = "[green]●[/green]" if window.window_active else "[gray]○[/gray]"
            console.print(f"  {status} {window.window_index}: {window.window_name}")
            
    except Exception as e:
        console.print(f"[red]Error listing windows: {e}[/red]")
        sys.exit(1)


def create_window_group(cli_group: click.Group) -> click.Group:
    """Create and configure the window command group."""
    @cli_group.group(name='window', aliases=['w'], cls=ClickAliasedGroup)
    def window_group() -> None:
        """Window management commands."""
        pass
    
    # Add aliases for window commands
    window_group.add_command(new, 'n')
    window_group.add_command(goto, 'g')
    window_group.add_command(close, 'c')
    window_group.add_command(list, 'l')

    return window_group
