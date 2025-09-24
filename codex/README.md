# Codex Pipeline Orchestrator

This repository provides a lightweight command-line tool for running a disciplined
ChatGPT Pro workflow for software projects. The workflow covers the full lifecycle outlined
below:

1. Requirements discovery loop
2. `requirements.md`
3. `architecture.md`
4. `implementation.md`
5. Implementation & testing iteration
6. Code review loop
7. Release readiness report

The tool never calls OpenAI APIs. Instead it generates vetted prompts and checklists for
collaboration with either **GPT-5 Codex** or **GPT-5 Pro** inside the ChatGPT Pro web
experience. Artifacts are captured locally for traceability.

## Prerequisites

- Python 3.10+ (standard library only)
- A ChatGPT Pro subscription with access to GPT-5 Codex and/or GPT-5 Pro
- Git for version control of your actual project code (not required by the CLI but recommended)

## Quick start

```bash
python -m codex.pipeline_cli init --project "Project Name" --concept "One sentence idea" \
    --model gpt-5-codex --github-auto-sync
python -m codex.pipeline_cli status
python -m codex.pipeline_cli prompt requirements_loop
```

1. Run `init` once per project. Select either `gpt-5-codex` or `gpt-5-pro`.
   Add `--github-auto-sync` to create an auto-pushing workflow for GitHub.
2. Use `prompt <stage>` to print the tailored system prompt, kickoff prompt, instructions, and
   ready checklist for that stage.
3. Operate ChatGPT Pro with those prompts. When a stage produces a document,
   store it locally via `python -m codex.pipeline_cli capture <stage>`.
4. Mark non-document stages complete with `python -m codex.pipeline_cli complete <stage>`.
5. `status` shows progress and any notes captured during the run.

Artifacts are saved in the `codex/artifacts/` directory:

- `codex/artifacts/requirements.md`
- `codex/artifacts/architecture.md`
- `codex/artifacts/implementation.md`
- `codex/artifacts/code_log.md`
- `codex/artifacts/review_log.md`
- `codex/artifacts/ready_report.md`

Use version control to commit these documents alongside your codebase.

### GitHub auto-sync and review feedback

The CLI can push every completed stage to GitHub and keep a pull request updated so that
Actions-driven code review workflows run automatically.

1. Ensure you are inside a git repository with a GitHub remote.
2. Provide a token that can create and update pull requests via the environment variable
   `CODEX_PIPELINE_GITHUB_TOKEN` (or reuse an existing `GITHUB_TOKEN`). The token only needs the
   `repo` scope for private repositories.
3. Either pass the GitHub options during `init` (`--github-auto-sync`, `--github-remote`,
   `--github-branch`, `--github-base`) or configure them later:

   ```bash
   python -m codex.pipeline_cli github configure --auto-sync
   ```

   The command will detect the current branch and remote by default.

4. After each `capture` or `complete`, the CLI commits the updated artifacts and pipeline state,
   pushes to the configured branch, and creates or refreshes a draft pull request. The PR body
   renders the stage checklist so reviewers can track readiness.
5. To see the latest automated review output, run:

   ```bash
   python -m codex.pipeline_cli github feedback --max-reviews 3
   ```

   This prints check-run results, workflow run URLs, and the most recent GitHub review comments so
   the findings can be fed back into subsequent ChatGPT Pro sessions for remediation.

## Stage overview

| Stage key | Output | Purpose |
|-----------|--------|---------|
| `requirements_loop` | — | Requirements interview with ready checklist gating. |
| `requirements_doc` | `codex/artifacts/requirements.md` | Formal requirements using shall/shall not language. |
| `architecture_doc` | `codex/artifacts/architecture.md` | Architectural decisions, rationale, and traceability table. |
| `implementation_doc` | `codex/artifacts/implementation.md` | Developer-facing execution plan and testing strategy. |
| `code_build` | `codex/artifacts/code_log.md` | Summary of implementation slices, tests, and learnings. |
| `review_loop` | `codex/artifacts/review_log.md` | Reviewer verdicts and remediation notes. |
| `ready_gate` | `codex/artifacts/ready_report.md` | Final readiness decision with supporting evidence. |

The CLI enforces stage ordering so discovery happens before requirements, requirements before
architecture, and so on.

## Working with ChatGPT Pro

Each `prompt` command prints two blocks to copy into ChatGPT Pro:

- **System prompt** – paste into the conversation instructions pane.
- **Kickoff prompt** – send as the first message.

Choose the desired model from the model selector. The prompts are written so that both
GPT-5 Codex and GPT-5 Pro follow the expectations for each stage. The CLI personalizes
the copy with the project name and concept.

Because the workflow runs entirely through the ChatGPT interface, models can be switched at
any time by re-running `init --force` or editing `codex/.codex_pipeline/state.json` to change
the `model` field.

## Managing state

- `python -m codex.pipeline_cli status` – check which stages are pending or complete.
- `python -m codex.pipeline_cli capture <stage>` – record generated Markdown directly from the
  chat output. Use `--append` if you want to accumulate multiple sessions in the same file.
- `python -m codex.pipeline_cli complete <stage>` – mark discovery-only stages once the ready
  checklist is satisfied.
- `python -m codex.pipeline_cli reset` – clear the current pipeline state (does not delete
  artifacts).

## Suggested workflow

1. Kick off discovery and do not move forward until the ready checklist is entirely PASS.
2. Generate and commit each Markdown artifact as it is approved.
3. Follow the implementation loop instructions: request small changes, run tests locally, and
   record the outcomes in `code_log.md`.
4. Use the review prompts whenever a pull request is opened. Continue iterating with the model
   until a PASS verdict is received.
5. Finish with the readiness report to confirm requirements coverage and test evidence before
   release.

This approach yields a reproducible, auditable pipeline that mirrors the manual flow while
maintaining compatibility with ChatGPT Pro subscriptions.
