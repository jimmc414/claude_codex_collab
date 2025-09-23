---
description: Fetch and merge latest changes from GitHub
---

Fetch and merge latest changes from the remote repository:

!git pull

Or if you need to handle divergent branches:
!git pull --no-rebase

To just fetch without merging:
!git fetch

To see what's different before merging:
!git fetch && git status
