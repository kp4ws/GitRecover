import os
import subprocess
from pathlib import Path
from GitRecover.utils import run_cmd
from GitRecover.core.schemas import RemoteSyncInfo, RemoteSyncStatus, RepoStatus

def get_repo_status(repo_path: str) -> RepoStatus:
    git_dir = Path(repo_path) / ".git"

    #Check for ongoing operations
    if (git_dir / "rebase-merge").exists() or (git_dir / "rebase-apply").exists():
        return RepoStatus.REBASE

    if (git_dir / "MERGE_HEAD").exists():
        return RepoStatus.MERGE

    if (git_dir / "CHERRY_PICK_HEAD").exists():
        return RepoStatus.CHERRY_PICK

    branch = get_current_branch(repo_path)
    if not branch:
        return RepoStatus.DETACHED

    is_dirty = run_cmd("git", "status", "--porcelain", cwd=repo_path).strip()
    if is_dirty:
        return RepoStatus.DIRTY

    #If all the above checks passed then repo state is considered clean
    return RepoStatus.CLEAN

def get_current_head(repo_path: str) -> str:
    result = run_cmd("git", "rev-parse", "HEAD", cwd=repo_path)

    if result:
        return result.strip()

    #By default if cannot determine HEAD, return "Unknown"
    return "Unknown"

def get_current_branch(repo_path: str) -> str:
    result = run_cmd("git", "symbolic-ref", "--short", "-q", "HEAD", cwd=repo_path)
    if result:
        return result.strip()

    #default return empty string for current branch
    return ""

def _run_remote_cmd(repo_path: str, *args: str) -> subprocess.CompletedProcess:
    environment = os.environ.copy()
    #prevents Git from waiting on terminal input
    environment["GIT_TERMINAL_PROMPT"] = "0"

    result: subprocess.CompletedProcess = run_cmd(
        *args, 
        cwd=repo_path,
        capture_output=True,
        text=True,
        check=False,
        timeout=30,
        env=environment,
        return_str=False
    )

    #Empty string signifies error, so just manually return -999 as error code
    if result == "":
        return -999
    
    return result

def get_remote_sync_info(repo_path: str) -> RemoteSyncInfo:
    #If in detached head state, then return detached sync status
    if not get_current_branch(repo_path):
        return RemoteSyncInfo(
            status=RemoteSyncStatus.DETACHED,
        )

    remote_result = _run_remote_cmd(repo_path, "git", "remote")
    if remote_result.returncode != 0:
        return RemoteSyncInfo(
            status=RemoteSyncStatus.ERROR,
            error_message="Error getting remote, please try again.",
        )

    remotes = remote_result.stdout.strip().splitlines()
    #If no remote setup, then return no remote sync status    
    if not remotes:
        return RemoteSyncInfo(
            status=RemoteSyncStatus.NO_REMOTE,
        )

    #grab upstream branch
    upstream_result = _run_remote_cmd(repo_path, "git", "rev-parse", "--symbolic-full-name", "@{upstream}")
    if upstream_result.returncode != 0:
        return RemoteSyncInfo(
            status=RemoteSyncStatus.NO_UPSTREAM,
        )

    upstream_ref = upstream_result.stdout.strip()
    sorted_remotes = sorted(remotes, key=len, reverse=True)

    remote_name = ""
    upstream = ""
    for remote in sorted_remotes:
        remote_ref_prefix = f"refs/remotes/{remote}/"
        match_flag = upstream_ref.startswith(remote_ref_prefix)

        #Checking if upstream ref matches a remote
        if match_flag:
            remote_name = remote
            upstream = upstream_ref[len("refs/remotes/"):]
            break

    if not remote_name:
        return RemoteSyncInfo(
            status=RemoteSyncStatus.NO_UPSTREAM,
        )

    fetch_result = _run_remote_cmd(repo_path, "git", "fetch", "--no-tags", remote_name)

    if fetch_result.returncode != 0:
        return RemoteSyncInfo(
            status=RemoteSyncStatus.ERROR,
            upstream=upstream,
            error_message="Error fetching, please try again.",
        )

    upstream_counts_result = _run_remote_cmd(repo_path, "git", "rev-list", "--left-right", "--count", f"{upstream_ref}...HEAD")
    if upstream_counts_result.returncode != 0:
        return RemoteSyncInfo(
            status=RemoteSyncStatus.ERROR,
            upstream=upstream,
            error_message="Error getting upstream counts, please try again.",
        )

    count_values = upstream_counts_result.stdout.strip().split()
    count_flag = False

    if len(count_values) != 2:
        count_flag = True
    for value in count_values:
        if not value.isdigit():
            count_flag = True
            break 
    if count_flag:
        return RemoteSyncInfo(
            status=RemoteSyncStatus.ERROR,
            upstream=upstream,
            error_message="Unexpected ahead/behind count, please try again.",
        )

    #Get counts for behind and ahead
    behind = int(count_values[0])
    ahead = int(count_values[1])

    #Determine if branch is up to date or not
    if ahead == 0 and behind == 0:
        status = RemoteSyncStatus.UP_TO_DATE
    elif ahead > 0 and behind == 0:
        status = RemoteSyncStatus.AHEAD
    elif ahead == 0 and behind > 0:
        status = RemoteSyncStatus.BEHIND
    else:
        #if ahead > 0 and behind > 0, implies unique commits on both sides => diverged
        status = RemoteSyncStatus.DIVERGED

    return RemoteSyncInfo(
        status=status,
        upstream=upstream,
        ahead=ahead,
        behind=behind,
    )

