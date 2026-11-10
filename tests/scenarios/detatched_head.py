from tests.scenarios.scenario_base import (
    setup_repo,
    run_scenario_cmd,
    commit,
    print_scenario_report
)

def setup_scenario():
    setup_repo()

    print("Creating initial commits on main...")
    commit(
        "app.py",
        'def initialize():',
        "Initial commit"
    )
    commit(
        "app.py",
        "def initialize(): return False",
        "Added return"
    )

    print("Looking at old code, checking out to first commit")
    run_scenario_cmd("git", "checkout", "HEAD~1")

    print("Changes made in detached head state")
    commit (
        "app.py",
        'def initialize(): return True',
        "Changed return value"
    )

    print("Switching back to main, losing the detached commit")
    run_scenario_cmd("git", "checkout", "main")
    
    print_scenario_report("Detached HEAD")

if __name__ == "__main__":
    setup_scenario()