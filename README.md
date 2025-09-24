# Claude Codex Collab - Dual Workflow Development Pipeline

This repository implements a structured development pipeline with two automation tracks: Claude Code and Codex. Each track includes configuration, commands, and documentation for running a repeatable software delivery process with GitHub Actions integration.

## Repository Structure

```
/
├── claude_code/        # Claude Code workflow implementation
│   ├── pipeline/       # Claude-specific pipeline configuration
│   ├── commands/       # Claude command definitions
│   └── docs/           # Claude documentation
│
├── codex/              # Codex workflow implementation
│   ├── pipeline/       # Codex-specific pipeline configuration
│   ├── commands/       # Codex commands
│   └── docs/           # Codex documentation
│
├── shared/             # Shared resources between workflows
│   ├── docs/           # Generated project documentation
│   ├── src/            # Generated source code
│   └── utils/          # Shared utilities
│
└── .github/            # GitHub Actions workflows
    ├── workflows/
    │   ├── claude/     # Claude-specific workflows
    │   └── codex/      # Codex workflows
    └── scripts/
        ├── claude/     # Claude validation scripts
        └── codex/      # Codex validation scripts
```

## Quick Start

### Claude Code Track

1. Navigate to the Claude Code documentation:
   ```bash
   cd claude_code
   cat docs/PIPELINE_USAGE_GUIDE.md
   ```
2. Review the setup guide for local environment details:
   ```bash
   cat docs/CLAUDE_SETUP_GUIDE.md
   ```
3. Follow the usage guide to work through the requirements, architecture, implementation planning, coding, and review phases.

### Codex Track

1. Review the Codex documentation:
   ```bash
   cd codex
   cat README.md
   ```
2. Complete the workflow configuration steps documented in the Codex directory as they become available.

## Pipeline Workflow

Both tracks follow the same progression:

1. **Requirements Gathering** – Produce `shared/docs/requirements.md`
2. **Architecture Design** – Create `shared/docs/architecture.md`
3. **Implementation Planning** – Produce `shared/docs/implementation.md`
4. **Code Implementation** – Build project assets in `shared/src/`
5. **Review & Iteration** – Run GitHub Actions and address feedback until all checks pass

## Key Features

- **Dual Workflow Support**: Choose between Claude Code and Codex configurations
- **GitHub Actions Integration**: Automated validation at each pipeline phase
- **Shared Resources**: Centralized documentation and source directories
- **Quality Gates**: Configurable acceptance thresholds
- **Traceability**: Requirements tracked through to implementation
- **Continuous Feedback**: Automated review loops for every stage

## Naming Conventions

### Claude Code Track
- Branches: `claude/feature-name`
- PR Labels: `claude-code`
- Workflows: `claude-*.yml`
- Config prefix: `claude_`

### Codex Track
- Branches: `codex/feature-name`
- PR Labels: `codex`
- Workflows: `codex-*.yml`
- Config prefix: `codex_`

## GitHub Actions

### Claude Workflows
Located in `.github/workflows/claude/`:
- `requirements-review.yml` – Validates requirements documents
- `architecture-review.yml` – Reviews architecture designs
- `implementation-review.yml` – Checks implementation plans
- `code-review.yml` – Performs code quality checks
- `final-review.yml` – Runs comprehensive validation

### Codex Workflows
Located in `.github/workflows/codex/`:
- `codex-pipeline.yml` – Main Codex pipeline (template)
- Additional workflows will be added as the track is expanded

## Configuration

### Claude Code Configuration
- Pipeline: `claude_code/pipeline/config/pipeline_config.yml`
- Readiness: `claude_code/pipeline/config/readiness_criteria.yml`

### Codex Configuration
- Pipeline: `codex/pipeline/config/pipeline_config.yml`
- Additional configuration files to be documented in future updates

## Documentation

- `claude_code/docs/PIPELINE_USAGE_GUIDE.md`
- `claude_code/docs/CLAUDE_SETUP_GUIDE.md`
- `codex/README.md`

## Contributing

1. Use the appropriate workflow directory for your changes
2. Follow the naming conventions for branches and pull requests
3. Update documentation as part of any change
4. Ensure GitHub Actions checks pass before requesting a review

## Metrics

Both tracks monitor:
- Requirements coverage
- Test coverage
- Code quality scores
- Time per phase
- Review iterations

## Links

- [Claude Code Issues](https://github.com/anthropics/claude-code/issues)
- [Repository](https://github.com/jimmc414/claude_codex_collab)

## License

License details will be added when available.
