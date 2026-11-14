from dataclasses import dataclass, field
from enum import Enum

class RepoStatus(Enum):
    CLEAN = "Clean"
    REBASE = "Rebasing"
    MERGE = "Merging"
    CHERRY_PICK = "Cherry-Picking"
    DETACHED = "Detached HEAD"
    DIRTY = "Dirty (Uncommitted Changes)"

class RemoteSyncStatus(Enum):
    NOT_CHECKED = "Not checked"
    NO_REMOTE = "No remote configured"
    NO_UPSTREAM = "No upstream configured"
    DETACHED = "Detached HEAD"
    UP_TO_DATE = "Up to date"
    AHEAD = "Ahead"
    BEHIND = "Behind"
    DIVERGED = "Diverged"
    ERROR = "Check failed"

@dataclass
class RemoteSyncInfo:
    status: RemoteSyncStatus = RemoteSyncStatus.NOT_CHECKED
    upstream: str = ""
    ahead: int = 0
    behind: int = 0
    error_message: str = ""

    @property
    def display_text(self) -> str:
        if self.status == RemoteSyncStatus.AHEAD:
            message = f"Ahead by {self.ahead} commit(s) of {self.upstream}"

        elif self.status == RemoteSyncStatus.BEHIND:
            message = f"Behind by {self.behind} commit(s) from {self.upstream}"

        elif self.status == RemoteSyncStatus.DIVERGED:
            message = f"Diverged from {self.upstream}: {self.ahead} ahead, {self.behind} behind"

        elif self.status == RemoteSyncStatus.UP_TO_DATE and self.upstream:
            message = f"Up to date with {self.upstream}"

        elif self.status == RemoteSyncStatus.ERROR:
            message = f"*ERROR*: {self.error_message}"

        else: 
            message = self.status.value

        return message

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
    git_action: str = ""

@dataclass
class RepositoryState:
    status: RepoStatus
    current_head: str = "Unknown"
    current_branch: str = ""
    staging_area: list[IndexItem] = field(default_factory=list)
    remote_sync: RemoteSyncInfo = field(default_factory=RemoteSyncInfo)

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