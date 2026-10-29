from tests.scenarios.scenario_base import (
    setup_repo,
    commit, 
    run_scenario_cmd, 
    print_scenario_report,
)

def setup_scenario():
    setup_repo()

    print("Creating initial commit...")
    commit(
        "config.txt",
        "test_value=True\n",
        "Initial commit: Testing stuff"
    )

    print("switching branches")
    run_scenario_cmd("git", "checkout", "-b", "feature/new_feature")

    print("Making changes on the new branch")
    commit(
        "config.txt",
        "test_value=False\n",
        "Changed test value"
    )

    print("Returning to main branch...")
    run_scenario_cmd("git", "checkout", "main")

    print("Making conflicting changes on main branch...")
    commit(
        "config.txt",
        "test_value=None\n",
        "Switched test_value to none"
    )

    print("Triggering merge conflict...")
    try:
        run_scenario_cmd("git", "merge", "feature/new_feature")
    except Exception:
        pass

    print_scenario_report("Merge Conflict")

if __name__ == "__main__":
    setup_scenario()