# Claude Code Setup & Workflow Guide

## Overview

This project ships with a complete Claude Code development environment configured for GitHub Actions. The setup described below outlines the baseline tooling, supporting scripts, and recommended practices for working within the workflow.

## Environment Summary

- **OS**: Ubuntu 24.04.2 LTS on WSL2
- **Node.js**: v22.19.0
- **npm**: v10.9.3
- **Claude Code**: v1.0.120
- **GitHub CLI**: Authenticated and configured for the associated account

## Custom Commands and Functions

### Bash Functions (defined in `~/.bashrc`)
- **`init`**: Sets the working directory, activates the `llm` Conda environment, prompts for a project name, creates the project folder when provided, and launches Claude Code with the `--dangerously-skip-permissions` flag
- **`gh-upload`**: Creates a public GitHub repository, initializing git when necessary, committing files, and pushing the initial revision
- **`gh-upload-private`**: Same workflow as `gh-upload`, but creates a private repository
- **`gh-describe`**: Updates the repository description
- **`gh-info`**: Displays information about the current repository

### Claude Code Command Files (stored in `~/.claude/commands/`)
- **`/github`**: Runs the public repository setup workflow
- **`/github-private`**: Creates a private repository
- **`/describe`**: Updates the repository description interactively
- **`/push`**: Commits and pushes all changes
- **`/pull`**: Fetches and merges the latest changes
- **`/sync`**: Pulls remote updates, then commits and pushes local changes

## GitHub Integration

- GitHub Actions workflows are installed and ready to run
- The Claude GitHub App is configured for pull request reviews
- The required API token is stored as the `CLAUDE_CODE_OAUTH_TOKEN` secret

## Pipeline Workflow

### Starting a Project

1. Run `init` in the terminal to open Claude Code in the project directory
2. Claude Code receives access to project files, shell commands, git operations, and the global command directory
3. Use the command palette or slash commands to perform project tasks

### Working with Files and Code

- Generate files with `/generate`
- Edit existing files, execute tests, and run shell commands using the CLI interface
- Commit and push changes as work progresses

### GitHub Workflow

1. Execute `/github` to create a repository and push the current project state
2. Install the Claude GitHub App for automated reviews when prompted
3. Use the available commands to create pull requests, run tests, and review results

### Continuous Development Support

Claude Code tooling streamlines:
- Refactoring and optimization tasks
- Bug investigations
- Documentation updates
- Test creation and execution
- Commit message generation
- Pull request summaries

## Available Commands

### Terminal Commands (run before launching Claude Code)
```bash
init  # Start a new project using the configured workflow
```

### Claude Code Commands
```
/help                   # List available commands
/status                 # View current setup details
!<command>              # Execute shell commands
/generate <request>     # Produce files or code snippets
/edit <file>            # Modify an existing file
/test                   # Run project tests
!git commit -m "msg"    # Commit changes
!git push               # Push updates to GitHub
/pr                     # Create a pull request (when supported)
```

### Global Command Files (`~/.claude/commands/`)
```
/github         # Public repository workflow
/github-private # Private repository workflow
/describe       # Update repository description
/push           # Commit and push changes
/pull           # Fetch and merge remote updates
/sync           # Pull remote updates, then commit and push local changes
```

### Bash Functions Accessible from Claude Code (`!` or `/shell`)
```
!gh-upload                 # Create and push to a public GitHub repository
!gh-upload-private         # Create and push to a private GitHub repository
!gh-describe "description" # Update repository description
!gh-info                   # Display repository information
!git add . && git commit -m "msg" && git push  # Commit and push quickly

# Some contexts prefer /shell over ! for executing bash commands
```

## File Structure

```
~/                       # Linux home directory
├── .bashrc              # Custom bash functions
├── .claude/
│   └── commands/        # Global Claude Code commands
│       ├── github.md
│       ├── github-private.md
│       ├── describe.md
│       ├── push.md
│       ├── pull.md
│       └── sync.md
└── .local/bin/claude    # Claude Code binary

/mnt/c/python/
├── claude_codex_collab/ # This project
│   ├── .git/
│   ├── .github/
│   │   └── workflows/   # GitHub Actions definitions
│   ├── README.md
│   └── claude_code/docs/CLAUDE_SETUP_GUIDE.md
└── [other projects]/
```

## Best Practices

### Performance
1. Prefer working within the WSL filesystem (`~/projects/`) for faster I/O
2. Use `/mnt/c/python/` only when Windows-side access is required, understanding that file operations may be slower
3. Keep dependencies isolated in virtual environments

### Git Workflow
1. Use the provided commands to keep commit messages consistent
2. Apply descriptive titles to pull requests
3. Allow automated reviews to complete before merging

### Security
- Store OAuth tokens in GitHub secrets
- Avoid committing API keys or other sensitive data
- Use private repositories for confidential work

### Working Efficiently with the CLI
1. Provide specific prompts when generating code or documentation
2. Run `/status` to confirm environment readiness
3. Review generated code prior to committing
4. Execute `/test` frequently to catch regressions

## Troubleshooting

### Common Issues
- **Claude Code unavailable on Windows terminals**: Launch the WSL Ubuntu terminal instead of Windows Command Prompt
- **Permission errors**: Launch Claude Code with `--dangerously-skip-permissions`
- **Slow file operations**: Move projects from `/mnt/c/` to the WSL filesystem when possible
- **GitHub authentication problems**: Run `gh auth status` and reauthenticate as needed
- **Missing commands**: Restart Claude Code after adding files to `~/.claude/commands/`

### Reset Commands
```bash
# Re-authenticate GitHub
gh auth login

# Reset Claude Code credentials
claude auth reset
claude auth login

# Diagnose Claude Code issues
claude doctor
```

## Environment Variables

- `PATH`: Includes `~/.local/bin` (Claude Code binary) and `~/.npm-global/bin`
- Conda environment: `llm`
- Git `autocrlf`: set to `input` for consistent line endings

## Next Steps

1. Launch new projects with `init`
2. Use the provided commands to manage development tasks
3. Push repositories to GitHub with `/github`
4. Keep local copies synchronized with `/pull` and `/push`
5. Rely on the workflow scripts for pull request reviews and iteration support

---

*Configuration captured on January 23, 2025 for Claude Code version 1.0.120. Refer to https://docs.claude.com/en/docs/claude-code for updates.*
