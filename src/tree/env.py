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
from rich.console import Console

from .config import TreeConfig, load_tree_config

# Initialize console for rich output
console = Console()

class EnvironmentConfig:
    """Environment class for managing worktrees and Docker environments."""

    def __init__(self, config: TreeConfig, env_name: str | None = None):
        self.config = config
        self.env_name = env_name or self.generate_env_name()
    
    @staticmethod
    def generate_env_name() -> str:
        """Generate a 3-word memorable name.

        Returns:
            A memorable 3-word name like 'cobra-felix-amateur'
        """
        name = coolname.generate_slug(3)
        return str(name)

    @property
    def repo_path(self) -> Path:
        """Get the repository name.
        
        Returns:
            The repository name
        """
        return Path.home() / ".config" / "tree" / "work" / self.config.repo_name

    @property
    def work_path(self) -> Path:
        """Get the path for the worktree.
        
        Args:
            env_name: Name of the environment / branch
            
        Returns:
            Path to the worktree directory
        """
        return self.repo_path / self.env_name

    @property
    def image_name(self) -> str:
        """Get the name of the Docker image.
        
        Returns:
            The name of the Docker image
        """
        return f"tree-env_{self.config.repo_name}_{self.env_name}"

    def list_work_trees(self) -> list['EnvironmentConfig']:
        """List all worktrees for the current user.
        
        Returns:
            List of Environment objects representing worktree directories
        """
        work_paths = list(self.repo_path.glob("*"))
        return [EnvironmentConfig(self.config, work_path.name)  for work_path in work_paths]


def is_superfluous_dagger_error(error: Exception) -> bool:
    """
    Check if the error is the specific Dagger type checking issue.
    It can be safely ignored.
    
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


def setup_work_repo(env: EnvironmentConfig) -> Path:
    """Clone the repository to the specified directory.
    
    Args:
        config: TreeConfig instance with repository configuration
        env_name: Name of the environment / branch
        
    Returns:
        Path to the cloned repository
        
    Raises:
        RuntimeError: If git clone or checkout fails
    """
    work_path = env.work_path
    repo_path = env.repo_path
    env_name = env.env_name
    
    # Create the directory structure
    work_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Check if repository already exists
    if work_path.exists():
        console.print(f"Repository already exists at {work_path}")
        return work_path
    
    console.print(f"Cloning repository from {repo_path} to {work_path}")
    
    # Clone the repository
    try:
        result = subprocess.run(
            ["git", "clone", "--single-branch", "--branch", env.config.default_branch, repo_path, str(work_path)],
            capture_output=True,
            text=True,
            check=True
        )
        console.print(f"Repository cloned successfully: {result.stdout}")
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Failed to clone repository from {repo_path}: {e.stderr}") from e
    
    # Create and checkout the new branch
    try:
        console.print(f"Creating new branch: {env_name}")
        result = subprocess.run(
            ["git", "-C", work_path, "checkout", "-b", env_name],
            capture_output=True,
            text=True,
            check=True
        )
        console.print(f"Branch created successfully: {result.stdout}")
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Failed to create branch {env_name}: {e.stderr}") from e
    
    return work_path


async def start_docker_environment(env: EnvironmentConfig) -> str:
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

    work_path = env.work_path
    repo_name = env.config.repo_name
    config = env.config
    
    # Verify work path exists
    if not work_path.exists():
        raise RuntimeError(f"Work path does not exist: {work_path}")

    console.print(f"Starting Docker environment for {repo_name} at {work_path}")
    
    # Start dagger client with verbose logging
    async with dagger.Connection(dagger.Config(log_output=sys.stdout)) as client:
        try:
            # Pull the Docker image
            console.print(f"Pulling Docker image: {config.docker_image}")
            container = client.container().from_(config.docker_image)

            # Mount the worktree directory to /work_dir
            container = container.with_mounted_directory(
                "/work_dir", client.host().directory(str(work_path))
            )

            # Set work directory
            container = container.with_workdir("/work_dir")

            # Install git if not already present
            console.print("Installing git...")
            container = container.with_exec([
                "sh", "-c", 
                "which git || (apt-get update && apt-get install -y git) || (yum install -y git) || (apk add git)"
            ])

            # Run setup commands
            for i, cmd in enumerate(config.setup_cmds, 1):
                if cmd.startswith("#"):
                    continue

                console.print(f"Running setup command {i}/{len(config.setup_cmds)}: {cmd}")
                # Use shell to execute commands that may contain operators like &&
                container = container.with_exec(["sh", "-c", cmd])

            # Build the container as a local Docker image
            image_name = env.image_name
            console.print(f"Building container as Docker image: {image_name}")
            
            try:
                await container.export_image(f"{image_name}")
            except Exception as e:
                if is_superfluous_dagger_error(e):
                    console.print(f"[yellow]Warning: Dagger type checking issue detected (this is expected): {type(e).__name__}[/yellow]")
                    console.print(f"[dim]Error details: {str(e)}[/dim]")
                else:
                    raise

            console.print(f"Container loaded as Docker image: {image_name}")
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
        env = EnvironmentConfig(load_tree_config(config_path))
        
        work_path = setup_work_repo(env)
        image_name = await start_docker_environment(env)

        # Start interactive shell
        console.print(f"Starting interactive shell in container...")
        subprocess.run([
            "docker", "run", "-it", "--rm", 
            "-v", f"{work_path}:/work_dir",
            image_name, "/bin/sh"
        ])
        
    except Exception as e:
        raise RuntimeError(f"Failed to start environment: {str(e)}") from e

async def list_work_trees(config_path: str | Path | None = None) -> list[EnvironmentConfig]:
    """List all worktrees for the current user.
    
    Returns:
        List of Environment objects representing worktree directories
    """
    try:
        env = EnvironmentConfig(load_tree_config(config_path))
        return env.list_work_trees()

    except Exception as e:
        raise RuntimeError(f"Failed to list worktrees: {str(e)}") from e
