"""
Command-line interface for wt-tools.

This module provides the main CLI entry point for the wt-tools package using Click.
"""

from .base import cli
from . import session, window

# Create and register command groups
session.create_session_group(cli)
window.create_window_group(cli)


def main() -> None:
    """Main CLI entry point."""
    cli()


if __name__ == "__main__":
    main()
