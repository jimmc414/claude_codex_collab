---
description: Complete GitHub setup with Actions
---

Execute the GitHub upload process:
```bash
repo_name=$(basename "$PWD")
gh_user=$(gh api user --jq .login)

[ ! -d .git ] && git init

git add .
git commit -m "Initial commit" 2>/dev/null || git commit -m "Update"

echo "Creating GitHub repo: $repo_name"
gh repo create "$repo_name" --public --source=. --remote=origin --push

echo ""
echo "✅ Repository created: https://github.com/$gh_user/$repo_name"
echo ""
echo "NEXT STEP: Run /install-github-app and enter: $gh_user/$repo_name"
echo "$gh_user/$repo_name" > .github_repo
