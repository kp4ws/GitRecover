# Scenarios
The following scenarios are used for testing out the app's performance against common git issues that developers run into.  

## Direct Commit to Main
Occurs when developers accidentally commit changes without realizing they're on the main branch

To simulate this scenario, enter the following command:  
`committed_to_main.py`

## Merge Conflicts
Occurs when multiple developers modify the same file, results in a merge conflict.

To simulate this scenario, enter the following command:  
`merge_conflict.py`
 
## Bad Merges
Occurs when merge goes bad, and unintended changes are merged.  

To simulate this scenario, enter the following command:  
`bad_merge.py`

## Unmerged Branch Deletion
Occurs when the developer accidentally deletes a branch that hasn't been merged yet.  

To simulate this scenario, enter the following command:  
`unmerged_branch_deletion.py`

## Lost Work from Hard Reset
Typically happens when developer tries to undo something by using `git reset --hard` but accidentally loses their work. 

To simulate this scenario, enter the following command:  
`hard_reset.py`

## Lost Uncommitted Staged Files
Occurs when developers lose their work they've staged, typically due to a hard reset.  

To simulate this scenario, enter the following command:  
`uncommitted_staged_changes.py`

## Dropped Stash
Occurs when developer accidentally runs `git stash drop` which removes anything they have stored in the stash  

To simulate this scenario, enter the following command:  
`dropped_stash.py`

## Messed up Rebase
Occurs when branch history is broken during a rebase operation.  

To simulate this scenario, enter the following command:  
`bad_rebase.py`

## Detached HEAD mistakes
Occurs when a developer looks at older commits and accidentally make additional commits while at the older commit, causing the newer commits to be lost.  

To simulate this scenario, enter the following command:  
`detached_head.py`