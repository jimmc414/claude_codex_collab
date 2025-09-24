# Claude Code Commands Setup

## Quick Setup

Run the following from your WSL terminal:

```bash
cd /mnt/c/python/claude_codex_collab
chmod +x setup_claude_commands.sh
./setup_claude_commands.sh
```

The script copies the Claude Code command files into `~/.claude/commands/` so they are available globally.

## Available Commands

After installation, the Claude Code CLI exposes these commands:

- `/github` – Create a public GitHub repository and configure Actions
- `/github-private` – Create a private GitHub repository and configure Actions
- `/describe` – Update the repository description
- `/push` – Commit and push changes
- `/pull` – Fetch the latest changes from GitHub
- `/sync` – Pull the latest updates, then commit and push local changes

## Manual Installation

Copy the command files manually if you prefer not to run the script:

```bash
cp /mnt/c/python/claude_codex_collab/claude_commands/*.md ~/.claude/commands/
```

## Post-Installation Steps

1. Restart Claude Code (`claude --dangerously-skip-permissions`)
2. Confirm the commands are available with `/help`
3. Apply the commands in your projects as needed

## Files Included

- `github.md` – Public repository workflow
- `github-private.md` – Private repository workflow
- `describe.md` – Update repository description
- `push.md` – Commit and push changes
- `pull.md` – Fetch and merge updates
- `sync.md` – Complete synchronization workflow
