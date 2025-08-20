#!/usr/bin/env python3
"""
Demo script showing wt-tools tmux functionality.

This script demonstrates how to use the wt-tools tmux management features.
"""

import subprocess
import sys
from pathlib import Path


def run_command(cmd: str) -> str:
    """Run a command and return its output."""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error running command '{cmd}': {e}")
        return ""


def main():
    """Run the tmux demo."""
    print("🐍 wt-tools Tmux Demo")
    print("=" * 50)
    
    # Check if wt command is available
    wt_version = run_command("wt --version")
    if wt_version:
        print(f"✅ wt-tools version: {wt_version.strip()}")
    else:
        print("❌ wt-tools not found. Please install it first.")
        sys.exit(1)
    
    print("\n📋 Available Commands:")
    print("-" * 30)
    
    # Show help
    help_output = run_command("wt --help")
    print(help_output)
    
    print("\n🔧 Session Management:")
    print("-" * 30)
    session_help = run_command("wt session --help")
    print(session_help)
    
    print("\n🪟 Window Management:")
    print("-" * 30)
    window_help = run_command("wt window --help")
    print(window_help)
    
    print("\n📝 Example Usage:")
    print("-" * 30)
    examples = [
        "wt session new myproject     # Create and attach to new session",
        "wt session attach myproject  # Attach to existing session", 
        "wt session list             # List all sessions",
        "wt session list-detailed    # List sessions with detailed info",
        "wt session kill myproject   # Kill a specific session",
        "wt session kill-all         # Kill all sessions",
        "wt session kill-all -e current # Kill all except 'current'",
        "wt window new               # Create new window",
        "wt window goto 3            # Go to window 3",
        "wt window close             # Close current window",
        "wt window list              # List windows in current session"
    ]
    
    for example in examples:
        print(f"  {example}")
    
    print("\n🎯 Try it out:")
    print("-" * 30)
    print("1. Start a new session: wt session new demo")
    print("2. Create a new window: wt window new")
    print("3. List windows: wt window list")
    print("4. Switch to window 1: wt window goto 1")
    print("5. List sessions: wt session list")
    print("6. List detailed sessions: wt session list-detailed")
    print("7. Kill a session: wt session kill demo")
    print("8. Kill all sessions: wt session kill-all")
    
    print("\n✨ Demo completed!")


if __name__ == "__main__":
    main()
