from dataclasses import dataclass, field
from enum import Enum

class RepoStatus(Enum):
    CLEAN = "Clean"
    REBASE = "Rebasing"
    MERGE = "Merging"
    CHERRY_PICK = "Cherry-Picking"
    DETACHED = "Detached HEAD"
    DIRTY = "Dirty (Uncommitted Changes)"

@dataclass
class IndexItem:
    mode: str
    hash: str
    stage: int
    file_path: str

    @property
    def is_conflict(self) -> bool:
        '''stage > 0 => active merge conflict'''
        return self.stage > 0

@dataclass
class GitCommit:
    hash: str
    message: str
    author: str
    date: str
    is_dangling: bool = False
    parents: list[str] = field(default_factory=list)

@dataclass
class RepositoryState:
    status: RepoStatus
    current_head: str = "Unknown"
    current_branch: str = ""
    staging_area: list[IndexItem] = field(default_factory=list)

    @property
    def is_clean(self) -> bool:
        return self.status == RepoStatus.CLEAN

@dataclass
class RepositoryHistory:
    commit_history: list[GitCommit]
    refs: dict[str, str] = field(default_factory=dict)
    unpushed_commits: str = ""

@dataclass
class RecoveryRequest:
    repo_path: str
    state: RepositoryState
    history: RepositoryHistory
    chat_history: list[str] = field(default_factory=list)