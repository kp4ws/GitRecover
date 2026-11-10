from tests.scenarios.scenario_base import (
    setup_repo,
    commit,
    run_scenario_cmd, 
    print_scenario_report,
)

def setup_scenario():
    setup_repo()

    print("Creating Initial commit...")
    commit(
        "app.py",
        'def hello_world()',
        "Initial commit"
    )

    print("Checking out to feature branch")
    run_scenario_cmd("git", "checkout", "-b", "feature/new_feature")
    commit(
        "app.py",
        "def process_data(input: str)",
        "Added process data function"
    )

    print("Switching back to main and making divergent change")
    run_scenario_cmd("git", "checkout", "main")
    commit(
        "app.py",
        "def process_data(input: int)",
        "Modified process_data function params"
    )

    print("Switch to feature and attemp to rebase onto main...")
    run_scenario_cmd("git", "checkout", "feature/new_feature")

    run_scenario_cmd("git", "rebase", "main")

    print("Developer accidentally runs --skip, deleting work ...")

    run_scenario_cmd("git", "rebase", "--skip")

    print_scenario_report("Bad Rebase")

if __name__ == "__main__":
    setup_scenario()