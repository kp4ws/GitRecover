from tests.scenarios.scenario_base import (
    setup_repo,
    write_to_file,
    commit,
    merge,
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

    print("New commit on feature branch...")
    run_scenario_cmd("git", "checkout", "-b", "feature/new_feature")
    commit(
        "app.py",
        'def process_data()',
        "Modified function name"
    )

    print("Switching back to main to create a conflict...")
    run_scenario_cmd("git", "checkout", "main")
    commit(
        "app.py",
        'def print_out()',
        "Changing function name to print_out"
    )

    print("Merging feature into main to create a merge conflict...")
    merge("feature/new_feature") #TODO: This command fails.

    print("Developer attempts to resolve accepting wrong changes ...")

    write_to_file("app.py", "def print_out()")

    run_scenario_cmd("git", "add", "app.py")
    run_scenario_cmd("git", "commit", "--no-edit")

    print_scenario_report("Bad Merge")

if __name__ == "__main__":
    setup_scenario()