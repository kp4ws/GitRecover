import os
import re
import sys
import zlib
import subprocess

"""
Porcelain commands: The regular git commands that are used
Plumbing commands: The low level git commands that may be used behind the scenes
->"Many of these commands aren’t meant to be used manually on the command line, but rather to be used as building blocks for new tools and custom scripts."
https://git-scm.com/book/en/v2/Git-Internals-Plumbing-and-Porcelain

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

class CommitNode:
    def __init__(self, hash, msg):
        self.hash = hash
        self.msg = msg
        self.parent = None

def get_commit_contents(commit_hash):
    """
    No easy way to read packfiles (binary) so seems like we need to use git cat-file -p command
    """
    result = subprocess.run(
        ["git", "cat-file", "-p", commit_hash],
        capture_output=True, text=True, check=True
    )
    return result.stdout

def git_log():
    if not os.path.exists(".git"):
        sys.stderr.write("Error: .git directory not found.\n")
        sys.exit(1)

    #TODO: Could instead use git rev-parse head cmd here
    branch = sys.argv[1] if len(sys.argv) > 1 else "main"
    with open(os.path.join(".git", "refs", "heads", branch), "r") as f:
        head = f.read().strip()

    current_hash = head
    root = None
    curr = None

    while current_hash:
        commit_contents = get_commit_contents(current_hash)
        if not commit_contents:
            break

        next_hash = None
        msg = ""

        #extract parent
        parent_match = re.search(r"parent ([0-9a-f]+)", commit_contents)        
        if parent_match:
            next_hash = parent_match.group(1)

        #extract message
        msg_match = re.search(r"\n\n(.*)", commit_contents, re.DOTALL)
        msg = msg_match.group(1).strip()

        new_node = CommitNode(current_hash, msg)

        if root is None:
            root = new_node
            curr = root
        else:
            curr.parent = new_node
            curr = curr.parent

        current_hash = next_hash

    curr = root
    while curr is not None:
        print(f"Commit: {curr.hash}\nMessage: {curr.msg}")
        if curr.parent is not None:
            print(f"Parent: {curr.parent.hash}\n")
        curr = curr.parent