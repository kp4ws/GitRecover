from dataclasses import dataclass, asdict

@dataclass
class RepositoryState:
    head: str
    refs: list[str]

@dataclass
class GitHistory:
    local_commits: list[str]

@dataclass
class RecoveryRequest:
    repository_state: RepositoryState
    git_history: GitHistory
    user_prompt: str

    def to_payload(self) -> dict[str, object]:
        return asdict(self)

# "repository_state": {
#     "structure": repo_structure.splitlines(),
#     "current_branch": "",
#     "current_head": head,
#     "index": git_staging,
#     "modified_files": modified_files,
#     "local_commits": local_commits,
#     "refs": git_refs,
#     "fsck_checks": fsck_checks
# },

# "git_history": {
#     "commits": [{"hash": "", "message": "", "action": ""}],
#     "reflog_entries": [],
#     "dangling_commits": []
# },

# "user_context": {
#     "prompt": user_prompt
# }