def get_recent_commits(repo_path: str, max_count: int = 30) -> list[dict]:
    '''commits including those not part of commit tree (orphaned commits found via reflog)'''

    dangling_set = get_dangling_commit_set(repo_path)

    reflog_fields = [
        "%H", #commit hash
        "%P", #parent hashes
        "%an", #author
        "%ad", #date
        "%s", #message
        "%gs", #git action
    ]

    #We use null delimiter to join the fields (so that it doesn't appear in git command)
    reflog_format = "%x00".join(reflog_fields)
    result = run_cmd("git", "log", "-g", f"-n{max_count}", f"--format={reflog_format}", "--date=short", cwd=repo_path).strip()

    commits = []
    if result:
        for record in result.splitlines():
            record_fields = record.split("\x00", 5) #split on null delimiter
            if len(record_fields) == 6:
                commit_hash = record_fields[0]
                parent_hashes = record_fields[1]
                author = record_fields[2]
                date = record_fields[3]
                message = record_fields[4]
                git_action = record_fields[5]

                parents = []
                if parent_hashes:
                    parents = parent_hashes.split()

                commits.append({
                    "hash": commit_hash,
                    "parents": parents,
                    "author": author,
                    "date": date,
                    "message": message,
                    "git_action": git_action,
                    "is_dangling": commit_hash in dangling_set
                })

    return commits

def get_dangling_commit_set(repo_path: str) -> set[str]:
    #Check for dangling commits
    result = run_cmd("git", "fsck", "--lost-found", cwd=repo_path).strip()
    if not result:
        return set()
    
    dangling_commits = set()
    for line in result.splitlines():
        if "dangling commit" in line:
            line_parts = line.split()
            if len(line_parts) >= 3:
                dangling_commits.add(line_parts[2])

    return dangling_commits

def get_unpushed_commits(repo_path: str) -> str:
    '''Returns commits that haven't been pushed upstream yet'''
    return run_cmd("git", "cherry", "-v", cwd=repo_path)

def get_refs(repo_path: str) -> str:
    result = run_cmd("git", "for-each-ref", cwd=repo_path)

    #Clean up result and strip away any formatting
    refs = {}
    for line in result.strip().splitlines():
        hash_val, ref_name = line.split(" ", 1)
        #Each ref key contains the hash for that ref
        refs[ref_name] = hash_val

    return refs

def get_staging_area(repo_path: str) -> list[dict]:
    '''Gets index/staging area'''
    result = run_cmd("git", "ls-files", "-s", cwd=repo_path)
    if not result:
        return []

    #Create dictionary items for each index
    index_items = []
    for line in result.strip().splitlines():
        line_parts = line.split(maxsplit=3)
        if len(line_parts) == 4:
            index_items.append({
                "mode": line_parts[0],
                "hash": line_parts[1],
                "stage": int(line_parts[2]),
                "file_path": line_parts[3]
            })
        
    return index_items