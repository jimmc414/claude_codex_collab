---
description: Quick commit and push to GitHub
---

Execute the git push process:
```bash
# Check if there are changes to commit
if git diff --quiet && git diff --cached --quiet && [ -z "$(git ls-files --others --exclude-standard)" ]; then
    echo "✅ No changes to push. Repository is up to date."
else
    # Add all changes
    git add .

    # Get a simple commit message or use default
    commit_msg="${1:-Update files}"

    # Commit and push
    git commit -m "$commit_msg"
    git push

    echo "✅ Successfully pushed changes to GitHub!"
fi
```
