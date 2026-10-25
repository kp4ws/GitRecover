from pathlib import Path
from GitRecover.utils import run_cmd

def get_repo_structure(git_repo: str | Path | None = None) -> str:
    return run_cmd("git repo structure --format=lines", git_repo)

def get_local_commits(git_repo: str | Path | None = None) -> str:
    return run_cmd("git cherry -v", git_repo)

def get_refs(git_repo: str | Path | None = None) -> str:
    return run_cmd("git for-each-ref", git_repo)

def get_staging_area(git_repo: str | Path | None = None) -> str:
    '''Gets index/staging area'''
    return run_cmd("git ls-files -s", git_repo)

def get_modified_files(git_repo: str | Path | None = None) -> str:
    return run_cmd("git ls-files -s", git_repo)

def get_current_head(git_repo: str | Path | None = None) -> str:
    return run_cmd("git rev-parse HEAD", git_repo)

def get_fsck_checks(git_repo: str | Path | None = None) -> str:
    return run_cmd("git fsck --full --strict --unreachable --dangling --lost-found --verbose", git_repo)