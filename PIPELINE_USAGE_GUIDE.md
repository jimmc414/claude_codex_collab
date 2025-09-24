# Claude Code Development Pipeline - Usage Guide

## Overview

This pipeline provides a systematic approach to software development using Claude Code (Opus 4.1) with integrated GitHub Actions for continuous quality assurance. Each phase builds upon the previous one, with automated reviews and feedback loops at every step.

## Quick Start

### Prerequisites

1. **Claude Code Setup**
   - Ensure you're using Claude Code with Opus 4.1 model
   - Have this repository cloned locally
   - GitHub repository configured with Actions enabled

2. **Initial Setup**
   ```bash
   # Clone the repository
   git clone https://github.com/yourusername/claude_codex_collab.git
   cd claude_codex_collab

   # Ensure GitHub Actions are enabled
   gh repo set-default
   ```

## Pipeline Phases

### Phase 1: Requirements Gathering

**Start the conversation with Claude:**
```
User: "I want to build a task management application"
Claude: "I'll help you define comprehensive requirements for your project. Let me read the requirements gathering template and begin our discussion."
```

Claude will:
1. Read `claude_pipeline/prompts/requirements_gathering.md`
2. Ask structured questions about your project
3. Generate `docs/requirements.md` with RFC 2119 language
4. Commit and push to a feature branch
5. GitHub Action validates requirements automatically

**What happens behind the scenes:**
- `requirements-review.yml` runs validation checks
- Feedback posted as PR comments
- Claude reads feedback and iterates if needed

### Phase 2: Architecture Design

**Continue with:**
```
User: "Now let's design the architecture"
Claude: "I'll read the requirements and create a comprehensive architecture design."
```

Claude will:
1. Read `docs/requirements.md`
2. Propose architecture patterns
3. Create detailed `docs/architecture.md` with diagrams
4. Push changes triggering architecture review
5. Iterate based on GitHub Actions feedback

**Architecture includes:**
- System overview with Mermaid diagrams
- Component design
- Data models
- API specifications
- Security architecture
- Deployment strategy

### Phase 3: Implementation Planning

**Proceed with:**
```
User: "Create the implementation plan"
Claude: "I'll create a detailed implementation plan based on the architecture."
```

Claude will:
1. Analyze architecture components
2. Create step-by-step `docs/implementation.md`
3. Include code examples and instructions
4. Define task breakdown and dependencies
5. Push for automated review

**Implementation plan contains:**
- Setup instructions
- Phased implementation approach
- Code snippets for each component
- Testing strategies
- Troubleshooting guide

### Phase 4: Code Implementation

**Begin coding:**
```
User: "Start implementing the code"
Claude: "I'll begin implementing based on our plan. I'll use the TodoWrite tool to track progress."
```

Claude will:
1. Create project structure
2. Implement components in logical order
3. Write tests alongside code
4. Commit incrementally
5. Push changes triggering code review

**Code review checks:**
- Linting (ESLint, Pylint)
- Type checking
- Security scanning
- Test coverage
- Performance metrics

### Phase 5: Final Review

**Complete the pipeline:**
```
User: "Run the final review"
Claude: "I'll perform a comprehensive review to ensure everything meets our requirements."
```

Claude will:
1. Generate traceability matrix
2. Verify all requirements are met
3. Calculate quality score
4. Create final review report
5. Auto-approve PR if quality threshold met

## Working with Claude Code

### Starting a New Project

```markdown
User: "Start new project: [project name]"
Claude: *Creates feature branch*
        *Reads requirements gathering prompt*
        "I'll help you define comprehensive requirements for [project name].
         Let's begin with understanding what you're building."
```

### Monitoring Progress

```markdown
User: "Show pipeline status"
Claude: *Checks GitHub Actions status*
        *Reviews PR comments*
        "Current status:
         ✅ Requirements: Passed
         ✅ Architecture: Passed
         🔄 Implementation: In Progress
         ⏸️ Code Review: Pending
         ⏸️ Final Review: Pending"
```

### Handling Feedback

When GitHub Actions post feedback:

```markdown
Claude: "The requirements review found issues:
         - Missing acceptance criteria for FR-3
         - NFR-2 lacks measurable metrics

         I'll fix these issues now..."
*Updates requirements.md*
*Pushes changes*
"Fixed and pushed. Waiting for re-review..."
```

## GitHub Actions Integration

### Understanding the Workflow

1. **Push triggers Action** →
2. **Action runs validation** →
3. **Results posted to PR** →
4. **Claude reads feedback** →
5. **Claude fixes issues** →
6. **Repeat until passing**

### Manual Trigger

You can manually trigger reviews:

```bash
# Trigger specific workflow
gh workflow run requirements-review.yml

# View workflow status
gh workflow view

# Check PR comments
gh pr view --comments
```

## Configuration

### Customizing Thresholds

Edit `claude_pipeline/config/readiness_criteria.yml`:

