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

    print("File from initial commit is changed and staged")
    write_to_file("app.py", "def init(): return True")
    run_scenario_cmd("git", "add", "app.py")


    print("Hard reset occurs, wiping staged work")
    run_scenario_cmd("git", "reset", "--hard", "HEAD")

    print_scenario_report("Lost Uncommitted Staged Files")

if __name__ == "__main__":
    setup_scenario()