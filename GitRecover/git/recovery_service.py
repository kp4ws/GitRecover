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
from GitRecover.ai.ollama_provider import provide_feedback
import GitRecover.utils as utils
from GitRecover.git.recovery_request import RecoveryRequest, RepositoryState, GitHistory

#TODO Determine if a class is needed or not (currently its not storing any state)
class RecoveryService():
    def __init__(self):
        pass

    def _create_recovery_request(self, git_repo: str, user_prompt: str) -> RecoveryRequest:
        repo_structure: str = utils.run_cmd("git repo structure --format=lines", git_repo)
        local_commits: str = utils.run_cmd("git cherry -v", git_repo)
        git_refs: str = utils.run_cmd("git for-each-ref", git_repo)
        git_staging: str = utils.run_cmd("git ls-files -s", git_repo)
        modified_files: str = utils.run_cmd("git ls-files -s", git_repo)
        head: str = utils.run_cmd("git rev-parse HEAD", git_repo)
        fsck_checks: str = utils.run_cmd("git fsck --full --strict --unreachable --dangling --lost-found --verbose", git_repo)

        payload = RecoveryRequest(
            repository_state=RepositoryState(
                head="",
                refs=""
            ),
            git_history=GitHistory(
                local_commits=[""]
            ),
            user_prompt=user_prompt
        )

        return payload

    def handle_recovery(self, git_repo: str, user_prompt: str):
        recovery_request = self._create_recovery_request(git_repo, user_prompt)
        ai_feedback = provide_feedback(recovery_request.to_payload())
        return ai_feedback