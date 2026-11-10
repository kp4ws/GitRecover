from tests.scenarios.scenario_base import (
    setup_repo,
    commit,
    print_scenario_report
)

def setup_scenario():
    setup_repo()

    print("Creating initial commit on main...")
    base_commit = commit(
        "app.py",
        'print("testing things out")',
        "Initial commit"
    )

    print("Accidentally committing new feature to main...")
    commit(
        "app.py",
        'print("testing things out")\n print("new feature")',
        "New Feature"
    )

    print_scenario_report("Direct Commit to Main")

if __name__ == "__main__":
    setup_scenario()