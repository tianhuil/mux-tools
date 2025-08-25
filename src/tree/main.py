"""
Tree command entry point.

This module provides the main CLI entry point for the tree command.
"""

import asyncio

import click
from rich.console import Console

from tree.config import ConfigLoader

from .env import Environment, EnvironmentConfig

console = Console()


@click.group()
def main() -> None:
    """Tree command for environment management and visualization."""
    pass


@main.command()
@click.option("--config", "-c", type=str, help="Path to configuration file")
@click.option("--repo-only", "-r", is_flag=True, help="Create a new repository only")
def create(config: str | None, repo_only: bool = False) -> None:
    """Create a new development environment."""
    try:
        environment = Environment.load_from_config(config)
        asyncio.run(environment.create(repo_only))
        if repo_only:
            console.print("[green]Repository created successfully![/green]")
            console.print(
                f"Repo Directory: [bold]{environment.env_config.work_path}[/bold]"
            )
        else:
            console.print("[green]Environment created successfully![/green]")
            console.print(
                f"To join the environment, run [bold]tree join {environment.env_config.env_name}[/bold]"
            )
    except Exception as e:
        console.print(f"[red]Error creating environment: {e}[/red]")
        console.print(f"[yellow]Error type: {type(e).__name__}[/yellow]")
        console.print(f"[yellow]Error details: {str(e)}[/yellow]")

        # Print traceback for debugging
        import traceback

        console.print("[dim]Traceback:[/dim]")
        for line in traceback.format_exc().split("\n"):
            if line.strip():
                console.print(f"[dim]{line}[/dim]")

        import sys

        sys.exit(1)


@main.command()
@click.option("--config", "-c", type=str, help="Path to configuration file")
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
        for line in traceback.format_exc().split("\n"):
            if line.strip():
                console.print(f"[dim]{line}[/dim]")

        import sys

        sys.exit(1)


@main.command()
@click.option("--config", "-c", type=str, help="Path to configuration file")
@click.option("--detail", "-d", is_flag=True, help="Show details")
def list(config: str | None, detail: bool = False) -> None:
    """Create a new environment."""
    env_config = Environment.load_from_config(config).env_config

    console.print(
        f"Environments for [bold][blue]{env_config.config.repo_name}[/blue]:[/bold]"
    )
    for env in env_config.list_work_trees():
        console.print(f"[green]{env.env_name}[/green]")
        if detail:
            console.print(f"  [dim]Path: {env.work_path}[/dim]")
            console.print(f"  [dim]Image: {env.image_name}[/dim]")
            console.print(f"  [dim]Docker container: {env.image_name}[/dim]")


@main.command()
@click.argument("env", type=str, required=True)
@click.option("--config", "-c", type=str, help="Path to configuration file")
def join(env: str, config: str | None) -> None:
    """Join an environment."""
    environment = Environment.load_from_config(config, env)
    environment.join()


@main.command()
@click.argument("env", type=str, required=True)
@click.option("--config", "-c", type=str, help="Path to configuration file")
@click.option("--repo-only", "-r", is_flag=True, help="Remove repository only")
def remove(env: str, config: str | None, repo_only: bool = False) -> None:
    """Remove an environment."""
    environment = Environment.load_from_config(config, env)
    asyncio.run(environment.remove(repo_only))


@main.command()
@click.option("--config", "-c", type=str, help="Path to configuration file")
def info(config: str | None) -> None:
    """Show information about an environment."""
    tree_config = ConfigLoader(config).load_config()
    console.print(f"Repository:   [bold][blue]{tree_config.repo_name}[/blue]")
    console.print(f"Worktree:     [bold][blue]{tree_config.repo_path}[/blue]")
    console.print(f"Image:        [bold][blue]{tree_config.docker_image}[/blue]")


@main.command()
@click.argument("remote", type=str, required=True)
@click.argument("env", type=str, required=True)
@click.option("--config", "-c", type=str, help="Path to configuration file")
def push(remote: str, env: str, config: str | None) -> None:
    """Push changes to a remote repository."""
    environment = Environment.load_from_config(config, env)
    environment.push(remote)


if __name__ == "__main__":
    main()
