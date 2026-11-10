from pathlib import Path
from GitRecover.utils import run_cmd
from GitRecover.core.schemas import RepoStatus

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

def get_recent_commits(repo_path: str, max_count: int = 30) -> list[dict]:
    '''commits including those not part of commit tree (orphaned commits found via reflog)'''

    dangling_set = get_dangling_commits(repo_path)

    #creates a format template we can use in our command to format the output
    #Hash | Parents | Author | Date | Reflog Action
    reflog_format = "%H|%P|%an|%ad|%gs"
    result = run_cmd("git", "log", "-g", f"-n{max_count}", f"--format={reflog_format}", "--date=short", cwd=repo_path).strip()

    commits = []
    if result:
        for line in result.splitlines():
            line_parts = line.split("|", 4)
            if len(line_parts) == 5:
                commit_hash = line_parts[0]
                parents = []
                if line_parts[1]:
                    parents = line_parts[1].split()

                print(dangling_set, commit_hash)
                commits.append({
                    "hash": commit_hash,
                    "parents": parents,
                    "author": line_parts[2],
                    "date": line_parts[3],
                    "message": line_parts[4],
                    "is_dangling": commit_hash in dangling_set
                })

    return commits

def get_dangling_commits(repo_path: str) -> set[str]:
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