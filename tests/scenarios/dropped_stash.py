from tests.scenarios.scenario_base import (
    setup_repo,
    commit, 
    run_scenario_cmd, 
    print_scenario_report,
)

def setup_scenario():
    setup_repo()

    
    
    print_scenario_report("Dropped Stash")

if __name__ == "__main__":
    setup_scenario()