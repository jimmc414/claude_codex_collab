"""Git and GitHub integration helpers for the Codex pipeline."""
from __future__ import annotations

import json
import os
import subprocess
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable, List, Optional, Sequence
from urllib import error, request

from .state import GitHubSettings, PipelineState
from .stages import STAGE_ORDER


class GitIntegrationError(RuntimeError):
    """Raised when git or GitHub operations cannot be completed."""


@dataclass
class AutoSyncResult:
    """Represents the outcome of a GitHub auto-sync attempt."""

    commit_sha: Optional[str] = None
    pr_number: Optional[int] = None
    updated_state: bool = False
    messages: List[str] = field(default_factory=list)


def _run_git(args: Sequence[str], *, root: Path, check: bool = True) -> subprocess.CompletedProcess[str]:
    process = subprocess.run(
        ["git", *args],
        cwd=root,
        text=True,
        capture_output=True,
        check=False,
    )
    if check and process.returncode != 0:
        raise GitIntegrationError(process.stderr.strip() or "Git command failed")
    return process


def _ensure_git_repo(root: Path) -> None:
    result = _run_git(["rev-parse", "--is-inside-work-tree"], root=root, check=False)
    if result.returncode != 0 or result.stdout.strip() != "true":
        raise GitIntegrationError("Not inside a git repository. Initialize git before enabling GitHub sync.")


def _current_branch(root: Path) -> str:
    branch = _run_git(["rev-parse", "--abbrev-ref", "HEAD"], root=root).stdout.strip()
    if branch == "HEAD":
        raise GitIntegrationError("Cannot determine branch in detached HEAD state.")
    return branch


def _default_remote(root: Path) -> str:
    remotes = _run_git(["remote"], root=root).stdout.strip().splitlines()
    if not remotes:
        raise GitIntegrationError("No git remotes configured. Add a GitHub remote first.")
    return remotes[0].strip()


def _remote_url(root: Path, remote: str) -> str:
    return _run_git(["remote", "get-url", remote], root=root).stdout.strip()


def _parse_repository_slug(url: str) -> str:
    cleaned = url.strip()
    if cleaned.endswith(".git"):
        cleaned = cleaned[:-4]
    if cleaned.startswith("git@github.com:"):
        slug = cleaned.split(":", 1)[1]
    elif cleaned.startswith("https://github.com/"):
        slug = cleaned.split("github.com/", 1)[1]
    elif cleaned.startswith("ssh://git@github.com/"):
        slug = cleaned.split("github.com/", 1)[1]
    else:
        raise GitIntegrationError("Remote does not point to GitHub. Provide a GitHub remote for auto-sync.")
    if slug.count("/") < 1:
        raise GitIntegrationError("Unable to parse GitHub repository owner/name from remote URL.")
    return slug


def prepare_github_settings(
    root: Path,
    *,
    remote: Optional[str],
    branch: Optional[str],
    base: Optional[str],
    auto_sync: bool,
) -> GitHubSettings:
    """Resolve git metadata and create a GitHubSettings instance."""

    _ensure_git_repo(root)
    resolved_remote = remote or _default_remote(root)
    remotes = _run_git(["remote"], root=root).stdout.splitlines()
    if resolved_remote not in remotes:
        raise GitIntegrationError(f"Remote '{resolved_remote}' not found. Available remotes: {', '.join(remotes)}")

    resolved_branch = branch or _current_branch(root)
    resolved_base = base or "main"
    repository = _parse_repository_slug(_remote_url(root, resolved_remote))
    return GitHubSettings(
        remote=resolved_remote,
        branch=resolved_branch,
        base=resolved_base,
        auto_sync=auto_sync,
        repository=repository,
    )


def _require_clean_index(root: Path) -> None:
    staged = _run_git(["diff", "--cached", "--name-only"], root=root).stdout.strip()
    if staged:
        raise GitIntegrationError(
            "Cannot auto-sync while other files are staged. Commit or unstage them before proceeding."
        )


def _relative_paths(root: Path, paths: Iterable[Path]) -> List[Path]:
    rel_paths: List[Path] = []
    for path in paths:
        if not path:
            continue
        try:
            rel_paths.append(path.resolve().relative_to(root.resolve()))
        except ValueError:
            raise GitIntegrationError(f"Path '{path}' is outside the repository root and cannot be staged.")
    return rel_paths


