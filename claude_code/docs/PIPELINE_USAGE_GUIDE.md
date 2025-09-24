# Claude Code Development Pipeline - Usage Guide

## Overview

This guide explains how to run the Claude Code development pipeline with GitHub Actions integration. The workflow is divided into sequential phases that build on one another, with automated checks at every step to maintain quality.

## Quick Start

### Prerequisites

1. Install Claude Code (Opus 4.1) version 1.0.120 or later
2. Clone this repository locally
3. Authenticate the GitHub CLI and ensure Actions are enabled for the target repository

### Initial Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/claude_codex_collab.git
cd claude_codex_collab

# Set the default GitHub repository for CLI commands
gh repo set-default
```

## Pipeline Phases

### Phase 1: Requirements Gathering

- Review `claude_code/pipeline/prompts/requirements_gathering.md` to understand the information expected
- Collect project overview, stakeholders, functional scope, non-functional criteria, and constraints
- Capture the results in `docs/requirements.md` using RFC 2119 terminology and measurable acceptance criteria
- GitHub Actions runs `requirements-review.yml` to validate structure and completeness

### Phase 2: Architecture Design

- Study the approved requirements document
- Design system components, interfaces, data flows, security measures, and infrastructure considerations
- Document the architecture in `docs/architecture.md`, including diagrams where appropriate
- Push updates to trigger the `architecture-review.yml` workflow for automated checks

### Phase 3: Implementation Planning

- Translate the architecture into a practical plan covering prerequisites, task breakdown, code structure, and testing strategy
- Record the plan in `docs/implementation.md` with detailed step-by-step guidance
- Use `implementation-review.yml` to confirm coverage of critical tasks and traceability

### Phase 4: Code Implementation

- Build the project according to the implementation plan, committing logical increments to version control
- Maintain alignment between code changes and documented requirements
- Run local linters, tests, and security scans as you progress; GitHub Actions (`code-review.yml`) enforces quality gates

### Phase 5: Final Review

- Assemble traceability evidence linking requirements, architecture decisions, implementation tasks, and code artifacts
- Verify that coverage, security, and performance thresholds are met
- Use `final-review.yml` to confirm the pipeline is complete and ready for merge

## Operating the Pipeline

### Starting New Work

1. Create a feature branch following the naming convention `claude/<feature-name>`
2. Work through the phases in order, committing artifacts for each milestone
3. Open a pull request once all required documents and code updates are ready

### Monitoring Progress

- View GitHub Actions status in the repository UI or via the CLI:
  ```bash
  gh workflow list
  gh run list
  gh run view <run-id>
  ```
- Inspect pull request comments for automated feedback and checklist items

### Handling Feedback

1. Review workflow logs to identify failing checks
2. Update the relevant documentation or code files
3. Commit and push changes to rerun the corresponding workflow
4. Repeat until all checks succeed

## GitHub Actions Integration

### Automated Execution Flow

1. Push changes to a branch
2. The corresponding workflow runs validation scripts
3. Results appear in the pull request conversation and workflow logs
4. Address findings and push updates until the workflow reports success

### Manual Triggers

Use the GitHub CLI to run specific workflows when needed:

```bash
# Trigger a workflow manually
gh workflow run requirements-review.yml

# View workflow status
gh workflow view requirements-review.yml

# Review pull request comments
gh pr view --comments
```

## Configuration

### Customizing Thresholds

Modify `claude_code/pipeline/config/readiness_criteria.yml` to adjust acceptance levels:

```yaml
code_review:
  test_coverage:
    minimum: 85  # Increase from default of 80
  security:
    max_high_risk: 0  # Block merges if any high-risk issues are detected
```

### Adding Custom Validators

Add scripts under `.github/review-scripts/` to extend validation:

```python
#!/usr/bin/env python3
# custom_validator.py
import sys
import json


def validate(filepath):
    # Implement custom validation logic
    return {"passed": True, "issues": []}


if __name__ == "__main__":
    result = validate(sys.argv[1])
    with open("custom_review.json", "w", encoding="utf-8") as file:
        json.dump(result, file)
```

## Best Practices

1. Complete each phase before advancing to the next to maintain traceability
2. Use measurable language in requirements and plans
3. Keep documentation synchronized with implementation
4. Write tests alongside new code to maintain coverage targets
5. Treat warnings in workflow logs as actionable items, not optional suggestions

## Common Commands

- Start a new project: `git checkout -b claude/<feature-name>`
- Check pipeline status: `gh run list`
- Review workflow results: `gh run view <run-id>`
- Address review items: edit the relevant files, commit, and push updates
- Generate a pipeline summary: compile notes from workflow outputs and documentation updates

## Troubleshooting

### Architecture Review Fails
- Confirm that `docs/architecture.md` includes required diagrams and component descriptions
- Verify that all requirements are mapped to architectural elements

### Low Test Coverage
- Inspect coverage reports produced by the testing framework
- Add unit or integration tests targeting untested functions and edge cases

### Ambiguous Requirements
- Revisit stakeholder input and clarify acceptance criteria
- Update `docs/requirements.md` with measurable targets and edge case coverage

## Advanced Usage

- **Parallel Phase Execution**: For independent subsystems, maintain separate implementation plans and coordinate workflows for each component
- **Custom Project Types**: Adapt templates for specialized domains (for example, browser extensions) by extending the relevant documentation sections
- **Multi-Repository Initiatives**: Align multiple repositories by replicating the pipeline configuration and synchronizing milestones across teams

## Metrics and Reporting

The pipeline tracks:
- Time spent per phase
- Review iteration counts
- Test coverage trends
- Quality score progression
- Requirements completion percentage

To review metrics stored in JSON outputs:

```bash
gh run download <run-id> --pattern "*metrics.json"
```

## Getting Help

1. Review the documentation in `claude_code/docs/`
2. Check GitHub Actions logs for validation details
3. Examine review scripts under `.github/` when diagnosing workflow behavior
4. Report issues at https://github.com/anthropics/claude-code/issues

## Conclusion

Following this pipeline provides a consistent approach from requirements gathering through final review. Maintain updated documentation, respond promptly to workflow feedback, and iterate until every phase meets the configured acceptance criteria.
