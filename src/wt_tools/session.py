"""
Session management commands for wt-tools.

This module provides Click commands for managing tmux sessions.
"""

import os
import sys

import click
import libtmux
from rich.console import Console

console = Console()


@click.command()
@click.argument('session_name')
def new(session_name: str) -> None:
    """Create a new tmux session and attach to it."""
    try:
        console.print(f"[blue]Creating new session '{session_name}'...[/blue]")
        server = libtmux.Server()
        
        # Create session without attaching first
        current_dir = os.getcwd()
        
        session = server.new_session(
            session_name=session_name, 
            attach=False,
            start_directory=current_dir
        )
        
        session.attach_session()

    except Exception as e:
        console.print(f"[red]Error creating session: {e}[/red]")
        sys.exit(1)


@click.command()
@click.argument('session_name')
def attach(session_name: str) -> None:
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
        
    except Exception as e:
        console.print(f"[red]Error attaching to session: {e}[/red]")
        sys.exit(1)


@click.command()
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
            # Get session details
            status = "[green]●[/green]" if session.session_attached else "[gray]○[/gray]"
            window_count = len(session.windows)
            creation_time = getattr(session, 'session_created', 'Unknown')
            
            # Format creation time if available
            if creation_time != 'Unknown':
                try:
                    from datetime import datetime
                    creation_time = datetime.fromtimestamp(int(creation_time)).strftime('%Y-%m-%d %H:%M')
                except (ValueError, TypeError):
                    creation_time = 'Unknown'
            
            console.print(f"  {status} {session.session_name} ({window_count} windows, created: {creation_time})")
            
    except Exception as e:
        console.print(f"[red]Error listing sessions: {e}[/red]")
        sys.exit(1)


@click.command()
def list_detailed() -> None:
    """List all tmux sessions with detailed information."""
    try:
        server = libtmux.Server()
        sessions = server.sessions
        
        if not sessions:
            console.print("[yellow]No tmux sessions found[/yellow]")
            return
        
        console.print("[bold]Detailed tmux session information:[/bold]")
        console.print()
        
        for session in sessions:
            # Session header
            status_icon = "[green]●[/green]" if session.session_attached else "[gray]○[/gray]"
            status_text = "Attached" if session.session_attached else "Detached"
            
            console.print(f"{status_icon} [bold]{session.session_name}[/bold] - {status_text}")
            
            # Session details
            window_count = len(session.windows)
            console.print(f"  Windows: {window_count}")
            
            # Show windows in this session
            if session.windows:
                console.print("  Window list:")
                for window in session.windows:
                    window_status = "[green]●[/green]" if window.window_active else "[gray]○[/gray]"
                    console.print(f"    {window_status} {window.window_index}: {window.window_name}")
            
            console.print()  # Empty line between sessions
            
    except Exception as e:
        console.print(f"[red]Error listing detailed sessions: {e}[/red]")
        sys.exit(1)


@click.command()
@click.argument('session_name')
@click.option('-f', '--force', is_flag=True, help='Force kill without confirmation')
def kill(session_name: str, force: bool) -> None:
    """Kill a specific tmux session."""
    try:
        server = libtmux.Server()
        session = server.find_where({"session_name": session_name})
        
        if not session:
            console.print(f"[red]Session '{session_name}' not found[/red]")
            console.print("[yellow]Available sessions:[/yellow]")
            for s in server.sessions:
                console.print(f"  - {s.session_name}")
            sys.exit(1)
        
        # Check if session is attached and warn user
        if session.session_attached and not force:
            console.print(f"[yellow]Warning: Session '{session_name}' is currently attached.[/yellow]")
            response = input("Are you sure you want to kill it? (y/N): ")
            if response.lower() != 'y':
                console.print("[yellow]Session kill cancelled[/yellow]")
                return
        
        session.kill_session()
        console.print(f"[green]Killed session '{session_name}'[/green]")
        
    except Exception as e:
        console.print(f"[red]Error killing session: {e}[/red]")
        sys.exit(1)


@click.command()
@click.option('-e', '--except', 'except_session', help='Session name to keep')
@click.option('-f', '--force', is_flag=True, help='Force kill without confirmation')
def kill_all(except_session: str | None, force: bool) -> None:
    """Kill all tmux sessions, optionally excepting one."""
    try:
        server = libtmux.Server()
        sessions = server.sessions
        
        if not sessions:
            console.print("[yellow]No tmux sessions found[/yellow]")
            return
        
        # Filter sessions to kill
        sessions_to_kill = []
        for session in sessions:
            if except_session and session.session_name == except_session:
                continue
            sessions_to_kill.append(session)
        
        if not sessions_to_kill:
            console.print(f"[yellow]No sessions to kill (keeping '{except_session}')[/yellow]")
            return
        
        # Show what will be killed
        console.print(f"[yellow]Will kill {len(sessions_to_kill)} session(s):[/yellow]")
        for session in sessions_to_kill:
            status = " (attached)" if session.session_attached else ""
            console.print(f"  - {session.session_name}{status}")
        
        if not force:
            response = input("Are you sure? (y/N): ")
            if response.lower() != 'y':
                console.print("[yellow]Session kill cancelled[/yellow]")
                return
        
        # Kill sessions
        killed_count = 0
        for session in sessions_to_kill:
            try:
                session.kill_session()
                killed_count += 1
                console.print(f"[green]Killed session '{session.session_name}'[/green]")
            except Exception as e:
                console.print(f"[red]Error killing session '{session.session_name}': {e}[/red]")
        
        if except_session:
            console.print(f"[green]Killed {killed_count} sessions, kept '{except_session}'[/green]")
        else:
            console.print(f"[green]Killed {killed_count} sessions[/green]")
        
    except Exception as e:
        console.print(f"[red]Error killing sessions: {e}[/red]")
        sys.exit(1)