def _unstage(root: Path, rel_paths: Sequence[Path]) -> None:
    if not rel_paths:
        return
    _run_git(["reset", "HEAD", *[str(p) for p in rel_paths]], root=root)


def _commit_and_push(
    *,
    root: Path,
    settings: GitHubSettings,
    stage_key: str,
    stage_title: str,
    tracked_paths: Sequence[Path],
) -> Optional[str]:
    _require_clean_index(root)

    rel_paths = _relative_paths(root, tracked_paths)
    for rel_path in rel_paths:
        _run_git(["add", str(rel_path)], root=root)

    diff_check = _run_git(["diff", "--cached", "--quiet"], root=root, check=False)
    if diff_check.returncode == 0:
        _unstage(root, rel_paths)
        return None

    commit_message = f"codex({stage_key}): sync {stage_title}"
    _run_git(["commit", "-m", commit_message], root=root)
    commit_sha = _run_git(["rev-parse", "HEAD"], root=root).stdout.strip()
    _run_git(["push", settings.remote, settings.branch], root=root)
    return commit_sha


def _github_token() -> Optional[str]:
    for env_var in ("CODEX_PIPELINE_GITHUB_TOKEN", "GITHUB_TOKEN"):
        token = os.environ.get(env_var)
        if token:
            return token
    return None


def _github_request(
    *,
    token: str,
    method: str,
    url: str,
    data: Optional[dict] = None,
) -> object:
    payload = None
    if data is not None:
        payload = json.dumps(data).encode("utf-8")
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "User-Agent": "codex-pipeline-cli",
    }
    req = request.Request(url, data=payload, headers=headers, method=method)
    try:
        with request.urlopen(req) as resp:
            text = resp.read().decode("utf-8")
    except error.HTTPError as exc:  # pragma: no cover - network error handling
        detail = exc.read().decode("utf-8") if exc.fp else exc.reason
        raise GitIntegrationError(f"GitHub API request failed: {exc.code} {detail}") from exc
    return json.loads(text) if text else None


def _render_pr_body(state: PipelineState) -> str:
    lines = [
        f"# Codex Pipeline Progress — {state.project_name}",
        "",
        "| Stage | Status | Notes |",
        "|-------|--------|-------|",
    ]
    for stage in STAGE_ORDER:
        status = state.get_status(stage)
        note = state.stage_notes.get(stage, "")
        safe_note = note.replace("|", "\\|") if note else ""
        lines.append(f"| `{stage}` | {status} | {safe_note} |")
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    lines.extend(["", f"_Last updated: {timestamp}_"])
    return "\n".join(lines)


def _ensure_repository(settings: GitHubSettings, root: Path) -> tuple[str, bool]:
    if settings.repository:
        return settings.repository, False
    repository = _parse_repository_slug(_remote_url(root, settings.remote))
    settings.repository = repository
    return repository, True


def _ensure_pull_request(
    *,
    root: Path,
    settings: GitHubSettings,
    state: PipelineState,
    messages: List[str],
) -> tuple[Optional[int], bool]:
    token = _github_token()
    if not token:
        messages.append(
            "Skipped PR management because no GitHub token is configured. Set CODEX_PIPELINE_GITHUB_TOKEN"
            " or GITHUB_TOKEN to enable automatic pull request updates."
        )
        return settings.pr_number, False

    repository, repo_updated = _ensure_repository(settings, root)
    owner, repo_name = repository.split("/", 1)
    api_base = f"https://api.github.com/repos/{owner}/{repo_name}"

    body = _render_pr_body(state)
    state_changed = repo_updated

    if settings.pr_number:
        _github_request(
            token=token,
            method="PATCH",
            url=f"{api_base}/pulls/{settings.pr_number}",
            data={"body": body},
        )
        messages.append(f"Updated pull request #{settings.pr_number} with the latest pipeline status.")
        return settings.pr_number, state_changed

    existing: List[dict] = _github_request(
        token=token,
        method="GET",
        url=f"{api_base}/pulls?head={owner}:{settings.branch}&state=open",
    )  # type: ignore[assignment]

    if existing:
        number = int(existing[0]["number"])
        state_changed = state_changed or settings.pr_number != number
        _github_request(
            token=token,
            method="PATCH",
            url=f"{api_base}/pulls/{number}",
            data={"body": body},
        )
        messages.append(f"Linked to existing pull request #{number} for branch {settings.branch}.")
        return number, state_changed

    created = _github_request(
        token=token,
        method="POST",
        url=f"{api_base}/pulls",
        data={
            "title": f"[Codex Pipeline] {state.project_name}",
            "head": settings.branch,
            "base": settings.base,
            "body": body,
            "draft": True,
        },
    )
    number = int(created["number"])
    messages.append(
        f"Opened draft pull request #{number} targeting {settings.base}. GitHub Actions and review workflows can"
        " now run on each sync."
    )
    return number, True


