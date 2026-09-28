import os
import re
import sys
import zlib

class CommitNode:
    msg: str = ""
    hash: str = ""
    parent = None

    def __init__(self, hash, msg):
        self.hash = hash
        self.msg = msg
        self.parent = None

if not os.path.exists(".git"):
    sys.stderr.write("Error: .git directory not found.\n")
    sys.exit(1)

branch = sys.argv[1] if len(sys.argv) > 1 else "main"

with open(os.path.join(".git", "refs", "heads", branch), "r") as f:
    head = f.read().strip()

next_commit = head
root = None
curr = None

moreCommits = True
while moreCommits:
    #TODO Currently not working. Look into loose objects and packfiles
    with open(os.path.join(".git", "objects", next_commit[:2], next_commit[2:]), "rb") as f:
        data = f.read()

    contents = zlib.decompress(data).decode()
    r = re.search("parent [0-9a-f]+", contents)
    parent = None

    if r is None:
        moreCommits = False
    else:
        parent = r.group(0).split()[1:] #Determine if should be 1: or 7:
        next_commit = parent
    
    msg = re.search("message\n\n.*", contents).group(0)

    if root is None:
        root = CommitNode(next_commit, msg)
        curr = root
    else:
        curr.parent = CommitNode(next_commit, msg)
        curr = curr.parent

curr = root
while curr is not None:
    print(f"Commit: {curr.hash}\nMessage: {curr.msg}\n")
    if curr.parent is not None:
        print(f"Parent: {curr.parent.hash}\n")
    curr = curr.parent