"""Definitions for the Codex pipeline stages and prompts."""
from __future__ import annotations

from dataclasses import dataclass
from textwrap import dedent
from typing import Dict, Iterable, List, Optional


@dataclass(frozen=True)
class Stage:
    """Represents a single stage in the workflow pipeline."""

    key: str
    title: str
    description: str
    instructions: str
    system_prompt_template: Optional[str] = None
    kickoff_prompt_template: Optional[str] = None
    ready_checklist: Optional[List[str]] = None
    artifact_path: Optional[str] = None

    def format_system_prompt(self, *, project_name: str, model_label: str, concept: str) -> Optional[str]:
        if not self.system_prompt_template:
            return None
        return dedent(self.system_prompt_template).format(
            project_name=project_name,
            model_label=model_label,
            concept=concept,
            checklist_block=_format_checklist(self.ready_checklist),
        ).strip()

    def format_kickoff_prompt(self, *, project_name: str, model_label: str, concept: str) -> Optional[str]:
        if not self.kickoff_prompt_template:
            return None
        return dedent(self.kickoff_prompt_template).format(
            project_name=project_name,
            model_label=model_label,
            concept=concept,
            checklist_block=_format_checklist(self.ready_checklist),
        ).strip()


_MODEL_LABELS = {
    "gpt-5-codex": "GPT-5 Codex",
    "gpt-5-pro": "GPT-5 Pro",
}


def model_label(model: str) -> str:
    try:
        return _MODEL_LABELS[model]
    except KeyError as exc:  # pragma: no cover - defensive programming
        raise ValueError(f"Unsupported model: {model}") from exc


def _format_checklist(checklist: Optional[Iterable[str]]) -> str:
    if not checklist:
        return ""
    bullet_lines = [f"- {item}" for item in checklist]
    return "\n".join(bullet_lines)


STAGES: Dict[str, Stage] = {}


def register_stage(stage: Stage) -> None:
    if stage.key in STAGES:  # pragma: no cover - guard against programmer error
        raise KeyError(f"Stage '{stage.key}' already registered")
    STAGES[stage.key] = stage


# --- Stage definitions ----------------------------------------------------

register_stage(
    Stage(
        key="requirements_loop",
        title="Requirements Discovery Loop",
        description=(
            "Use {model_label} inside ChatGPT Pro to interrogate the concept until "
            "the ready checklist is satisfied."
        ),
        instructions=dedent(
            """
            1. Open a new ChatGPT Pro conversation and select the desired model.
            2. Paste the system prompt into the conversation instructions panel.
            3. Send the kickoff prompt as your first message and answer follow-up questions
               from the assistant.
            4. Update your answers until every item in the ready checklist is satisfied.
            5. Conclude the loop by typing **READY CHECK PASSED**.
            """
        ).strip(),
        system_prompt_template="""
            You are {model_label}, an expert product requirements analyst.
            Project name: {project_name}.

            Your mission is to facilitate a discovery interview with the human builder.
            Ask one focused question per turn, then update a running summary with the
            following sections:
              - Confirmed Facts
              - Assumptions (to be validated)
              - Open Questions
              - Ready Checklist (show each item and mark as PASS or TODO)

            Stay within the discovery scope: do not propose solutions or implementation
            details yet. Keep iterating until the human explicitly types "READY CHECK PASSED".

            Ready checklist:
            {checklist_block}
        """,
        kickoff_prompt_template="""
            Project concept: {concept}

            Begin the discovery interview now. Ask your first clarification question,
            maintain the running summary, and continue until I respond with
            "READY CHECK PASSED".
        """,
        ready_checklist=[
            "Primary user personas identified",
            "Business or mission outcomes captured",
            "Key functional capabilities outlined",
            "Non-functional and quality attributes enumerated",
            "Constraints and dependencies recorded",
            "Success metrics or acceptance tests drafted",
            "Out-of-scope boundaries acknowledged",
        ],
    )
)

