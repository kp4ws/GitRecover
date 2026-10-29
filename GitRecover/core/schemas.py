from dataclasses import dataclass, asdict
import json

@dataclass
class GitCommit:
    hash: str
    message: str
    date: str
    author: str

@dataclass
class RepositoryState:
    head: str
    refs: list[str]
    status: str #TODO This should be changed to enum
    current_head: str
    current_branch: str
    is_dirty: bool

@dataclass
class GitHistory:
    local_commits: list[str]
    staged: str

@dataclass
class RecoveryRequest:
    repository_state: RepositoryState
    git_history: GitHistory
    user_prompt: str
    repo_path: str
    chat_history: list[str]

    def to_payload(self) -> dict[str, object]:
        return asdict(self)

    def save_to_disk(self, filepath: str):
        with open(filepath, "w") as f:
            json.dump(self.to_payload(), f, indent=2)

    def load_from_disk(self, filepath: str):
        with open(filepath, "r") as f:
            data = json.dumpstr()

        return data