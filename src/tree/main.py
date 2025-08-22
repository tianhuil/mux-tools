"""
Tree command entry point.

This module provides the main CLI entry point for the tree command.
"""

import asyncio

import click
from rich.console import Console

from .env import Environment, EnvironmentConfig

console = Console()

@click.group()
def main() -> None:
    """Tree command for environment management and visualization."""
    pass


@main.command()
@click.option('--config', '-c', type=str, help='Path to configuration file')
def start(config: str | None) -> None:
    """Start development environment with tmux and Docker."""
    try:
        asyncio.run(Environment.load_from_config(config).start())
        console.print("[green]Environment started successfully![/green]")
    except Exception as e:
        console.print(f"[red]Error starting environment: {e}[/red]")
        console.print(f"[yellow]Error type: {type(e).__name__}[/yellow]")
        console.print(f"[yellow]Error details: {str(e)}[/yellow]")
        
        # Print traceback for debugging
        import traceback
        console.print("[dim]Traceback:[/dim]")
        for line in traceback.format_exc().split('\n'):
            if line.strip():
                console.print(f"[dim]{line}[/dim]")
        
        import sys
        sys.exit(1)


@main.command()
@click.option('--config', '-c', type=str, help='Path to configuration file')
@click.option('--detail', '-d', is_flag=True, help='Show details')
def list(config: str | None, detail: bool = False) -> None:
    """Create a new environment."""
    env_config = Environment.load_from_config(config).env_config

    console.print(f"[bold]Environments for {env_config.config.repo_path}:[/bold]")
    for env in env_config.list_work_trees():
        console.print(f"[green]{env.env_name}[/green]")
        if detail:
            console.print(f"[dim]Path: {env.work_path}[/dim]")
            console.print(f"[dim]Image: {env.image_name}[/dim]")
            console.print(f"[dim]Docker container: {env.image_name}[/dim]")


@main.command()
@click.argument('env', type=str, required=True)
@click.option('--config', '-c', type=str, help='Path to configuration file')
def join(env: str, config: str | None) -> None:
    """Join an environment."""
    environment = Environment.load_from_config(config, env)
    environment.join()

@main.command()
@click.argument('env', type=str, required=True)
@click.option('--config', '-c', type=str, help='Path to configuration file')
def stop(env: str, config: str | None) -> None:
    """Stop an environment."""
    environment = Environment.load_from_config(config, env)
    asyncio.run(environment.remove())  

@main.command()
def sample() -> None:
    """Tree command for environment management and visualization."""
    click.echo("Running sample command")

if __name__ == "__main__":
    main()