import os

import libtmux


def generate_session_name(remote_repo: str) -> str:
    """Generate a session name from remote repository URL.

    Args:
        remote_repo: Remote repository URL

    Returns:
        Session name derived from the repository
    """
    # Extract repo name from URL
    if remote_repo.endswith(".git"):
        remote_repo = remote_repo[:-4]

    # Get the last part of the URL (repo name)
    repo_name = remote_repo.split("/")[-1]

    return repo_name


def ensure_tmux(remote_repo: str) -> None:
    """Ensure we're in a tmux session for the given remote repository.

    Args:
        remote_repo: Remote repository URL to use for session naming
    """
    # Check if we're already in tmux
    if os.environ.get("TMUX") is None:
        # Not in tmux, try to attach to existing session or create new one
        server = libtmux.Server()

        # Generate session name from remote repo
        session_name = generate_session_name(remote_repo)

        # Try to find existing session
        session = server.find_where({"session_name": session_name})
        if session:
            print(f"Attaching to existing tmux session: {session_name}")
            session.attach_session()
            return

        # Create new session
        print(f"Creating new tmux session: {session_name}")
        session = server.new_session(session_name=session_name, attach=False)
        session.attach_session()
    else:
        print("Already in tmux session")
