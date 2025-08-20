"""
Utility functions for mux-tools.

This module provides common utility functions used across the package.
"""

import os
import libtmux
from libtmux.session import Session


def get_current_session() -> Session | None:
    """Get the current tmux session using environment variables."""
    tmux_env = os.environ.get('TMUX')
    if not tmux_env:
        return None
    
    parts = tmux_env.split(',')
    if len(parts) > 2:
        session_id = f"${parts[2]}"  # Prepend '$' as tmux IDs usually start with it
        server = libtmux.Server()
        return server.get_by_id(session_id)
    return None