register_stage(
    Stage(
        key="requirements_doc",
        title="Generate requirements.md",
        description="Draft the formal requirements artifact using normative language.",
        instructions=dedent(
            """
            1. In the same conversation (or a fresh one) with {model_label}, pin the system prompt.
            2. Provide the discovery summary and instruct the model with the kickoff prompt.
            3. Inspect the generated Markdown carefully and iterate until the ready checklist passes.
            4. Use `python -m codex.pipeline_cli capture requirements_doc` to store the approved document.
            """
        ).strip(),
        system_prompt_template="""
            You are {model_label}, acting as a senior requirements engineer for the project
            "{project_name}".

            Produce a Markdown document named `requirements.md` that uses only the modal verbs
            "shall", "shall not", "must", and "must not" for all normative statements.
            Structure the document with the following headings:
              1. Overview
              2. Functional Requirements
              3. Non-Functional Requirements
              4. Constraints
              5. Out of Scope
              6. Acceptance Criteria

            Each section should contain numbered lists. Reconfirm the ready checklist at the end
            with explicit PASS/FAIL markers. Do not include implementation details.
        """,
        kickoff_prompt_template="""
            Using the final discovery notes below, draft `requirements.md` according to the
            mandated structure and language rules. After the document, restate the ready
            checklist with PASS or TODO for each item.

            Discovery summary:
            <paste the Confirmed Facts / Assumptions / Open Questions summary here>
        """,
        ready_checklist=[
            "All required sections are present and numbered",
            "Normative statements only use shall/shall not/must/must not",
            "Acceptance criteria map to success metrics",
            "Out-of-scope items listed explicitly",
            "Ready checklist restated with PASS for every item",
        ],
        artifact_path="artifacts/requirements.md",
    )
)

register_stage(
    Stage(
        key="architecture_doc",
        title="Generate architecture.md",
        description="Capture technical decisions, components, and rationale with no code blocks.",
        instructions=dedent(
            """
            1. Start a fresh ChatGPT Pro conversation using {model_label} to avoid stale context.
            2. Pin the system prompt, then provide the final `requirements.md` along with the kickoff prompt.
            3. Request revisions until the document covers decisions, alternatives, and trade-offs satisfactorily.
            4. Save the approved artifact via `python -m codex.pipeline_cli capture architecture_doc`.
            """
        ).strip(),
        system_prompt_template="""
            You are {model_label}, working as the lead software architect for "{project_name}".
            Produce an `architecture.md` document that:
              - Summarizes the solution context and core components.
              - Details technology selections with rationale and alternatives considered.
              - Describes data flows, integration points, and deployment topology.
              - Addresses cross-cutting concerns (security, observability, compliance).

            Present decisions using Markdown with subsections per area and optional text-based diagrams
            (Mermaid or C4 notations). Do not provide any source code.
        """,
        kickoff_prompt_template="""
            Reference the approved `requirements.md` content below to produce `architecture.md`
            following the architect guidelines. Close with a table that links each architectural
            decision to the requirements it satisfies.

            Requirements:
            <paste contents of codex/artifacts/requirements.md here>
        """,
        ready_checklist=[
            "Solution context and scope described",
            "Component and integration overview documented",
            "Technology choices include rationale and alternatives",
            "Cross-cutting concerns addressed",
            "Traceability table links decisions to requirements",
        ],
        artifact_path="artifacts/architecture.md",
    )
)

register_stage(
    Stage(
        key="implementation_doc",
        title="Generate implementation.md",
        description="Create an execution-ready build plan derived from the architecture.",
        instructions=dedent(
            """
            1. Open a new conversation with {model_label} and apply the system prompt.
            2. Provide both `requirements.md` and `architecture.md` together with the kickoff message.
            3. Ensure the document enumerates tasks, module boundaries, test strategy, and deployment notes.
            4. Store the artifact using `python -m codex.pipeline_cli capture implementation_doc` once approved.
            """
        ).strip(),
        system_prompt_template="""
            You are {model_label}, the lead implementation strategist for "{project_name}".
            Produce an `implementation.md` playbook that stands alone for developers. Include:
              - A feature-by-feature work breakdown with suggested sequencing.
              - Interface contracts and data models referenced from the architecture.
              - Pseudocode or code snippets only for complex logic, otherwise describe steps plainly.
              - Environment setup, tooling, and automation instructions.
              - Testing strategy spanning unit, integration, and acceptance levels.
              - A migration or rollout plan if relevant.

            Ensure every work item maps back to architectural decisions or requirements.
        """,
        kickoff_prompt_template="""
            Using the finalized `requirements.md` and `architecture.md` documents provided below,
            produce `implementation.md` per the guidelines. Finish with a checklist of prerequisites
            the team must complete before coding starts.

            Requirements:
            <paste contents of codex/artifacts/requirements.md here>

            Architecture:
            <paste contents of codex/artifacts/architecture.md here>
        """,
        ready_checklist=[
            "Work breakdown covers all major features",
            "Interfaces and data models trace back to architecture",
            "Testing strategy spans multiple levels",
            "Environment and tooling instructions included",
            "Pre-coding readiness checklist provided",
        ],
        artifact_path="artifacts/implementation.md",
    )
)

