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
from GitRecover.core.schemas import RecoveryRequest, RepositoryState, RepositoryHistory, RepoStatus, GitCommit, IndexItem

class RecoveryService:
    def __init__(self, llm_provider):
        self.llm_provider: LLMProvider = llm_provider
        self.active_session: RecoveryRequest | None = None
    
    def _create_active_session(self, repo_path: str) -> RecoveryRequest:
        current_head: str = extractor.get_current_head(repo_path)
        current_branch: str = extractor.get_current_branch(repo_path)
        repo_status = extractor.get_repo_status(repo_path)

        #TODO staging area
        #TODO refs
        #TODO unpushed commits

        repo_state = RepositoryState(
            status = repo_status,
            current_head = current_head,
            current_branch = current_branch,

        )

        raw_commits = extractor.get_recent_commits(repo_path)
        commit_history = []
        for commit in raw_commits:
            commit_history.append(GitCommit(
                hash=commit["hash"],
                message=commit["message"],
                author=commit["author"],
                date=commit["date"],
                parents=commit["parents"],
                is_dangling=commit["is_dangling"]
            ))
        
        repo_history = RepositoryHistory(
            commit_history=commit_history
        )
        
        request = RecoveryRequest(
            repo_path = repo_path,
            state = repo_state,
            history = repo_history,
            chat_history = []
        )

        return request

    def create_recovery_request(self, repo_path: str, progress_callback=None):
        progress_callback(0, "Extracting Git Data...")
        self.active_session = self._create_active_session(repo_path)
        progress_callback(40, "Initializing Local LLM...")
        self.llm_provider.load_model()
        
        #TODO Get initial feedback from AI regarding their diagnosis of repository
        # progress_callback(50, "Diagnosing Repository Health...")
        #TODO I think this AI feedback should be popup because otherwise it will become stale when user chats more in AI window
        # ai_feedback = self.llm_provider.generate_response(payload)
        
        progress_callback(100, "Recovery Request Active")
        
        #TODO: determine if method should return anything or not
        # return ai_feedback

    def handle_chat_message(self, user_message: str, progress_callback=None):
        if not self.active_session:
            return "Error: No active Git recovery session."

        chat_history = self.active_session.chat_history
        chat_history.append({"role": "user", "content": user_message})
        ai_response = self.llm_provider.generate_response(chat_history)
        chat_history.append({"role": "assistant", "content": ai_response})

        #TODO create filtering mechanism where if AI response certainty is low, system forces it to retry up to N times
        return ai_response