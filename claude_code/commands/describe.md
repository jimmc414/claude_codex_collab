---
description: Update GitHub repository description interactively
---

Enter your description when prompted:

/shell bash -c 'read -p "Enter description: " desc && gh repo edit $(basename "$PWD") --description "$desc" && echo "✅ Description updated!"'