register_stage(
    Stage(
        key="code_build",
        title="Implementation & Test Loop",
        description="Coordinate coding sessions with the selected model while keeping tests green.",
        instructions=dedent(
            """
            1. Keep `implementation.md` nearby and work feature by feature.
            2. For each feature, prime {model_label} with the relevant implementation plan excerpt.
            3. Ask for code in small, reviewable chunks; run local tests or linters after every change.
            4. Paste any failures back into the chat to obtain fixes.
            5. Summarize the completed work and test evidence in `codex/artifacts/code_log.md` using the capture command.
            """
        ).strip(),
        system_prompt_template="""
            You are {model_label} acting as a senior pair-programmer and TDD coach.
            Collaborate iteratively: plan the next minimal change, propose code, and adjust based on
            compiler or test feedback provided by the human. Never skip writing or updating tests.
            Confirm when the current slice is green before suggesting another.
        """,
        kickoff_prompt_template="""
            We are starting implementation guided by `implementation.md`. Help craft the first
            development slice by outlining the plan, proposing code, and indicating which tests to run.
        """,
        ready_checklist=[
            "Every change accompanied by tests or validation",
            "Local automated checks pass",
            "Implementation.md updated if scope shifts",
            "Summary of work captured in codex/artifacts/code_log.md",
        ],
        artifact_path="artifacts/code_log.md",
    )
)

register_stage(
    Stage(
        key="review_loop",
        title="Code Review & Remediation",
        description="Leverage the model as a reviewer until it issues a PASS verdict.",
        instructions=dedent(
            """
            1. Open a clean conversation with {model_label} acting as the reviewer.
            2. Provide diffs or pull-request summaries along with test results.
            3. Address any BLOCK or ACTION REQUIRED comments by iterating in the implementation loop.
            4. Record the final review decision using `python -m codex.pipeline_cli capture review_loop`.
            """
        ).strip(),
        system_prompt_template="""
            You are {model_label}, an uncompromising software reviewer.
            Evaluate the provided code diffs for correctness, completeness, testing, security,
            and style. Respond with a structured review containing:
              - Verdict: PASS or BLOCK
              - Major Findings (required actions)
              - Suggestions (optional improvements)
              - Tests & Evidence summary
            Refuse to issue PASS until every blocking issue is resolved.
        """,
        kickoff_prompt_template="""
            Review the following diff and context. Apply the review rubric and return a PASS or
            BLOCK decision with actionable comments.

            Context:
            <describe feature branch, link to implementation plan sections, etc.>

            Diff:
            <paste git diff or summary>

            Test Results:
            <paste latest test output>
        """,
        ready_checklist=[
            "Reviewer provides explicit PASS verdict",
            "All blocking comments resolved",
            "Test evidence attached to review",
            "Review summary saved in codex/artifacts/review_log.md",
        ],
        artifact_path="artifacts/review_log.md",
    )
)

register_stage(
    Stage(
        key="ready_gate",
        title="Release Readiness Summary",
        description="Compile evidence that the work meets the ready threshold before closure.",
        instructions=dedent(
            """
            1. Once review passes, ask {model_label} to act as a release manager using the prompts below.
            2. Provide links or excerpts from `requirements.md`, `architecture.md`, test results, and the final diff.
            3. Capture the readiness report via `python -m codex.pipeline_cli capture ready_gate`.
            """
        ).strip(),
        system_prompt_template="""
            You are {model_label} serving as the release manager for "{project_name}".
            Assess whether the increment is ready to ship by verifying:
              - Requirements satisfied with evidence links
              - Architecture and implementation documents updated if scope changed
              - Test suite coverage and results
              - Outstanding risks, mitigations, and follow-up actions

            Produce a Markdown readiness report summarizing the evidence and a final READY / NOT READY decision.
        """,
        kickoff_prompt_template="""
            Using the supplied artifacts and test evidence, create the release readiness report.
            Explicitly cite the supporting documents and conclude with READY or NOT READY plus next steps.
        """,
        ready_checklist=[
            "Requirements traced to implemented work",
            "Test evidence documented",
            "Risks and mitigations listed",
            "Final READY/NOT READY decision recorded",
        ],
        artifact_path="artifacts/ready_report.md",
    )
)


STAGE_ORDER = [
    "requirements_loop",
    "requirements_doc",
    "architecture_doc",
    "implementation_doc",
    "code_build",
    "review_loop",
    "ready_gate",
]


ARTIFACT_STAGES = [stage.key for stage in STAGES.values() if stage.artifact_path]


def get_stage(stage_key: str) -> Stage:
    try:
        return STAGES[stage_key]
    except KeyError as exc:  # pragma: no cover - defensive
        raise KeyError(f"Unknown stage: {stage_key}") from exc


__all__ = [
    "Stage",
    "STAGES",
    "STAGE_ORDER",
    "ARTIFACT_STAGES",
    "get_stage",
    "model_label",
]
