#TODO: Consider adding these within git directory to separate git models from llm models
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