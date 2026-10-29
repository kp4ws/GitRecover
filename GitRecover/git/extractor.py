from pathlib import Path
from GitRecover.utils import run_cmd

#TODO Create an enum for RepoState
def get_repo_state(repo_path: str | Path | None = None) -> str:
    git_dir = Path(repo_path) / ".git"

    #Check for ongoing operations
    if (git_dir / "rebase_merge").exists() or (git_dir / "rebase_apply").exists():
        return "InRebase"

    if (git_dir / "MERGE_HEAD").exists():
        return "InMerge/Conflict"

    if (git_dir / "CHERRY_PICK_HEAD").exists():
        return "InCherryPick"

    #Check for detached HEAD

    #Check for uncommitted changes

    #TODO Determine if any other checks needed

    return "Clean"


def get_repo_structure(repo_path: str | Path | None = None) -> str:
    return run_cmd("git", "repo structure", "--format=lines", cwd=repo_path)

def get_local_commits(repo_path: str | Path | None = None) -> str:
    return run_cmd("git", "cherry", "-v", cwd=repo_path)

def get_refs(repo_path: str | Path | None = None) -> str:
    return run_cmd("git", "for-each-ref", cwd=repo_path)

def get_staging_area(repo_path: str | Path | None = None) -> str:
    '''Gets index/staging area'''
    return run_cmd("git", "ls-files", "-s", cwd=repo_path)

def get_modified_files(repo_path: str | Path | None = None) -> str:
    return run_cmd("git", "ls-files", "-s", cwd=repo_path)

def get_current_head(repo_path: str | Path | None = None) -> str:
    return run_cmd("git", "rev-parse", "HEAD", cwd=repo_path)

def get_fsck_checks(repo_path: str | Path | None = None) -> str:
    return run_cmd("git", "fsck,", "--full", "--strict", "--unreachable", "--dangling", "--lost-found", "--verbose", cwd=repo_path)