# Collaboration Toolkit for Claude Code and Codex

This repository houses two parallel workflows so teams can drive software projects with either
Claude Code or GPT-based Codex tooling without configuration conflicts.

- `claude_commands/` — prompt templates and automation helpers tailored for Claude Code.
- `codex/` — the Codex-oriented pipeline CLI, documentation, and generated artifacts. See
  [`codex/README.md`](codex/README.md) for complete usage instructions.
- `CLAUDE_SETUP_GUIDE.md` — step-by-step setup notes for the Claude Code environment.
- `COMMANDS_README.md` — shared command reference that applies to both workflows.

Each workflow keeps its own naming conventions, directories, and persistent state so the two
systems can coexist in the same repository without overwriting each other's files.

## Getting started

1. Decide which workflow you want to use (Claude Code or GPT-5 Codex/Pro).
2. Follow the corresponding guide:
   - Claude Code: review `CLAUDE_SETUP_GUIDE.md` and the prompt files under `claude_commands/`.
   - Codex: install Python 3.10+, then run the CLI commands documented in `codex/README.md`.
3. Keep commits scoped to one workflow's directory to maintain the separation between tooling
   ecosystems.

Both workflows can share the same git repository and GitHub automation, but their assets remain
isolated to avoid naming collisions or accidental overwrites.
