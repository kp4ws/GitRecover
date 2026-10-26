from tests.scenarios.scenario_base import (
    setup_repo,
    commit, 
    run_scenario_cmd, 
    print_scenario_report,
)

def setup_scenario():
    setup_repo()

    print("Creating initial commit ...")
    
    commit (
        "app.py",
        'print("Hello World")\n',
        "Initial commit"
    )

    print("Simulating file changes...")
    lost_commit = commit(
        "app.py",
        'print("Hello World")\nprint("This is my new feature!")\n',
        "Added new feature"
    )

    print("Accidental hard reset...")
    run_scenario_cmd("git", "reset", "--hard", "HEAD~1")

    print(f"Lost commit: {lost_commit}")
    print_scenario_report("Hard Reset")

if __name__ == "__main__":
    setup_scenario()