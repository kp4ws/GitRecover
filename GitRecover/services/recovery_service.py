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
import GitRecover.ai.llm_providerOLD as ai
import GitRecover.git.extractor as extractor
from GitRecover.models.schemas import RecoveryRequest, RepositoryState, GitHistory

class RecoveryService:
    def __init__(self):
        #TODO: Keep a list of historic records of the AI responses
        #TODO: Keep handle to current AI response (should this be displayed in console page?)
        pass

    def _create_request_payload(self, git_repo: str, user_prompt: str) -> RecoveryRequest:

        current_head: str = extractor.get_current_head(git_repo)
        staged: str = extractor.get_staging_area(git_repo)
        local_commits: str = extractor.get_local_commits(git_repo)

        repository_state = RepositoryState(
            head=current_head,
            refs=""
        )

        git_history = GitHistory(
            local_commits=local_commits.splitlines()
        )

        request = RecoveryRequest(
            repository_state=repository_state,
            git_history=git_history,
            user_prompt=user_prompt
        )

        json_payload: dict[str, object] = request.to_payload()
        return json_payload

    #TODO
    def _filter_ai_feedback(self, feedback: str):
         pass


    def handle_recovery(self, git_repo: str, user_prompt: str):
            recovery_request_payload = self._create_request_payload(git_repo, user_prompt)
            ai_feedback = ai.provide_feedback(recovery_request_payload)
            return ai_feedback