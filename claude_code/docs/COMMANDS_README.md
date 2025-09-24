# Claude Code Commands Setup

## Quick Setup

Run this command from your WSL terminal:

```bash
cd /mnt/c/python/claude_codex_collab
chmod +x setup_claude_commands.sh
./setup_claude_commands.sh
```

This will copy all Claude Code custom commands to the global location (`~/.claude/commands/`).

## Available Commands

After setup, you'll have these commands available in Claude Code:

- `/github` - Create public GitHub repo and setup Actions
- `/github-private` - Create private GitHub repo and setup Actions
- `/describe` - Update repository description
- `/push` - Quick commit and push changes
- `/pull` - Fetch latest from GitHub
- `/sync` - Pull latest, then commit and push

## Manual Installation

If you prefer to copy commands manually:

```bash
cp /mnt/c/python/claude_codex_collab/claude_commands/*.md ~/.claude/commands/
```

## After Installation

1. Restart Claude Code: `claude --dangerously-skip-permissions`
2. Verify commands are available: `/help`
3. Start using the commands in any project!

## Files Included

- `github.md` - Public repo creation workflow
- `github-private.md` - Private repo creation workflow
- `describe.md` - Update repo description
- `push.md` - Commit and push changes
- `pull.md` - Fetch and merge from remote
- `sync.md` - Full sync (pull then push)
