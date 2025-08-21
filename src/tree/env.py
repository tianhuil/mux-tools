"""
Environment management for the tree command.

This module provides functionality to manage tmux sessions and Docker environments
for development workflows.
"""

import subprocess
import sys
from pathlib import Path

import click
import coolname  # type: ignore

from .config import TreeConfig, load_tree_config


def generate_env_name() -> str:
    """Generate a 3-word memorable name.

    Returns:
        A memorable 3-word name like 'cobra-felix-amateur'
    """
    name = coolname.generate_slug(3)
    return str(name)


def get_worktree_path(repo_name: str, branch_name: str) -> Path:
    """Get the path for the worktree.
    
    Args:
        repo_name: Name of the repository
        branch_name: Name of the branch
        
    Returns:
        Path to the worktree directory
    """
    config_dir = Path.home() / ".config" / "tree" / "worktrees"
    worktree_path = config_dir / repo_name / branch_name
    return worktree_path


def checkout_worktree(config: TreeConfig, branch_name: str) -> Path:
    """Checkout a worktree to the specified location.
    
    Args:
        config: TreeConfig instance with repository configuration
        branch_name: Name of the branch to checkout
        
    Returns:
        Path to the checked out worktree
    """
    worktree_path = get_worktree_path(config.repo_name, branch_name)
    
    # Create the directory structure
    worktree_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Get current directory (assumed to be the main repo)
    current_dir = Path.cwd()
    
    # Check if worktree already exists
    if worktree_path.exists():
        print(f"Worktree already exists at {worktree_path}")
        return worktree_path
    
    # Create the worktree
    print(f"Creating worktree at {worktree_path}")
    result = subprocess.run(
        ["git", "-C", str(current_dir), "worktree", "add", str(worktree_path), "-b", branch_name],
        capture_output=True,
        text=True,
        check=True
    )
    
    print(f"Worktree created successfully: {result.stdout}")
    return worktree_path


async def start_docker_environment(config: TreeConfig, worktree_path: Path) -> None:
    """Start Docker environment with the specified configuration.

    Args:
        config: TreeConfig instance with Docker and setup configuration
        worktree_path: Path to the worktree directory
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

    # Start dagger client with verbose logging
    async with dagger.Connection(dagger.Config(log_output=sys.stdout)) as client:
        # Pull the Docker image
        container = client.container().from_(config.docker_image)

        # Mount the worktree directory to /work_dir
        container = container.with_mounted_directory(
            "/work_dir", client.host().directory(str(worktree_path))
        )

        # Set work directory
        container = container.with_workdir("/work_dir")

        # Install git if not already present
        print("Installing git...")
        container = container.with_exec([
            "sh", "-c", 
            "which git || (apt-get update && apt-get install -y git) || (yum install -y git) || (apk add git)"
        ])

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
        await container.export_image(f"{image_name}")

        print(f"Container loaded as Docker image: {image_name}")
        
    # Run the container in interactive mode
    print(f"Starting interactive shell in container...")
    subprocess.run([
        "docker", "run", "-it", "--rm", 
        "-v", f"{worktree_path}:/work_dir",
        image_name, "/bin/sh"
    ])


async def start(config_path: str | Path | None = None) -> None:
    """Main entry point for starting the environment.

    Args:
        config_path: Optional path to configuration file
    """
    # Load configuration
    config = load_tree_config(config_path)
    
    if not config.repo_name:
        print("Error: repo_name is required in configuration")
        sys.exit(1)
    
    # Generate branch name
    branch_name = generate_env_name()
    
    # Checkout worktree
    worktree_path = checkout_worktree(config, branch_name)
    
    # Start Docker environment
    await start_docker_environment(config, worktree_path)
