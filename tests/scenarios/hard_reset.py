from pathlib import Path
from git import Repo
import shutil
import os
import stat

#Helper function to unlock .git readonly files
def unlock_file(action, path, exc_info):
    os.chmod(path, stat.S_IWRITE)
    action(path)

def setup_scenario():
    base_dir = Path(__file__).parent.resolve()
    repo_dir = base_dir / "dummy_repo"

    #Clean up previous runs
    if repo_dir.exists():
        shutil.rmtree(repo_dir, onexc=unlock_file)

    #Create directory for this scenario
    repo_dir.mkdir()

    print(f"Initializing Git repo in {repo_dir.name}...")
    git_repo = Repo.init(repo_dir)

    print("Creating initial commit ...")
    file_path = repo_dir / "app.py"
    file_path.write_text('print("Hello World")\n')
    git_repo.index.add([file_path.name])
    git_repo.index.commit("Initial commit")

    print("Simulating file changes...")
    file_path.write_text('print("Hello World")\nprint("This is my new feature!")\n')
    git_repo.index.add([file_path.name])
    feature_commit = git_repo.index.commit("Added new feature")

    print("Accidental hard reset...")
    git_repo.head.reset("HEAD~1", index=True, working_tree=True)

    print("\nScenario ready")
    print(f"Lost commit: {feature_commit.hexsha}")
    print(f"Current HEAD: {git_repo.head.commit.hexsha}")

if __name__ == "__main__":
    setup_scenario()