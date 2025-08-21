"""
Environment management for the tree command.

This module provides functionality to manage tmux sessions and Docker environments
for development workflows.
"""

import sys
from pathlib import Path

import coolname  # type: ignore

from .config import TreeConfig, load_tree_config


def generate_env_name() -> str:
    """Generate a 3-word memorable name.

    Returns:
        A memorable 3-word name like 'cobra-felix-amateur'
    """
    name = coolname.generate_slug(3)
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
            if cmd.startswith("#"):
                continue

            print(f"Running setup command: {cmd}")
            # Use shell to execute commands that may contain operators like &&
            container = container.with_exec(["sh", "-c", cmd])

        # Build the container as a local Docker image
        image_name = f"mux-env-{config.repo_name}-{env_name}"
        print(f"Building container as Docker image: {image_name}")
        
        # Export the container as a local Docker image with the specified tag
        await container.export_image(image_name)
        
        print(f"Container built as local image: {image_name}")
        
    # Run the container in interactive mode
    import subprocess
    print(f"Starting interactive shell in container...")
    subprocess.run([
        "docker", "run", "-it", "--rm", 
        "-v", f"{current_dir}:/base_dir",
        image_name, "/bin/sh"
    ])


async def start(config_path: str | Path | None = None) -> None:
    """Main entry point for starting the environment.

    Args:
        config_path: Optional path to configuration file
    """
    # Load configuration
    config = load_tree_config(config_path)

    # Start Docker environment
    await start_docker_environment(config)
