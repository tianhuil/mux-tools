"""
Configuration management for the tree command.

This module provides Pydantic models for parsing YAML configuration files
with full type safety and mypy support.
"""

from pathlib import Path
from typing import Any

import yaml
from pydantic import BaseModel, Field


class TreeConfig(BaseModel):
    """Configuration for the tree command."""
    
    remote_repo: str = Field(
        default="",
        description="Remote repository URL"
    )

    docker_image: str = Field(
        default="alpine:latest",
        description="Docker image to use"
    )

    repo_path: str = Field(
        default="",
        description="Repository path"
    )
    
    default_branch: str = Field(
        default="main",
        description="Default branch name"
    )
    
    setup_cmds: list[str] = Field(
        default_factory=list,
        description="Commands to run during setup"
    )
    
    validation_cmds: list[str] = Field(
        default_factory=list,
        description="Commands to run for validation"
    )
    
    @property
    def repo_name(self) -> str:
        """Extract the repository name from the repo_path.
        
        Returns:
            The last part of the repo_path as the repository name
        """
        if not self.repo_path:
            return ""
        
        path = Path(self.repo_path)
        
        return path.name
        

class ConfigLoader:
    """Loader for configuration files."""
    
    def __init__(self, config_path: str | Path | None = None) -> None:
        """Initialize the config loader.
        
        Args:
            config_path: Path to the configuration file. If None, looks for
                        config files in common locations.
        """
        self.config_path = Path(config_path) if config_path else None
    
    def find_config_file(self) -> Path | None:
        """Find configuration file in common locations.
        
        Returns:
            Path to the configuration file if found, None otherwise.
        """
        if self.config_path and self.config_path.exists():
            return self.config_path
        
        # Common config file locations
        config_locations = [
            Path("tree-config.yaml"),
            Path("tree-config.yml"),
        ]
        
        for location in config_locations:
            if location.exists():
                return location
        
        return None
    
    def load_config(self) -> TreeConfig:
        """Load configuration from file or return defaults.
        
        Returns:
            TreeConfig instance with loaded or default values.
        """
        config_file = self.find_config_file()
        
        if config_file is None:
            return TreeConfig()
        
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                config_data = yaml.safe_load(f)
            
            if config_data is None:
                return TreeConfig()

            config_data["repo_path"] = config_data.get("repo_path") or str(Path.cwd())

            return TreeConfig(**config_data)
            
        except (yaml.YAMLError, OSError) as e:
            raise ValueError(f"Failed to load configuration from {config_file}: {e}")
    
    def save_config(self, config: TreeConfig, path: str | Path | None = None) -> None:
        """Save configuration to a file.
        
        Args:
            config: TreeConfig instance to save
            path: Path to save the configuration to. If None, uses the
                  default config path.
        """
        save_path = Path(path) if path else self.config_path
        
        if save_path is None:
            raise ValueError("No path specified for saving configuration")
        
        # Ensure the directory exists
        save_path.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            with open(save_path, 'w', encoding='utf-8') as f:
                yaml.dump(config.model_dump(), f, default_flow_style=False, indent=2)
        except OSError as e:
            raise ValueError(f"Failed to save configuration to {save_path}: {e}")


def load_tree_config(config_path: str | Path | None = None) -> TreeConfig:
    """Convenience function to load tree configuration.
    
    Args:
        config_path: Optional path to configuration file
        
    Returns:
        TreeConfig instance
    """
    loader = ConfigLoader(config_path)
    return loader.load_config()


def create_sample_config(path: str | Path) -> None:
    """Create a sample configuration file.
    
    Args:
        path: Path where to create the sample configuration
    """
    sample_config = TreeConfig(
        remote_repo="https://github.com/example/repo.git",
        docker_image="alpine:latest",
        default_branch="main",
        setup_cmds=["npm install", "pip install -r requirements.txt"],
        validation_cmds=["npm test", "python -m pytest"]
    )
    
    loader = ConfigLoader()
    loader.save_config(sample_config, path)
