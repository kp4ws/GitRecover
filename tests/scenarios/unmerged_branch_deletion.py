from tests.scenarios.scenario_base import (
    setup_repo,
    commit,
    run_scenario_cmd, 
    print_scenario_report,
)

def setup_scenario():
    setup_repo()

    print("Creating initial commit on main...")
    commit(
        "app.py",
        "def init():",
        "Initial commit"
    )

    print("Checking out to feature branch ...")
    run_scenario_cmd("git", "checkout", "-b", "feature/new_feature")
    commit(
        "app.py",
        "def print()",
        "New feature"
    )

    print("Switching back to main and accidentally deleting unmerged feature branch ...")
    run_scenario_cmd("git", "checkout", "main")
    
    run_scenario_cmd("git", "branch", "-D", "feature/new_feature")

    print_scenario_report("Unmerged Branch Deletion")

if __name__ == "__main__":
    setup_scenario()