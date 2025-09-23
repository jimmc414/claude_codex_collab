# Claude Code Setup & Workflow Guide

## Overview
This project is configured with a complete Claude Code development environment integrated with GitHub Actions for automated CI/CD workflows.

## What We've Set Up

### 1. WSL2 Ubuntu Environment
- **OS**: Ubuntu 24.04.2 LTS on WSL2
- **Node.js**: v22.19.0
- **npm**: v10.9.3
- **Claude Code**: v1.0.120
- **GitHub CLI**: Authenticated and configured

### 2. Custom Commands & Functions

#### Bash Functions (in ~/.bashrc)
- **`init`**: Quick project starter
  - Changes to `/mnt/c/python`
  - Activates conda `llm` environment
  - Prompts for project name
  - Creates project folder if specified
  - Launches Claude Code with `--dangerously-skip-permissions` flag

- **`gh-upload`**: Creates public GitHub repository
  - Auto-detects folder name as repo name
  - Initializes git if needed
  - Commits all files
  - Creates and pushes to GitHub

- **`gh-upload-private`**: Same as above but creates private repo

- **`gh-describe`**: Updates repository description after creation

- **`gh-info`**: Displays current repository information

#### Claude Code Custom Commands (in /mnt/c/python/.claude/commands/)
- **`/project:github`**: Complete GitHub setup workflow (public)
- **`/project:github-private`**: Complete GitHub setup workflow (private)
- **`/project:describe`**: Update repository description

### 3. GitHub Integration
- GitHub Actions workflow installed
- Claude GitHub App configured for PR reviews
- API token saved as `CLAUDE_CODE_OAUTH_TOKEN` secret

## Workflow from Claude's Perspective

### Starting a New Project
1. User runs `init` in terminal
2. Claude Code launches in the project directory
3. Claude has access to:
   - All files in the current directory
   - Shell commands via `/shell`
   - Git operations
   - Project-specific commands in `.claude/commands/`

### Creating Files and Code
Claude can:
- Generate new files with `/generate` command
- Edit existing files
- Run tests and debug code
- Execute shell commands for package installation
- Commit changes to git

### GitHub Integration Workflow
When user runs `/project:github`:
1. Claude executes `gh-upload` function via shell
2. Repository is created and code is pushed
3. User is prompted to run `/install-github-app`
4. GitHub Actions workflow is set up
5. Claude can now:
   - Create pull requests
   - Run tests via GitHub Actions
   - Provide PR reviews
   - Suggest improvements

### Continuous Development
Claude assists with:
- Code refactoring and optimization
- Bug fixes and debugging
- Documentation generation
- Test creation and execution
- Git commit messages
- PR descriptions

## Available Commands

### Terminal Commands (run before starting Claude)
```bash
init                    # Start new project with Claude Code
```

### Claude Code Commands
```
/help                   # Show all available commands
/status                 # Check current setup
/shell <command>        # Execute shell commands
/generate <request>     # Generate new files/code
/edit <file>           # Edit existing files
/test                   # Run tests
/commit <message>       # Commit changes
/push                   # Push to GitHub
/pr                     # Create pull request
```

### Custom Project Commands
```
/project:github         # Upload to GitHub (public) and setup Actions
/project:github-private # Upload to GitHub (private) and setup Actions
/project:describe       # Update repository description
```

### Shell Functions (via /shell in Claude)
```
/shell gh-upload        # Create and push to public GitHub repo
/shell gh-upload-private # Create and push to private GitHub repo
/shell gh-describe "description" # Update repo description
/shell gh-info          # Show repository information
```

## File Structure
```
/mnt/c/python/
├── .claude/
│   └── commands/       # Global Claude Code commands
│       ├── github.md
│       ├── github-private.md
│       └── describe.md
├── claude_codex_collab/  # This project
│   ├── .git/
│   ├── .github/
│   │   └── workflows/  # GitHub Actions
│   ├── README.md
│   └── CLAUDE_SETUP_GUIDE.md  # This file
└── [other projects]/
```

## Best Practices

### For Optimal Performance
1. Work in WSL filesystem when possible (`~/projects/`) for better I/O
2. Use `/mnt/c/python/` for easy Windows access but expect slower operations
3. Keep project dependencies in virtual environments

### Git Workflow
1. Let Claude handle commit messages for consistency
2. Use descriptive PR titles
3. Allow Claude to review PRs before merging

### Security
- GitHub OAuth token is stored securely as GitHub secret
- API keys are not stored in code
- Use private repos for sensitive projects

### Tips for Claude Code
1. Be specific in requests - treat Claude like a senior developer
2. Use `/status` to verify setup before major operations
3. Review generated code before committing
4. Use `/test` frequently to catch issues early

## Troubleshooting

### Common Issues
- **"Claude Code not supported on Windows"**: Ensure you're in WSL Ubuntu terminal, not Windows CMD
- **Permission errors**: The `--dangerously-skip-permissions` flag handles most WSL permission issues
- **Slow file operations**: Normal when working in `/mnt/c/` - consider moving to WSL filesystem
- **GitHub auth issues**: Run `gh auth status` and re-authenticate if needed

### Reset Commands
```bash
# Re-authenticate GitHub
gh auth login

# Re-authenticate Claude Code
claude auth reset
claude auth login

# Check Claude Code health
claude doctor
```

## Environment Variables
The following are configured:
- `PATH`: Includes `~/.local/bin` and `~/.npm-global/bin`
- Conda environment: `llm` (activated via `init`)
- Git autocrlf: Set to `input` for cross-platform compatibility

## Next Steps
1. Create new projects with `init`
2. Use Claude for development assistance
3. Push to GitHub with `/project:github`
4. Let Claude handle PR reviews
5. Iterate and improve with AI assistance

---

*This setup was configured on January 23, 2025. Claude Code version 1.0.120.*
*For updates, check: https://docs.claude.com/en/docs/claude-code*
