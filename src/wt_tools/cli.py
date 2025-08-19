"""
Command-line interface for wt-tools.

This module provides the main CLI entry point for the wt-tools package.
"""

import click
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text

from .demo import greet, process_data, calculate_stats

console = Console()


@click.group()
@click.version_option(version="0.1.0", prog_name="wt-tools")
@click.option("--verbose", "-v", is_flag=True, help="Enable verbose output")
def main(verbose: bool) -> None:
    """
    wt-tools - A collection of Python tools and utilities for development workflows.
    
    This tool provides various utilities for development, testing, and workflow automation.
    """
    if verbose:
        console.print("[bold blue]wt-tools[/bold blue] - Development utilities")
        console.print(f"Verbose mode: [green]enabled[/green]")


@main.command()
@click.argument("name")
@click.option("--greeting", "-g", help="Custom greeting message")
@click.option("--rich", "-r", is_flag=True, help="Use rich formatting")
def greet_cmd(name: str, greeting: str, rich: bool) -> None:
    """Greet someone with a customizable message."""
    result = greet(name, greeting)
    
    if rich:
        panel = Panel(
            Text(result, style="bold green"),
            title="Greeting",
            border_style="blue"
        )
        console.print(panel)
    else:
        click.echo(result)


@main.command()
@click.argument("data")
@click.option("--rich", "-r", is_flag=True, help="Use rich formatting")
def process(data: str, rich: bool) -> None:
    """Process different types of data using Python 3.10+ pattern matching."""
    result = process_data(data)
    
    if rich:
        panel = Panel(
            Text(result, style="bold yellow"),
            title="Data Processing Result",
            border_style="yellow"
        )
        console.print(panel)
    else:
        click.echo(result)


@main.command()
@click.argument("numbers", nargs=-1, type=float)
@click.option("--rich", "-r", is_flag=True, help="Use rich formatting")
def stats(numbers: tuple, rich: bool) -> None:
    """Calculate basic statistics for a list of numbers."""
    if not numbers:
        click.echo("Error: No numbers provided", err=True)
        return
    
    result = calculate_stats(list(numbers))
    
    if rich:
        table = Table(title="Statistics")
        table.add_column("Metric", style="cyan", no_wrap=True)
        table.add_column("Value", style="magenta")
        
        for key, value in result.items():
            table.add_row(key.title(), str(value))
        
        console.print(table)
    else:
        click.echo("Statistics:")
        for key, value in result.items():
            click.echo(f"  {key}: {value}")


@main.command()
def demo() -> None:
    """Run the demo showcasing all features."""
    console.print("[bold blue]Running wt-tools demo...[/bold blue]")
    
    # Greeting demo
    console.print("\n[bold]Greeting Demo:[/bold]")
    console.print(greet("World"))
    console.print(greet("Developer", "Welcome"))
    
    # Data processing demo
    console.print("\n[bold]Data Processing Demo:[/bold]")
    console.print(process_data("hello"))
    console.print(process_data(["apple", "banana", "cherry"]))
    console.print(process_data({"language": "Python", "version": "3.10"}))
    
    # Statistics demo
    console.print("\n[bold]Statistics Demo:[/bold]")
    numbers = [1.5, 2.7, 3.2, 4.1, 5.9]
    stats_result = calculate_stats(numbers)
    console.print(f"Statistics: {stats_result}")
    
    console.print("\n[bold green]Demo completed successfully![/bold green]")


@main.command()
def info() -> None:
    """Show information about wt-tools."""
    table = Table(title="wt-tools Information")
    table.add_column("Property", style="cyan", no_wrap=True)
    table.add_column("Value", style="magenta")
    
    table.add_row("Version", "0.1.0")
    table.add_row("Python Version", "3.10+")
    table.add_row("Description", "Development utilities and tools")
    table.add_row("License", "MIT")
    table.add_row("Repository", "https://github.com/yourusername/wt-tools")
    
    console.print(table)


if __name__ == "__main__":
    main()
