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
from GitRecover.core.schemas import GitCommit, RecoveryRequest, RepositoryHistory, RepositoryState

class RecoveryService:
    def __init__(self, llm_provider):
        self.llm_provider: LLMProvider = llm_provider
        self.active_session: RecoveryRequest | None = None
    
    def _create_active_session(self, repo_path: str) -> RecoveryRequest:
        current_head: str = extractor.get_current_head(repo_path)
        current_branch: str = extractor.get_current_branch(repo_path)
        repo_status = extractor.get_repo_status(repo_path)

        #TODO If time permits, consider adding additional git entries to the request (staging area, refs, unpushed commits)

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
                is_dangling=commit["is_dangling"],
                git_action=commit["git_action"],
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

    def _prepare_recovery_context(self, request: RecoveryRequest) -> str:
        context = f"Repository: {request.repo_path}\n"
        context += f"Status: {request.state.status.value}\n"

        if request.state.current_branch != "":
            context += f"Branch: {request.state.current_branch}\n"
        else:
            context += "Detatched HEAD\n"

        context += f"HEAD: {request.state.current_head}\n"
        context += f"Remote sync: {request.state.remote_sync.display_text}\n"

        #Only check 15 most recent commits for dangling
        max_dangling_check = min(len(request.history.commit_history), 15)
        for i in range(0, max_dangling_check):
            commit = request.history.commit_history[i] 
            if commit.is_dangling:
                context+= f"Dangling commit: {commit.hash}\n"

        return context

    def create_recovery_request(self, repo_path: str, progress_callback=None):
        progress_callback(0, "Extracting Git Data...")
        self.active_session = self._create_active_session(repo_path)
        progress_callback(25, "Checking Remote Sync...")
        self.active_session.state.remote_sync = extractor.get_remote_sync_info(repo_path)
        progress_callback(40, "Initializing Local LLM...")
        self.llm_provider.load_model()
        
        progress_callback(100, "Recovery Request Active")
        
    def generate_diagnostic_suggestion():
        pass #TODO if time permits, this function could be used to generate an AI suggestion for recovery request report

    def handle_chat_message(self, user_message: str, progress_callback=None):
        if not self.active_session:
            return "Error: No active Git recovery session."

        if progress_callback is not None:
            progress_callback(0, "Generating AI response")

        chat_history = self.active_session.chat_history
        pending_history = [*chat_history, {"role": "user", "content": user_message}]
        
        context = self._prepare_recovery_context(self.active_session)
        ai_response = self.llm_provider.generate_response(pending_history, context)
        
        #Update chat history
        chat_history.append({"role": "user", "content": user_message})
        chat_history.append({"role": "assistant", "content": ai_response})

        #TODO create filtering mechanism where if AI response certainty is low, system forces it to retry up to N times
        if progress_callback is not None:
            progress_callback(100, "AI response ready.")
        return ai_response