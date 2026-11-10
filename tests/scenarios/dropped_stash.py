from tests.scenarios.scenario_base import (
    setup_repo,
    commit, 
    write_to_file,
    run_scenario_cmd, 
    print_scenario_report,
)

def setup_scenario():
    setup_repo()

    print("Creating initial commit ...")
    commit(
        "app.py",
        "def init():",
        "Initial commit"
    )

    write_to_file("app.py", "def do_stuff()")

    print("Stashing changes...")
    run_scenario_cmd("git", "stash")

    print("Accidentally dropping stash")
    run_scenario_cmd("git", "stash", "drop")

    print_scenario_report("Dropped Stash")

if __name__ == "__main__":
    setup_scenario()