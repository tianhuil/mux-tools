"""
Tree package for directory tree visualization.

This package provides utilities for displaying directory structures in a tree format.
"""

__version__ = "0.1.0"
__author__ = "Your Name"
__email__ = "your.email@example.com"

from .config import TreeConfig
from .env import Environment, EnvironmentConfig
from .main import main

__all__ = [
    "__version__",
    "__author__", 
    "__email__",
    "main",
    "TreeConfig",
    "Environment",
    "EnvironmentConfig",
]