def auto_sync_stage(
    *,
    root: Path,
    state: PipelineState,
    settings: Optional[GitHubSettings],
    stage_key: str,
    stage_title: str,
    artifact_path: Optional[str],
    state_path: Path,
) -> AutoSyncResult:
    """Commit artifacts for a stage, push to GitHub, and ensure a pull request exists."""

    result = AutoSyncResult()
    if not settings or not settings.auto_sync:
        return result

    try:
        _ensure_git_repo(root)
    except GitIntegrationError as exc:
        result.messages.append(str(exc))
        return result

    tracked_paths = [state_path]
    if artifact_path:
        artifact = root / artifact_path
        if artifact.exists():
            tracked_paths.append(artifact)
    try:
        commit_sha = _commit_and_push(
            root=root,
            settings=settings,
            stage_key=stage_key,
            stage_title=stage_title,
            tracked_paths=tracked_paths,
        )
    except GitIntegrationError as exc:
        result.messages.append(str(exc))
        return result

    if not commit_sha:
        result.messages.append("GitHub sync skipped because there were no staged changes for this step.")
        return result

    result.commit_sha = commit_sha
    result.messages.append(
        f"Pushed stage '{stage_title}' to {settings.remote}/{settings.branch} (commit {commit_sha[:7]})."
    )

    try:
        pr_number, state_changed = _ensure_pull_request(
            root=root, settings=settings, state=state, messages=result.messages
        )
    except GitIntegrationError as exc:
        result.messages.append(str(exc))
        return result

    if pr_number and pr_number != settings.pr_number:
        settings.pr_number = pr_number
        result.updated_state = True
        result.pr_number = pr_number
    elif pr_number:
        result.pr_number = pr_number

    if state_changed and not result.updated_state:
        result.updated_state = True

    return result


def _latest_commit_sha(root: Path) -> str:
    return _run_git(["rev-parse", "HEAD"], root=root).stdout.strip()


def fetch_feedback(
    *,
    root: Path,
    settings: GitHubSettings,
    commit_sha: Optional[str] = None,
    max_reviews: int = 5,
) -> dict:
    """Retrieve review and check-run feedback for the tracked pull request."""

    if not settings.pr_number:
        raise GitIntegrationError("No pull request is associated with this pipeline yet. Run an auto-sync first.")

    token = _github_token()
    if not token:
        raise GitIntegrationError(
            "GitHub token not configured. Set CODEX_PIPELINE_GITHUB_TOKEN or GITHUB_TOKEN to fetch feedback."
        )

    repository, repo_updated = _ensure_repository(settings, root)
    owner, repo_name = repository.split("/", 1)
    api_base = f"https://api.github.com/repos/{owner}/{repo_name}"

    sha = commit_sha or _latest_commit_sha(root)

    reviews: List[dict] = _github_request(
        token=token,
        method="GET",
        url=f"{api_base}/pulls/{settings.pr_number}/reviews",
    )  # type: ignore[assignment]
    recent_reviews = reviews[-max_reviews:] if reviews else []

    check_runs_response = _github_request(
        token=token,
        method="GET",
        url=f"{api_base}/commits/{sha}/check-runs",
    )
    check_runs = check_runs_response.get("check_runs", []) if isinstance(check_runs_response, dict) else []

    workflows_response = _github_request(
        token=token,
        method="GET",
        url=f"{api_base}/actions/runs?branch={settings.branch}&per_page=5",
    )
    workflow_runs = workflows_response.get("workflow_runs", []) if isinstance(workflows_response, dict) else []

    return {
        "commit": sha,
        "reviews": recent_reviews,
        "check_runs": check_runs,
        "workflow_runs": workflow_runs,
        "repository": repository,
        "repository_updated": repo_updated,
    }


__all__ = [
    "AutoSyncResult",
    "GitIntegrationError",
    "auto_sync_stage",
    "fetch_feedback",
    "prepare_github_settings",
]
