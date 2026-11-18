"""
Author: Kent Pawson
scenario_base.py provides shared setup and command helpers for test scenarios.
"""

from GitRecover.utils import run_cmd
from pathlib import Path
import shutil
import os
import stat

SCENARIO_DIR = Path(__file__).resolve().parent
REPO_DIR = SCENARIO_DIR / "dummy_repo"

def run_scenario_cmd(*args: str) -> str:
    """Run a command inside the scenario repository.

    Parameters:
        *args: Command and arguments.

    Returns:
        The stripped command output.
    """
    return run_cmd(*args, cwd=str(REPO_DIR))

#Helper function to unlock .git readonly files
def unlock_file(action, path, exc_info):
    """Remove read-only restrictions before Windows deletes a file."""
    os.chmod(path, stat.S_IWRITE)
    action(path)

def setup_repo():
    """Reset and initialize the scenario repository."""
    if REPO_DIR.exists():
        shutil.rmtree(REPO_DIR, onexc=unlock_file)
    REPO_DIR.mkdir(parents=True)

    print(f"Initializing Git repo in {REPO_DIR.name}...")
    
    run_scenario_cmd("git", "init", "-b", "main")
    run_scenario_cmd("git", "config", "user.name", "GitRecover Test")
    run_scenario_cmd("git", "config", "user.email", "test@example.gitrecover")

def write_to_file(filename, content):
    """Create or update a file in the scenario repository."""
    path = REPO_DIR / filename
    path.parent.mkdir(parents=True, exist_ok=True) #Creates directory/file if not currently existing
    path.write_text(content, encoding="utf-8")

def commit(filename, content, message):
    """Write a file, stage it, and create a commit.

    Parameters:
        filename: File name relative to the scenario repository.
        content: New file content.
        message: Commit message.

    Returns:
        The new commit hash.
    """
    write_to_file(filename, content)
    run_scenario_cmd("git", "add", f"{filename}")
    run_scenario_cmd("git", "commit", "-m", f"{message}")
    return run_scenario_cmd("git", "rev-parse", "HEAD") #return head pointer

def merge(branch_name):
    """Merge a branch into the current branch.

    Parameters:
        branch_name: Branch to merge.
    """
    run_scenario_cmd("git", "merge", branch_name)

def print_scenario_report(title):
    """Print the scenario title and current Git status.

    Parameters:
        title: Scenario name.
    """
    print(f"Scenario Ready: {title}\nRepository: {REPO_DIR}")
    print("Git Status")
    print(run_scenario_cmd("git", "status"))