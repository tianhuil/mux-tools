#!/usr/bin/env python3
"""
Demo script showing mux-tools tmux functionality.

This script demonstrates how to use the mux-tools tmux management features.
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
    print("🐍 mux-tools Tmux Demo")
    print("=" * 50)
    
    # Check if mux command is available
    mux_version = run_command("mux --version")
    if mux_version:
        print(f"✅ mux-tools version: {mux_version.strip()}")
    else:
        print("❌ mux-tools not found. Please install it first.")
        sys.exit(1)
    
    print("\n📋 Available Commands:")
    print("-" * 30)
    
    # Show help
    help_output = run_command("mux --help")
    print(help_output)
    
    print("\n🔧 Session Management:")
    print("-" * 30)
    session_help = run_command("mux session --help")
    print(session_help)
    
    print("\n🪟 Window Management:")
    print("-" * 30)
    window_help = run_command("mux window --help")
    print(window_help)
    
    print("\n📝 Example Usage:")
    print("-" * 30)
    examples = [
        "mux session new myproject     # Create and attach to new session",
        "mux session attach myproject  # Attach to existing session", 
        "mux session list             # List all sessions",
        "mux session list-detailed    # List sessions with detailed info",
        "mux session kill myproject   # Kill a specific session",
        "mux session kill-all         # Kill all sessions",
        "mux session kill-all -e current # Kill all except 'current'",
        "mux window new               # Create new window",
        "mux window goto 3            # Go to window 3",
        "mux window close             # Close current window",
        "mux window list              # List windows in current session"
    ]
    
    for example in examples:
        print(f"  {example}")
    
    print("\n🎯 Try it out:")
    print("-" * 30)
    print("1. Start a new session: mux session new demo")
    print("2. Create a new window: mux window new")
    print("3. List windows: mux window list")
    print("4. Switch to window 1: mux window goto 1")
    print("5. List sessions: mux session list")
    print("6. List detailed sessions: mux session list-detailed")
    print("7. Kill a session: mux session kill demo")
    print("8. Kill all sessions: mux session kill-all")
    
    print("\n✨ Demo completed!")


if __name__ == "__main__":
    main()
