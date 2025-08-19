"""
Command-line interface for wt-tools.

This module provides the main CLI entry point for the wt-tools package using argparse and libtmux.
"""

import argparse
import sys
from typing import Optional

import libtmux
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

console = Console()


def create_session(session_name: str) -> None:
    """Create a new tmux session and attach to it."""
    try:
        server = libtmux.Server()
        
        # Check if session already exists
        existing_session = server.find_where({"session_name": session_name})
        if existing_session:
            console.print(f"[yellow]Session '{session_name}' already exists. Attaching...[/yellow]")
            existing_session.attach_session()
            return
        
        # Create new session
        session = server.new_session(session_name=session_name, attach=True)
        console.print(f"[green]Created and attached to session '{session_name}'[/green]")
        
    except Exception as e:
        console.print(f"[red]Error creating session: {e}[/red]")
        sys.exit(1)


def attach_session(session_name: str) -> None:
    """Attach to an existing tmux session."""
    try:
        server = libtmux.Server()
        session = server.find_where({"session_name": session_name})
        
        if not session:
            console.print(f"[red]Session '{session_name}' not found[/red]")
            console.print("[yellow]Available sessions:[/yellow]")
            for s in server.sessions:
                console.print(f"  - {s.session_name}")
            sys.exit(1)
        
        session.attach_session()
        console.print(f"[green]Attached to session '{session_name}'[/green]")
        
    except Exception as e:
        console.print(f"[red]Error attaching to session: {e}[/red]")
        sys.exit(1)


def new_window() -> None:
    """Create a new window in the current session."""
    try:
        server = libtmux.Server()
        current_session = server.get_current_session()
        
        if not current_session:
            console.print("[red]Not in a tmux session[/red]")
            sys.exit(1)
        
        new_win = current_session.new_window()
        console.print(f"[green]Created new window '{new_win.window_name}' (index: {new_win.window_index})[/green]")
        
    except Exception as e:
        console.print(f"[red]Error creating new window: {e}[/red]")
        sys.exit(1)


def goto_window(window_index: int) -> None:
    """Go to a specific window by index."""
    try:
        server = libtmux.Server()
        current_session = server.get_current_session()
        
        if not current_session:
            console.print("[red]Not in a tmux session[/red]")
            sys.exit(1)
        
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


def close_window() -> None:
    """Close the current window."""
    try:
        server = libtmux.Server()
        current_session = server.get_current_session()
        
        if not current_session:
            console.print("[red]Not in a tmux session[/red]")
            sys.exit(1)
        
        current_window = current_session.get_current_window()
        window_name = current_window.window_name
        window_index = current_window.window_index
        
        # Check if this is the last window
        if len(current_session.windows) == 1:
            console.print("[yellow]This is the last window. Closing will end the session.[/yellow]")
            response = input("Continue? (y/N): ")
            if response.lower() != 'y':
                console.print("[yellow]Window close cancelled[/yellow]")
                return
        
        current_window.kill_window()
        console.print(f"[green]Closed window {window_index}: {window_name}[/green]")
        
    except Exception as e:
        console.print(f"[red]Error closing window: {e}[/red]")
        sys.exit(1)


def list_sessions() -> None:
    """List all available tmux sessions."""
    try:
        server = libtmux.Server()
        sessions = server.sessions
        
        if not sessions:
            console.print("[yellow]No tmux sessions found[/yellow]")
            return
        
        console.print("[bold]Available tmux sessions:[/bold]")
        for session in sessions:
            status = "[green]●[/green]" if session.attached else "[gray]○[/gray]"
            console.print(f"  {status} {session.session_name}")
            
    except Exception as e:
        console.print(f"[red]Error listing sessions: {e}[/red]")
        sys.exit(1)


def list_windows() -> None:
    """List all windows in the current session."""
    try:
        server = libtmux.Server()
        current_session = server.get_current_session()
        
        if not current_session:
            console.print("[red]Not in a tmux session[/red]")
            sys.exit(1)
        
        console.print(f"[bold]Windows in session '{current_session.session_name}':[/bold]")
        for window in current_session.windows:
            status = "[green]●[/green]" if window.window_active else "[gray]○[/gray]"
            console.print(f"  {status} {window.window_index}: {window.window_name}")
            
    except Exception as e:
        console.print(f"[red]Error listing windows: {e}[/red]")
        sys.exit(1)


def main() -> None:
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="wt-tools - Tmux session and window management utilities",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  wt session new myproject     # Create and attach to new session
  wt session attach myproject  # Attach to existing session
  wt session list             # List all sessions
  wt window new               # Create new window
  wt window goto 3            # Go to window 3
  wt window close             # Close current window
  wt window list              # List windows in current session
        """
    )
    
    parser.add_argument('--version', action='version', version='wt-tools 0.1.0')
    parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose output')
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Session commands
    session_parser = subparsers.add_parser('session', help='Session management')
    session_subparsers = session_parser.add_subparsers(dest='session_command', help='Session commands')
    
    # session new
    new_parser = session_subparsers.add_parser('new', help='Create new session')
    new_parser.add_argument('session_name', help='Name of the new session')
    
    # session attach
    attach_parser = session_subparsers.add_parser('attach', help='Attach to session')
    attach_parser.add_argument('session_name', help='Name of the session to attach to')
    
    # session list
    session_subparsers.add_parser('list', help='List all sessions')
    
    # Window commands
    window_parser = subparsers.add_parser('window', help='Window management')
    window_subparsers = window_parser.add_subparsers(dest='window_command', help='Window commands')
    
    # window new
    window_subparsers.add_parser('new', help='Create new window')
    
    # window goto
    goto_parser = window_subparsers.add_parser('goto', help='Go to window')
    goto_parser.add_argument('window_index', type=int, help='Window index to go to')
    
    # window close
    window_subparsers.add_parser('close', help='Close current window')
    
    # window list
    window_subparsers.add_parser('list', help='List windows in current session')
    
    args = parser.parse_args()
    
    if args.verbose:
        console.print("[bold blue]wt-tools[/bold blue] - Tmux utilities")
        console.print(f"Verbose mode: [green]enabled[/green]")
    
    # Handle commands
    if args.command == 'session':
        if args.session_command == 'new':
            create_session(args.session_name)
        elif args.session_command == 'attach':
            attach_session(args.session_name)
        elif args.session_command == 'list':
            list_sessions()
        else:
            session_parser.print_help()
    
    elif args.command == 'window':
        if args.window_command == 'new':
            new_window()
        elif args.window_command == 'goto':
            goto_window(args.window_index)
        elif args.window_command == 'close':
            close_window()
        elif args.window_command == 'list':
            list_windows()
        else:
            window_parser.print_help()
    
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
