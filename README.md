# Claude Codex Collab - Dual Agent Development Pipeline

This repository implements a systematic development pipeline using two agents: Claude Code and Codex.

## Repository Structure

```
/
├── claude_code/        # Claude Code agent implementation
│   ├── pipeline/       # Claude-specific pipeline configuration
│   ├── commands/       # Claude slash commands
│   └── docs/          # Claude documentation
│
├── codex/             # Codex agent implementation
│   ├── pipeline/       # Codex-specific pipeline configuration
│   ├── commands/       # Codex commands
│   └── docs/          # Codex documentation
│
├── shared/            # Shared resources between agents
│   ├── docs/          # Generated project documentation
│   ├── src/           # Generated source code
│   └── utils/         # Shared utilities
│
└── .github/           # GitHub Actions workflows
    ├── workflows/
    │   ├── claude/    # Claude-specific workflows
    │   └── codex/     # Codex-specific workflows
    └── scripts/
        ├── claude/    # Claude validation scripts
        └── codex/     # Codex validation scripts
```

## Quick Start

### Using Claude Code

1. Navigate to Claude Code documentation:
   ```bash
   cd claude_code
   cat docs/PIPELINE_USAGE_GUIDE.md
   ```

2. Start a new project:
   ```
   "Let's build a [project type] using Claude pipeline"
   ```

3. The pipeline proceeds through:
   - Requirements gathering
   - Architecture design
   - Implementation planning
   - Code generation
   - Automated review cycles

### Using Codex

1. Navigate to Codex documentation:
   ```bash
   cd codex
   cat README.md
   ```

2. [Codex implementation details to be added]

## Pipeline Workflow

Both agents follow this systematic approach:

1. **Requirements Gathering** → Generate `shared/docs/requirements.md`
2. **Architecture Design** → Create `shared/docs/architecture.md`
3. **Implementation Planning** → Produce `shared/docs/implementation.md`
4. **Code Implementation** → Build in `shared/src/`
5. **Review & Iteration** → Continuous feedback via GitHub Actions

## Key Features

- **Dual Agent Support**: Use Claude Code or Codex based on your needs
- **GitHub Actions Integration**: Automated review at each pipeline phase
- **Shared Resources**: Both agents can work on the same project
- **Quality Gates**: Configurable thresholds for each phase
- **Traceability**: Requirements tracked through implementation
- **Continuous Feedback**: Real-time validation and iteration

## Naming Conventions

### Claude Code
- Branches: `claude/feature-name`
- PR Labels: `claude-code`
- Workflows: `claude-*.yml`
- Config prefix: `claude_`

### Codex
- Branches: `codex/feature-name`
- PR Labels: `codex`
- Workflows: `codex-*.yml`
- Config prefix: `codex_`

## GitHub Actions

### Claude Workflows
Located in `.github/workflows/claude/`:
- `requirements-review.yml` - Validates requirements documents
- `architecture-review.yml` - Reviews architecture designs
- `implementation-review.yml` - Checks implementation plans
- `code-review.yml` - Performs code quality checks
- `final-review.yml` - Comprehensive final validation

### Codex Workflows
Located in `.github/workflows/codex/`:
- `codex-pipeline.yml` - Main Codex pipeline (template)
- [Additional workflows to be implemented]

## Configuration

### Claude Code Configuration
- Pipeline: `claude_code/pipeline/config/pipeline_config.yml`
- Readiness: `claude_code/pipeline/config/readiness_criteria.yml`

### Codex Configuration
- Pipeline: `codex/pipeline/config/pipeline_config.yml`
- [Additional configs to be added]

## Documentation

- **Claude Code Guide**: `claude_code/docs/PIPELINE_USAGE_GUIDE.md`
- **Claude Setup**: `claude_code/docs/CLAUDE_SETUP_GUIDE.md`
- **Codex Guide**: `codex/README.md`

## Contributing

When contributing, please:
1. Use the appropriate agent directory
2. Follow the naming conventions
3. Update relevant documentation
4. Ensure GitHub Actions pass

## Metrics

Both pipelines track:
- Requirements coverage
- Test coverage
- Code quality scores
- Time per phase
- Review iterations

## Links

- [Claude Code Issues](https://github.com/anthropics/claude-code/issues)
- [Repository](https://github.com/jimmc414/claude_codex_collab)

## License

[License information to be added]

---

This repository demonstrates a systematic approach to software development using multiple agents.