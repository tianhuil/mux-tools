"""
Tree command entry point.

This module provides the main CLI entry point for the tree command.
"""

import click
import libtmux
from rich.console import Console

console = Console()


@click.command()
@click.argument('path', default='.')
@click.option('--max-depth', '-d', type=int, help='Maximum depth to traverse')
def main(path: str, max_depth: int | None) -> None:
    """Display directory tree structure."""
    try:
        # Create a new tmux session named 'tree-session'
        session_name = "tree-session"
        
        console.print(f"[blue]Creating new session '{session_name}'...[/blue]")
        server = libtmux.Server()
        
        # Kill existing session if it exists
        existing_session = server.find_where({"session_name": session_name})
        if existing_session:
            console.print(f"[yellow]Killing existing session '{session_name}'...[/yellow]")
            existing_session.kill_session()
        
        # Create new tmux session
        session = server.new_session(
            session_name=session_name,
            attach=False
        )
        
        # Get the first window and pane
        window = session.windows[0]
        pane = window.panes[0]
        
        # Send "echo hello" command to the pane
        pane.send_keys('echo hello', enter=True)
        
        # Attach to the session
        console.print(f"[green]Opening tmux session '{session_name}' with 'echo hello' command...[/green]")
        session.attach_session()
        
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        import sys
        sys.exit(1)


if __name__ == "__main__":
    main()