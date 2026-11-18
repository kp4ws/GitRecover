"""
Author: Kent Pawson
uncommitted_staged_files_lost.py creates a scenario for losing staged uncommitted files.
"""

from tests.scenarios.scenario_base import (
    setup_repo,
    commit, 
    write_to_file,
    run_scenario_cmd, 
    print_scenario_report,
)

def setup_scenario():
    """Set up the lost-staged-files scenario."""
    setup_repo()

    print("Creating initial commit ...")
    commit(
        "app.py",
        "def init():",
        "Initial commit"
    )

    print("File from initial commit is changed and staged")
    write_to_file("app.py", "def init(): return True")
    run_scenario_cmd("git", "add", "app.py")


    print("Hard reset occurs, wiping staged work")
    run_scenario_cmd("git", "reset", "--hard", "HEAD")

    print_scenario_report("Lost Uncommitted Staged Files")
if __name__ == "__main__":
    setup_scenario()