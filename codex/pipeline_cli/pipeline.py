"""Command-line interface for orchestrating the Codex pipeline."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path
from textwrap import indent
from typing import Optional

from .github import AutoSyncResult, GitIntegrationError, auto_sync_stage, fetch_feedback, prepare_github_settings
from .stages import ARTIFACT_STAGES, STAGE_ORDER, get_stage, model_label
from .state import PipelineState, StateManager

_STATUS_ICONS = {
    "pending": "⏳",
    "in_progress": "🔄",
    "complete": "✅",
}


def _print_header(text: str) -> None:
    print(f"\n=== {text} ===")


def _prompt_for_value(prompt: str, default: Optional[str] = None) -> str:
    if default:
        prompt = f"{prompt} [{default}]: "
    else:
        prompt = f"{prompt}: "
    value = input(prompt).strip()
    if not value:
        if default is not None:
            return default
        print("A value is required.")
        return _prompt_for_value(prompt.rstrip(": "), default)
    return value


def command_init(args: argparse.Namespace, manager: StateManager) -> None:
    if manager.exists() and not args.force:
        print("Pipeline already initialized. Use --force to overwrite.")
        sys.exit(1)

    project_name = args.project or _prompt_for_value("Project name")
    concept = args.concept or _prompt_for_value("Initial concept or problem statement")
    model = args.model

    github_settings = None
    if args.github_auto_sync or args.github_remote or args.github_branch or args.github_base:
        try:
            github_settings = prepare_github_settings(
                manager.root,
                remote=args.github_remote,
                branch=args.github_branch,
                base=args.github_base,
                auto_sync=args.github_auto_sync,
            )
        except GitIntegrationError as exc:
            print(f"Failed to configure GitHub integration: {exc}")
            sys.exit(1)

    stage_status = {stage: "pending" for stage in STAGE_ORDER}
    state = PipelineState(
        project_name=project_name,
        concept=concept,
        model=model,
        stage_status=stage_status,
        github=github_settings,
    )
    manager.save(state)
    print(f"Initialized pipeline for '{project_name}' using model {model_label(model)}.")
    if github_settings:
        if github_settings.auto_sync:
            print(
                f"GitHub auto-sync enabled for {github_settings.remote}/{github_settings.branch}"
                f" -> {github_settings.base}."
            )
        else:
            print(
                "GitHub repository metadata captured. Use 'python -m codex.pipeline_cli github configure --auto-sync'"
                " when you are ready to push after each stage."
            )


def command_status(manager: StateManager) -> None:
    manager.ensure_initialized()
    state = manager.load()
    print(f"Project: {state.project_name}")
    print(f"Model:   {model_label(state.model)}")
    print(f"Concept: {state.concept}")

    if state.github:
        _print_header("GitHub Sync")
        repo_label = state.github.repository or "(unknown repository)"
        print(f"Remote: {state.github.remote} -> {repo_label}")
        print(f"Branch: {state.github.branch} (base {state.github.base})")
        print(f"Auto-sync: {'enabled' if state.github.auto_sync else 'disabled'}")
        if state.github.pr_number:
            print(f"Pull request: #{state.github.pr_number}")

    _print_header("Stage Progress")
    for stage_key, status in state.list_statuses():
        stage = get_stage(stage_key)
        icon = _STATUS_ICONS.get(status, status)
        print(f"{icon} {stage.title} ({stage_key}) -> {status}")
        note = state.stage_notes.get(stage_key)
        if note:
            print(indent(f"Note: {note}", "    "))


def command_prompt(args: argparse.Namespace, manager: StateManager) -> None:
    manager.ensure_initialized()
    state = manager.load()
    stage = get_stage(args.stage)
    label = model_label(state.model)

    description = stage.description.format(
        model_label=label, project_name=state.project_name, concept=state.concept
    )
    instructions = stage.instructions.format(
        model_label=label, project_name=state.project_name, concept=state.concept
    )

    _print_header(stage.title)
    print(description)

    _print_header("Instructions")
    print(instructions)

    if stage.ready_checklist:
        _print_header("Ready Checklist")
        for item in stage.ready_checklist:
            print(f"- {item}")

    system_prompt = stage.format_system_prompt(
        project_name=state.project_name, model_label=label, concept=state.concept
    )
    if system_prompt:
        _print_header("System Prompt")
        print(system_prompt)

    kickoff_prompt = stage.format_kickoff_prompt(
        project_name=state.project_name, model_label=label, concept=state.concept
    )
    if kickoff_prompt:
        _print_header("Kickoff Prompt")
        print(kickoff_prompt)


def _read_capture_content(file_path: Optional[Path]) -> str:
    if file_path:
        return file_path.read_text()

    print("Paste the artifact content. End input with a line containing only 'EOF'.")
    lines = []
    while True:
        try:
            line = input()
        except EOFError:
            break
        if line.strip() == "EOF":
            break
        lines.append(line)
    content = "\n".join(lines).rstrip()
    if not content:
        raise RuntimeError("No content captured. Aborting.")
    return content + "\n"


def _handle_auto_sync_result(
    *,
    stage,
    state: PipelineState,
    manager: StateManager,
    result: AutoSyncResult,
) -> None:
    """Print auto-sync messages and persist any updated GitHub metadata."""

    note_updated = False
    for message in result.messages:
        print(message)
    if result.commit_sha:
        existing_note = state.stage_notes.get(stage.key, "")
        sync_note = f"GitHub sync commit {result.commit_sha[:7]}"
        if result.pr_number:
            sync_note += f" (PR #{result.pr_number})"
        if sync_note not in existing_note:
            state.stage_notes[stage.key] = (
                f"{existing_note}; {sync_note}" if existing_note else sync_note
            )
            note_updated = True
    if result.updated_state or note_updated:
        manager.save(state)


def command_capture(args: argparse.Namespace, manager: StateManager) -> None:
    manager.ensure_initialized()
    state = manager.load()
    stage = get_stage(args.stage)
    if not stage.artifact_path:
        print(f"Stage '{stage.key}' does not produce an artifact. Use the 'complete' command instead.")
        sys.exit(1)

    state.ensure_order(stage.key)

    artifact_path = manager.root / stage.artifact_path
    artifact_path.parent.mkdir(parents=True, exist_ok=True)

    repo_root = manager.root.parent
    try:
        display_path = artifact_path.relative_to(repo_root)
    except ValueError:
        display_path = artifact_path.relative_to(manager.root)

    content = _read_capture_content(args.file)
    mode = "a" if args.append else "w"
    with artifact_path.open(mode, encoding="utf-8") as f:
        f.write(content)
        if args.append and not content.endswith("\n"):
            f.write("\n")

    state.mark_complete(stage.key)
    state.stage_notes[stage.key] = f"Artifact saved to {display_path}"
    manager.save(state)
    print(f"Saved artifact to {display_path} and marked stage complete.")

    result = auto_sync_stage(
        root=manager.root,
        state=state,
        settings=state.github,
        stage_key=stage.key,
        stage_title=stage.title,
        artifact_path=stage.artifact_path,
        state_path=manager.state_path,
    )
    _handle_auto_sync_result(stage=stage, state=state, manager=manager, result=result)


def command_complete(args: argparse.Namespace, manager: StateManager) -> None:
    manager.ensure_initialized()
    state = manager.load()
    stage = get_stage(args.stage)
    if stage.artifact_path and not (manager.root / stage.artifact_path).exists():
        print(
            "Cannot complete this stage because its artifact is missing. Use the capture command first."
        )
        sys.exit(1)
    state.mark_complete(stage.key)
    if args.note:
        state.stage_notes[stage.key] = args.note
    manager.save(state)
    print(f"Stage '{stage.title}' marked as complete.")

    result = auto_sync_stage(
        root=manager.root,
        state=state,
        settings=state.github,
        stage_key=stage.key,
        stage_title=stage.title,
        artifact_path=stage.artifact_path,
        state_path=manager.state_path,
    )
    _handle_auto_sync_result(stage=stage, state=state, manager=manager, result=result)


def command_reset(manager: StateManager) -> None:
    manager.ensure_initialized()
    manager.state_path.unlink()
    print("Pipeline state cleared. Re-run init to start again.")


def command_github_configure(args: argparse.Namespace, manager: StateManager) -> None:
    manager.ensure_initialized()
    state = manager.load()

    current = state.github
    desired_remote = args.remote or (current.remote if current else None)
    desired_branch = args.branch or (current.branch if current else None)
    desired_base = args.base or (current.base if current else None)
    if args.auto_sync is None:
        desired_auto = current.auto_sync if current else False
    else:
        desired_auto = args.auto_sync

    try:
        new_settings = prepare_github_settings(
            manager.root,
            remote=desired_remote,
            branch=desired_branch,
            base=desired_base,
            auto_sync=desired_auto,
        )
    except GitIntegrationError as exc:
        print(f"GitHub configuration failed: {exc}")
        sys.exit(1)

    if current and current.pr_number and not new_settings.pr_number:
        new_settings.pr_number = current.pr_number
    if current and current.repository and not new_settings.repository:
        new_settings.repository = current.repository

    state.github = new_settings
    manager.save(state)

    status = "enabled" if new_settings.auto_sync else "disabled"
    print(
        f"GitHub sync configured for {new_settings.remote}/{new_settings.branch} -> {new_settings.base}"
        f" ({status})."
    )
    if new_settings.auto_sync:
        print("Future stage completions will commit, push, and update the tracked pull request automatically.")
    else:
        print("Automatic syncing is disabled. Re-run with --auto-sync to enable push-and-review automation.")


def command_github_feedback(args: argparse.Namespace, manager: StateManager) -> None:
    manager.ensure_initialized()
    state = manager.load()
    if not state.github:
        print(
            "GitHub integration is not configured. Run 'python -m codex.pipeline_cli github configure --auto-sync'"
            " after setting up your git repository."
        )
        sys.exit(1)

    try:
        data = fetch_feedback(
            root=manager.root,
            settings=state.github,
            commit_sha=args.commit,
            max_reviews=args.max_reviews,
        )
    except GitIntegrationError as exc:
        print(f"Unable to fetch GitHub feedback: {exc}")
        sys.exit(1)

    if data.get("repository_updated"):
        manager.save(state)

    _print_header("Commit")
    print(f"Inspecting commit: {data['commit']}")

    _print_header("Check Runs")
    check_runs = data.get("check_runs", [])
    if not check_runs:
        print("No check runs reported yet.")
    else:
        for check in check_runs:
            name = check.get("name", "<unknown>")
            conclusion = check.get("conclusion") or check.get("status")
            completed = check.get("completed_at") or check.get("started_at") or ""
            details_url = check.get("details_url") or ""
            line = f"- {name}: {conclusion}"
            if completed:
                line += f" (updated {completed})"
            print(line)
            if details_url:
                print(indent(details_url, "  "))

    _print_header("Workflow Runs")
    runs = data.get("workflow_runs", [])
    if not runs:
        print("No workflow runs found for the tracked branch.")
    else:
        for run in runs:
            name = run.get("name") or "Workflow"
            status = run.get("status")
            conclusion = run.get("conclusion")
            number = run.get("run_number")
            html_url = run.get("html_url")
            summary = f"- {name} #{number}: {status}"
            if conclusion:
                summary += f" → {conclusion}"
            print(summary)
            if html_url:
                print(indent(html_url, "  "))

    _print_header("Recent Reviews")
    reviews = data.get("reviews", [])
    if not reviews:
        print("No pull request reviews have been submitted yet.")
    else:
        for review in reviews:
            user = review.get("user", {}).get("login", "unknown")
            state_label = review.get("state")
            submitted = review.get("submitted_at") or review.get("dismissed_at") or ""
            print(f"- {user}: {state_label} at {submitted}")
            body = review.get("body")
            if body:
                print(indent(body.strip(), "  "))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Codex pipeline orchestration CLI")
    subparsers = parser.add_subparsers(dest="command")

    # init
    init_parser = subparsers.add_parser("init", help="Initialize the pipeline state")
    init_parser.add_argument("--project", help="Project name")
    init_parser.add_argument("--concept", help="Initial concept or problem statement")
    init_parser.add_argument(
        "--model",
        choices=["gpt-5-codex", "gpt-5-pro"],
        default="gpt-5-codex",
        help="Preferred ChatGPT Pro model",
    )
    init_parser.add_argument("--github-remote", help="Git remote to push pipeline updates to")
    init_parser.add_argument("--github-branch", help="Branch to push when syncing with GitHub")
    init_parser.add_argument(
        "--github-base",
        help="Target base branch for the pull request (default: main)",
    )
    init_parser.add_argument(
        "--github-auto-sync",
        action="store_true",
        help="Automatically commit and push after each stage to trigger GitHub workflows",
    )
    init_parser.add_argument("--force", action="store_true", help="Overwrite existing state")

    # status
    subparsers.add_parser("status", help="Show current pipeline status")

    # prompt
    prompt_parser = subparsers.add_parser("prompt", help="Display prompts for a stage")
    prompt_parser.add_argument("stage", choices=STAGE_ORDER, help="Stage key to display")

    # capture
    capture_parser = subparsers.add_parser("capture", help="Store an artifact for a stage")
    capture_parser.add_argument("stage", choices=[s for s in STAGE_ORDER if s in ARTIFACT_STAGES])
    capture_parser.add_argument("--file", type=Path, help="Read content from a file instead of stdin")
    capture_parser.add_argument("--append", action="store_true", help="Append instead of overwrite")

    # complete
    complete_parser = subparsers.add_parser("complete", help="Mark a stage as complete")
    complete_parser.add_argument("stage", choices=STAGE_ORDER)
    complete_parser.add_argument("--note", help="Optional note to attach to the stage")

    # reset
    subparsers.add_parser("reset", help="Delete existing pipeline state")

    # GitHub helpers
    github_parser = subparsers.add_parser("github", help="GitHub integration utilities")
    github_sub = github_parser.add_subparsers(dest="github_command")
    github_sub.required = True

    github_config = github_sub.add_parser("configure", help="Configure GitHub sync settings")
    github_config.add_argument("--remote", help="Git remote to push to")
    github_config.add_argument("--branch", help="Branch name to push")
    github_config.add_argument("--base", help="Target base branch for pull requests")
    auto_group = github_config.add_mutually_exclusive_group()
    auto_group.add_argument(
        "--auto-sync",
        dest="auto_sync",
        action="store_const",
        const=True,
        help="Enable automatic commit and push after each stage",
    )
    auto_group.add_argument(
        "--no-auto-sync",
        dest="auto_sync",
        action="store_const",
        const=False,
        help="Disable automatic commit and push",
    )
    github_config.set_defaults(auto_sync=None)

    github_feedback = github_sub.add_parser(
        "feedback", help="Fetch GitHub review and workflow status for the tracked pull request"
    )
    github_feedback.add_argument("--commit", help="Commit SHA to inspect (defaults to HEAD)")
    github_feedback.add_argument(
        "--max-reviews",
        type=int,
        default=5,
        help="Maximum number of recent reviews to display",
    )

    return parser


def main(argv: Optional[list[str]] = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)

    if not args.command:
        parser.print_help()
        return

    manager = StateManager()

    if args.command == "init":
        command_init(args, manager)
    elif args.command == "status":
        command_status(manager)
    elif args.command == "prompt":
        command_prompt(args, manager)
    elif args.command == "capture":
        command_capture(args, manager)
    elif args.command == "complete":
        command_complete(args, manager)
    elif args.command == "reset":
        command_reset(manager)
    elif args.command == "github":
        if args.github_command == "configure":
            command_github_configure(args, manager)
        elif args.github_command == "feedback":
            command_github_feedback(args, manager)
        else:  # pragma: no cover - defensive
            parser.print_help()
    else:  # pragma: no cover - defensive
        parser.print_help()


if __name__ == "__main__":  # pragma: no cover
    main()
