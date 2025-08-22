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


def is_dagger_type_error(error: Exception) -> bool:
    """Check if the error is the specific Dagger type checking issue.
    
    Args:
        error: The exception to check
        
    Returns:
        True if it's the Dagger type checking error, False otherwise
    """
    error_type = type(error).__name__
    error_msg = str(error)
    
    # Check for the specific Dagger type checking error patterns
    dagger_error_patterns = [
        "BeartypeCallHintReturnViolation",
        "dagger.Void",
        "expected to be of type",
        "return.*None.*expected"
    ]
    
    return any(pattern in error_type or pattern in error_msg for pattern in dagger_error_patterns)


def generate_env_name() -> str:
    """Generate a 3-word memorable name.

    Returns:
        A memorable 3-word name like 'cobra-felix-amateur'
    """
    name = coolname.generate_slug(3)
    return str(name)


def get_work_path(repo_name: str, env_name: str) -> Path:
    """Get the path for the worktree.
    
    Args:
        repo_name: Name of the repository
        env_name: Name of the environment / branch
        
    Returns:
        Path to the worktree directory
    """
    config_dir = Path.home() / ".config" / "tree" / "worktrees"
    worktree_path = config_dir / repo_name / env_name
    return worktree_path

def setup_work_repo(config: TreeConfig, env_name: str) -> Path:
    """Clone the repository to the specified directory.
    
    Args:
        config: TreeConfig instance with repository configuration
        env_name: Name of the environment / branch
        
    Returns:
        Path to the cloned repository
        
    Raises:
        RuntimeError: If git clone or checkout fails
    """
    work_path = get_work_path(config.repo_name, env_name)
    
    # Create the directory structure
    work_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Check if repository already exists
    if work_path.exists():
        print(f"Repository already exists at {work_path}")
        return work_path
    
    print(f"Cloning repository from {config.repo_path} to {work_path}")
    
    # Clone the repository
    try:
        result = subprocess.run(
            ["git", "clone", "--single-branch", "--branch", config.default_branch, config.repo_path, str(work_path)],
            capture_output=True,
            text=True,
            check=True
        )
        print(f"Repository cloned successfully: {result.stdout}")
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Failed to clone repository from {config.repo_path}: {e.stderr}") from e
    
    # Create and checkout the new branch
    try:
        print(f"Creating new branch: {env_name}")
        result = subprocess.run(
            ["git", "-C", work_path, "checkout", "-b", env_name],
            capture_output=True,
            text=True,
            check=True
        )
        print(f"Branch created successfully: {result.stdout}")
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Failed to create branch {env_name}: {e.stderr}") from e
    
    return work_path


async def start_docker_environment(config: TreeConfig, env_name: str) -> str:
    """Start Docker environment with the specified configuration.

    Args:
        config: TreeConfig instance with Docker and setup configuration
        env_name: Name of the environment
        
    Returns:
        Name of the created Docker image
        
    Raises:
        RuntimeError: If Docker operations fail
    """
    try:
        import dagger
    except ImportError:
        raise RuntimeError(
            "dagger package not found. Please install it with: pip install dagger-io"
        )

    work_path = get_work_path(config.repo_name, env_name)
    
    # Verify work path exists
    if not work_path.exists():
        raise RuntimeError(f"Work path does not exist: {work_path}")

    print(f"Starting Docker environment for {config.repo_name} at {work_path}")
    
    # Start dagger client with verbose logging
    async with dagger.Connection(dagger.Config(log_output=sys.stdout)) as client:
        try:
            # Pull the Docker image
            print(f"Pulling Docker image: {config.docker_image}")
            container = client.container().from_(config.docker_image)

            # Mount the worktree directory to /work_dir
            container = container.with_mounted_directory(
                "/work_dir", client.host().directory(str(work_path))
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
            for i, cmd in enumerate(config.setup_cmds, 1):
                if cmd.startswith("#"):
                    continue

                print(f"Running setup command {i}/{len(config.setup_cmds)}: {cmd}")
                # Use shell to execute commands that may contain operators like &&
                container = container.with_exec(["sh", "-c", cmd])

            # Build the container as a local Docker image
            image_name = f"mux-env-{config.repo_name}-{env_name}"
            print(f"Building container as Docker image: {image_name}")
            
            try:
                await container.export_image(f"{image_name}")
            except Exception as e:
                if is_dagger_type_error(e):
                    print(f"Warning: Dagger type checking issue detected (this is expected): {type(e).__name__}")
                    print(f"Error details: {str(e)}")
                else:
                    raise

            print(f"Container loaded as Docker image: {image_name}")
            return image_name
            
        except Exception as e:
            raise RuntimeError(f"Failed to build Docker environment: {str(e)}") from e
        



async def start(config_path: str | Path | None = None) -> None:
    """Main entry point for starting the environment.

    Args:
        config_path: Optional path to configuration file
        
    Raises:
        RuntimeError: If any step of the environment setup fails
    """
    try:
        # Load configuration
        print("Loading configuration...")
        config = load_tree_config(config_path)
        
        if not config.repo_path:
            raise RuntimeError("repo_path is required in configuration")
        
        if not config.repo_name:
            raise RuntimeError(f"Could not extract repo_name from repo_path: {config.repo_path}")

        # Generate environment name
        env_name = generate_env_name()
        print(f"Generated environment name: {env_name}")
        
        # Setup work repository
        work_path = setup_work_repo(config, env_name)
        
        # Start Docker environment
        image_name = await start_docker_environment(config, env_name)

        # Start interactive shell
        print(f"Starting interactive shell in container...")
        subprocess.run([
            "docker", "run", "-it", "--rm", 
            "-v", f"{work_path}:/work_dir",
            image_name, "/bin/sh"
        ])
        
    except Exception as e:
        raise RuntimeError(f"Failed to start environment: {str(e)}") from e
