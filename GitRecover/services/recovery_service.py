"""
Porcelain commands: The regular git commands that are used
Plumbing commands: The low level git commands that may be used behind the scenes

CORE PARTS OF GIT:
- HEAD file: Points to the branch you currently have checked out
- index file: Where Git stores staging information
- objects directory: Stores all content for database
- refs directory: Stores pointers into commit objects in that data (branches, tags, remotes, and more)

Git is a key-value data store -> Unique keys are generated for stored content objects
SHA1 hash:
2 characters = subdirectory
remaining 38 characters = filename

git cat-file swiss army knife for inspecting Git objects.
git hash-object used for writing objects into database


The initial format in which Git saves objects on disk is called a “loose” object format. 
However, occasionally Git packs up several of these objects into a single binary file called a “packfile” in order to save space and be more efficient. 
Git does this if you have too many loose objects around, if you run the git gc command manually, or if you push to a remote server. 


git log -g, which will give you a normal log output for your reflog.
git fsck --full

NOTE: For commands, such as git reflog, that work on readable files, I'll be creating custom implementations of them
For other binary files (pack files, etc) I'll be using plumbing commands (git fsck, git cat-file, etc) under the hood and extracting data from them
"""
import GitRecover.git.extractor as extractor
from GitRecover.ai.llm_provider import LLMProvider
from GitRecover.services.schemas import RecoveryRequest, RepositoryState, GitHistory

class RecoveryService:
    def __init__(self, llm_provider):
        self.llm_provider: LLMProvider = llm_provider
        self.active_session: RecoveryRequest | None = None
    
    def _create_active_session(self, repo_path: str, user_prompt: str) -> RecoveryRequest:
        current_head: str = extractor.get_current_head(repo_path)
        staged: str = extractor.get_staging_area(repo_path)
        local_commits: str = extractor.get_local_commits(repo_path)

        repository_state = RepositoryState(
            head=current_head,
            refs=""
        )

        git_history = GitHistory(
            local_commits=local_commits.splitlines(),
            staged=staged
        )

        request = RecoveryRequest(
            repository_state=repository_state,
            git_history=git_history,
            user_prompt=user_prompt,
            repo_path=repo_path,
            chat_history=["tes"]
        )

        return request

    def create_recovery_request(self, repo_path: str, user_prompt: str):
        self.active_session = self._create_active_session(repo_path, user_prompt)
        # self.save_recovery_request()
        # payload = self._create_request_payload(repo_path, user_prompt)
        # ai_feedback = self.llm_provider.generate_response(payload)
        # return ai_feedback

    def import_recovery_request(self, repo_path):
        self.active_session.load_from_disk(repo_path)

    def save_recovery_request(self, recovery_request: RecoveryRequest):
        with open ("", "w") as f:
            pass

    def handle_chat_message(self, user_message: str):
        if not self.active_session:
            print("No active session")
            return 

        chat_history = self.active_session.chat_history
        chat_history.append({"role": "user", "content": user_message})
        ai_response = self.llm_provider.generate_response(chat_history)
        chat_history.append({"role": "assistant", "content": ai_response})

        return ai_response