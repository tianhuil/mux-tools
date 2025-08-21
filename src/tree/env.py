"""
Environment management for the tree command.

This module provides functionality to manage tmux sessions and Docker environments
for development workflows.
"""

import sys
from pathlib import Path

import randomname  # type: ignore

from .config import TreeConfig, load_tree_config


def generate_env_name() -> str:
    """Generate a 3-word memorable name.

    Returns:
        A memorable 3-word name like 'cobra-felix-amateur'
    """
    # Generate 3 words using randomname
    # We'll use a verb, adjective, and noun to create memorable names
    name = randomname.generate("v", "adj", "n")
    return str(name)


async def start_docker_environment(config: TreeConfig) -> None:
    """Start Docker environment with the specified configuration.

    Args:
        config: TreeConfig instance with Docker and setup configuration
    """
    try:
        import dagger
    except ImportError:
        print(
            "Error: dagger package not found. Please install it with: pip install dagger-io"
        )
        sys.exit(1)

    # Generate environment name
    env_name = generate_env_name()

    # Get current directory
    current_dir = Path.cwd()

    # Start dagger client
    async with dagger.Connection() as client:
        # Pull the Docker image
        container = client.container().from_(config.docker_image)

        # Mount current directory to /base_dir
        container = container.with_mounted_directory(
            "/base_dir", client.host().directory(str(current_dir))
        )

        # Create work directory
        container = container.with_workdir("/work_dir")

        # Create worktree from /base_dir if remote_repo is provided
        if config.remote_repo:
            # Create worktree at /work_dir with a new branch
            container = container.with_exec(["git", "-C", "/base_dir", "worktree", "add", "/work_dir", env_name])

        # Run setup commands
        for cmd in config.setup_cmds:
            print(f"Running setup command: {cmd}")
            container = container.with_exec(cmd.split())

        # Start interactive shell
        print(f"Starting interactive shell in Docker container...")
        print(f"Environment name: {env_name}")
        print(f"Work directory: /work_dir")
        print(f"Base directory mounted at: /base_dir")

        # Note: dagger doesn't support interactive mode directly
        # We'll need to use a different approach for interactive mode
        # For now, we'll just show the container info
        print("Container prepared successfully!")
        print("To enter interactive mode, you can:")
        print(
            f"1. Use: docker run -it --rm -v {current_dir}:/base_dir {config.docker_image} /bin/sh"
        )
        print(f"2. Or use the worktree at: /work_dir")


async def start(config_path: str | Path | None = None) -> None:
    """Main entry point for starting the environment.

    Args:
        config_path: Optional path to configuration file
    """
    # Load configuration
    config = load_tree_config(config_path)

    # Start Docker environment
    await start_docker_environment(config)
