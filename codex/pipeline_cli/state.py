"""State management utilities for the Codex pipeline CLI."""
from __future__ import annotations

from dataclasses import dataclass, field
import json
from pathlib import Path
from typing import Dict, Iterable, Optional

from .stages import STAGE_ORDER, get_stage


VALID_STATUSES = {"pending", "in_progress", "complete"}
VALID_READY_STATES = {"todo", "pass"}


@dataclass
class GitHubSettings:
    """Configuration for syncing pipeline progress to GitHub."""

    remote: str
    branch: str
    base: str
    auto_sync: bool = False
    repository: Optional[str] = None
    pr_number: Optional[int] = None

    def to_dict(self) -> Dict[str, object]:
        return {
            "remote": self.remote,
            "branch": self.branch,
            "base": self.base,
            "auto_sync": self.auto_sync,
            "repository": self.repository,
            "pr_number": self.pr_number,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, object]) -> "GitHubSettings":
        return cls(
            remote=str(data["remote"]),
            branch=str(data["branch"]),
            base=str(data["base"]),
            auto_sync=bool(data.get("auto_sync", False)),
            repository=data.get("repository") or None,
            pr_number=data.get("pr_number"),
        )


@dataclass
class PipelineState:
    """Represents persisted pipeline metadata for a project."""

    project_name: str
    concept: str
    model: str
    stage_status: Dict[str, str] = field(default_factory=dict)
    stage_notes: Dict[str, str] = field(default_factory=dict)
    github: Optional[GitHubSettings] = None
    ready_status: Dict[str, Dict[str, str]] = field(default_factory=dict)

    def __post_init__(self) -> None:
        unknown = set(self.stage_status) - set(STAGE_ORDER)
        if unknown:  # pragma: no cover - defensive check
            raise ValueError(f"Unknown stage keys in state: {sorted(unknown)}")
        for key, status in list(self.stage_status.items()):
            if status not in VALID_STATUSES:
                raise ValueError(f"Invalid status '{status}' for stage '{key}'")

    def to_dict(self) -> Dict[str, object]:
        return {
            "project_name": self.project_name,
            "concept": self.concept,
            "model": self.model,
            "stage_status": self.stage_status,
            "stage_notes": self.stage_notes,
            "github": self.github.to_dict() if self.github else None,
            "ready_status": self.ready_status,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, object]) -> "PipelineState":
        return cls(
            project_name=str(data["project_name"]),
            concept=str(data["concept"]),
            model=str(data["model"]),
            stage_status=dict(data.get("stage_status", {})),
            stage_notes=dict(data.get("stage_notes", {})),
            github=GitHubSettings.from_dict(data["github"]) if data.get("github") else None,
            ready_status={
                stage: {
                    item: str(status)
                    for item, status in items.items()
                    if str(status) in VALID_READY_STATES
                }
                for stage, items in dict(data.get("ready_status", {})).items()
            },
        )

    def set_status(self, stage: str, status: str) -> None:
        if status not in VALID_STATUSES:
            raise ValueError(f"Invalid status '{status}'")
        self.stage_status[stage] = status

    def get_status(self, stage: str) -> str:
        return self.stage_status.get(stage, "pending")

    # Ready checklist helpers ----------------------------------------------

    def _ensure_checklist_slot(self, stage: str) -> Dict[str, str]:
        """Return the ready checklist mapping for a stage, initializing defaults."""

        stage_def = get_stage(stage)
        if not stage_def.ready_checklist:
            return self.ready_status.setdefault(stage, {})

        stored = self.ready_status.setdefault(stage, {})
        normalized: Dict[str, str] = {}
        for item in stage_def.ready_checklist:
            value = stored.get(item, "todo")
            if value not in VALID_READY_STATES:
                value = "todo"
            normalized[item] = value
        self.ready_status[stage] = normalized
        return normalized

    def get_ready_status(self, stage: str) -> Dict[str, str]:
        """Expose the ready checklist state for a stage."""

        return self._ensure_checklist_slot(stage)

    def update_ready_item(self, stage: str, item: str, status: str) -> None:
        if status not in VALID_READY_STATES:
            raise ValueError(f"Invalid ready status '{status}'")
        mapping = self._ensure_checklist_slot(stage)
        stage_def = get_stage(stage)
        if stage_def.ready_checklist and item not in stage_def.ready_checklist:
            raise KeyError(f"Item '{item}' is not part of the ready checklist for stage '{stage}'.")
        mapping[item] = status

    def reset_ready(self, stage: str) -> None:
        mapping = self._ensure_checklist_slot(stage)
        for item in list(mapping):
            mapping[item] = "todo"

    def is_ready_complete(self, stage: str) -> bool:
        stage_def = get_stage(stage)
        if not stage_def.ready_checklist:
            return True
        mapping = self._ensure_checklist_slot(stage)
        return all(mapping.get(item) == "pass" for item in stage_def.ready_checklist)

    def ensure_ready(self, stage: str) -> None:
        stage_def = get_stage(stage)
        if not stage_def.ready_checklist:
            return
        if not self.is_ready_complete(stage):
            remaining = [
                item for item in stage_def.ready_checklist if self.ready_status[stage][item] != "pass"
            ]
            raise RuntimeError(
                "Ready checklist incomplete for stage '{stage}'. Remaining items: {items}".format(
                    stage=stage_def.title,
                    items=", ".join(remaining),
                )
            )

    def ensure_order(self, target_stage: str) -> None:
        """Ensure that all preceding stages are complete before moving forward."""

        try:
            index = STAGE_ORDER.index(target_stage)
        except ValueError as exc:  # pragma: no cover - defensive
            raise ValueError(f"Unknown stage '{target_stage}'") from exc
        prior = STAGE_ORDER[:index]
        blockers = [stage for stage in prior if self.get_status(stage) != "complete"]
        if blockers:
            raise RuntimeError(
                "Cannot advance stage '{stage}' until these stages are complete: {blockers}".format(
                    stage=target_stage, blockers=", ".join(blockers)
                )
            )

    def mark_complete(self, stage: str) -> None:
        self.ensure_order(stage)
        self.ensure_ready(stage)
        self.set_status(stage, "complete")

    def list_statuses(self) -> Iterable[tuple[str, str]]:
        for stage in STAGE_ORDER:
            yield stage, self.get_status(stage)


class StateManager:
    """Handles reading and writing state to disk."""

    def __init__(self, root: Path | None = None) -> None:
        default_root = Path(__file__).resolve().parents[1]
        self.root = Path(root) if root is not None else default_root
        self.state_dir = self.root / ".codex_pipeline"
        self.state_path = self.state_dir / "state.json"

    # General utilities -------------------------------------------------

    def exists(self) -> bool:
        return self.state_path.exists()

    def ensure_initialized(self) -> None:
        if not self.exists():
            raise RuntimeError(
                "Pipeline not initialized. Run 'python -m codex.pipeline_cli init' first."
            )

    # Load/save ---------------------------------------------------------

    def load(self) -> PipelineState:
        self.ensure_initialized()
        data = json.loads(self.state_path.read_text())
        return PipelineState.from_dict(data)

    def save(self, state: PipelineState) -> None:
        self.state_dir.mkdir(parents=True, exist_ok=True)
        self.state_path.write_text(json.dumps(state.to_dict(), indent=2))


__all__ = [
    "GitHubSettings",
    "PipelineState",
    "StateManager",
    "VALID_STATUSES",
    "VALID_READY_STATES",
]
