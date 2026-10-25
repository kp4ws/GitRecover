from pathlib import Path
from GitRecover.utils import run_cmd

def get_repo_structure(repo_path: str | Path | None = None) -> str:
    return run_cmd("git", "repo structure", "--format=lines", repo_path)

def get_local_commits(repo_path: str | Path | None = None) -> str:
    return run_cmd("git", "cherry", "-v", repo_path)

def get_refs(repo_path: str | Path | None = None) -> str:
    return run_cmd("git", "for-each-ref", repo_path)

def get_staging_area(repo_path: str | Path | None = None) -> str:
    '''Gets index/staging area'''
    return run_cmd("git", "ls-files", "-s", repo_path)

def get_modified_files(repo_path: str | Path | None = None) -> str:
    return run_cmd("git", "ls-files", "-s", repo_path)

def get_current_head(repo_path: str | Path | None = None) -> str:
    return run_cmd("git", "rev-parse", "HEAD", repo_path)

def get_fsck_checks(repo_path: str | Path | None = None) -> str:
    return run_cmd("git", "fsck,", "--full", "--strict", "--unreachable", "--dangling", "--lost-found", "--verbose", repo_path)