```yaml
code_review:
  test_coverage:
    minimum: 85  # Increase from 80
  security:
    max_high_risk: 0  # No high-risk issues allowed
```

### Adding Custom Validators

Create new validation script in `.github/review-scripts/`:

```python
#!/usr/bin/env python3
# custom_validator.py
import sys
import json

def validate(filepath):
    # Your validation logic
    return {"passed": True, "issues": []}

if __name__ == "__main__":
    result = validate(sys.argv[1])
    with open("custom_review.json", "w") as f:
        json.dump(result, f)
```

## Best Practices

### 1. Incremental Development
- Complete each phase before moving to next
- Don't skip validation steps
- Address feedback immediately

### 2. Clear Requirements
- Be specific in requirements gathering
- Use measurable criteria
- Include edge cases

### 3. Documentation
- Keep all generated docs updated
- Document decisions in architecture
- Maintain traceability

### 4. Testing
- Write tests during implementation
- Aim for >80% coverage
- Include edge cases

### 5. Review Iterations
- Don't ignore warnings
- Fix issues before proceeding
- Use feedback to improve

## Common Commands

### Working with Claude

```markdown
# Start new project
"Let's build a [type] application"

# Check status
"What's the current pipeline status?"

# Review specific phase
"Show me the requirements review results"

# Fix issues
"Fix the issues found in code review"

# Generate report
"Create a summary of the entire pipeline"
```

### Git Commands Claude Uses

```bash
# Create feature branch
git checkout -b feature/project-name

# Incremental commits
git add docs/requirements.md
git commit -m "Requirements: Initial draft"
git push -u origin feature/project-name

# Create PR
gh pr create --title "Feature: Project Name" --body "..."

# Check PR status
gh pr view --comments
```

## Troubleshooting

### Issue: GitHub Action Failing

```markdown
User: "The architecture review is failing"
Claude: *Checks action logs*
        "I see the issue - missing diagram in section 3.
         Let me add that now..."
```

### Issue: Low Test Coverage

```markdown
User: "Test coverage is only 65%"
Claude: *Analyzes coverage report*
        "I'll add tests for uncovered functions:
         - UserService.delete()
         - AuthMiddleware.validate()
         Let me implement these tests..."
```

### Issue: Requirements Not Clear

```markdown
Claude: "The requirement 'system should be fast' is too vague.
         Let's make it measurable:
         'System SHALL respond to API requests within 200ms
         for 95% of requests under normal load'"
```

## Advanced Features

### Parallel Phase Execution

For independent components:

```markdown
User: "Implement the frontend and backend in parallel"
Claude: "I'll create separate implementation plans and work on both:
         - Backend API (Node.js/Express)
         - Frontend UI (React)
         Using parallel GitHub Actions for review..."
```

### Custom Project Types

```markdown
User: "This is a Chrome extension project"
Claude: "I'll adapt the pipeline for Chrome extension requirements:
         - Manifest.json configuration
         - Content script architecture
         - Background service workers
         - Chrome API integration"
```

### Multi-Repository Projects

```markdown
User: "This project spans multiple repositories"
Claude: "I'll coordinate across repositories:
         - Main application repo
         - Shared libraries repo
         - Infrastructure repo
         Each with its own pipeline instance..."
```

## Example Complete Session

```markdown
User: "Let's build a URL shortener service"

Claude: "I'll help you build a URL shortener using our development pipeline.
         Starting with requirements gathering...

         What's the expected daily traffic volume?"

User: "About 10,000 URLs per day"

Claude: "Who are the target users?"

User: "Public users and registered users with analytics"

[... continues through all phases ...]

Claude: "Pipeline complete!
         ✅ Requirements documented
         ✅ Architecture designed
         ✅ Implementation planned
         ✅ Code implemented
         ✅ All tests passing (92% coverage)
         ✅ Quality score: 94/100

         PR #47 has been auto-approved and is ready to merge."
```

## Metrics and Reporting

The pipeline tracks:
- Time spent per phase
- Number of review iterations
- Test coverage trends
- Quality score progression
- Requirements completion rate

Access metrics:
```markdown
User: "Show pipeline metrics"
Claude: *Reads docs/pipeline_metrics.json*
        "Pipeline Performance:
         - Average time to completion: 2.5 days
         - First-time pass rate: 78%
         - Average quality score: 87/100"
```

## Getting Help

1. **Documentation Issues**
   ```markdown
   User: "Explain how the architecture review works"
   Claude: *Explains the architecture review process*
   ```

2. **Pipeline Issues**
   - Check GitHub Actions logs
   - Review PR comments
   - Examine validation scripts

3. **Report Issues**
   - https://github.com/anthropics/claude-code/issues

## Conclusion

This pipeline ensures high-quality software development through systematic phases, automated reviews, and continuous feedback. Each phase builds on the previous one, creating a traceable path from requirements to deployment.

Remember: The pipeline is a guide, not a rigid framework. Adapt it to your specific needs while maintaining the core principles of quality and traceability.