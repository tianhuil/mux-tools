"""
Command-line interface for mux-tools.

This module provides the main CLI entry point for the mux-tools package using Click.
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
