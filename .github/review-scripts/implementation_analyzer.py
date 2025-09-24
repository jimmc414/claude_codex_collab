#!/usr/bin/env python3
"""
Implementation Plan Analyzer
Validates implementation documents for completeness and feasibility.
"""

import json
import re
import sys
from pathlib import Path
from typing import List, Dict, Any


class ImplementationAnalyzer:
    """Analyzes and validates implementation plans."""

    def __init__(self, impl_file: str, arch_file: str = None, req_file: str = None):
        self.impl_filepath = Path(impl_file)
        self.arch_filepath = Path(arch_file) if arch_file else None
        self.req_filepath = Path(req_file) if req_file else None
        self.impl_content = ""
        self.arch_content = ""
        self.req_content = ""
        self.issues = []
        self.tasks = {"total": 0, "effort": "Unknown", "dependencies": 0}
        self.coverage = {"percentage": 0, "missing": []}

    def analyze(self) -> Dict[str, Any]:
        """Run all analysis checks."""
        if not self.impl_filepath.exists():
            return {
                "passed": False,
                "issues": [f"Implementation file not found: {self.impl_filepath}"],
                "tasks": self.tasks,
                "coverage": self.coverage
            }

        self.impl_content = self.impl_filepath.read_text()

        if self.arch_filepath and self.arch_filepath.exists():
            self.arch_content = self.arch_filepath.read_text()

        if self.req_filepath and self.req_filepath.exists():
            self.req_content = self.req_filepath.read_text()

        self._analyze_tasks()
        self._check_code_examples()
        self._check_dependencies()
        self._estimate_effort()
        if self.arch_content:
            self._check_architecture_coverage()
        self._validate_implementation_steps()

        passed = len(self.issues) == 0

        return {
            "passed": passed,
            "issues": self.issues,
            "tasks": self.tasks,
            "coverage": self.coverage,
            "complexity": self._calculate_complexity()
        }

    def _analyze_tasks(self):
        """Analyze task breakdown in the implementation plan."""
        # Look for task patterns
        task_patterns = [
            r"^\d+\.", r"^-\s+\[", r"^Task\s+\d+:",
            r"^Step\s+\d+:", r"^Phase\s+\d+:"
        ]

        lines = self.impl_content.split("\n")
        task_lines = []

        for line in lines:
            for pattern in task_patterns:
                if re.match(pattern, line.strip()):
                    task_lines.append(line.strip())
                    break

        self.tasks["total"] = len(task_lines)

        if self.tasks["total"] < 3:
            self.issues.append(
                "Implementation plan lacks sufficient task breakdown"
            )

        # Check for task dependencies
        dependency_keywords = ["depends on", "requires", "after", "before", "prerequisite"]
        dependency_count = sum(
            1 for line in lines
            if any(keyword in line.lower() for keyword in dependency_keywords)
        )
        self.tasks["dependencies"] = dependency_count

    def _check_code_examples(self):
        """Check for code examples and snippets."""
        code_block_pattern = r"```[\w]*\n[\s\S]*?```"
        code_blocks = re.findall(code_block_pattern, self.impl_content)

        if len(code_blocks) < 2:
            self.issues.append(
                "Implementation plan should include more code examples"
            )

        # Check for inline code
        inline_code_pattern = r"`[^`]+`"
        inline_codes = re.findall(inline_code_pattern, self.impl_content)

        if len(inline_codes) < 5:
            self.issues.append(
                "Consider adding more inline code references for clarity"
            )

    def _check_dependencies(self):
        """Check for external dependencies documentation."""
        dependency_sections = [
            "dependencies", "requirements", "prerequisites",
            "libraries", "packages", "tools"
        ]

        has_dependencies = any(
            section in self.impl_content.lower()
            for section in dependency_sections
        )

        if not has_dependencies:
            self.issues.append(
                "Implementation plan should document external dependencies"
            )

    def _estimate_effort(self):
        """Estimate implementation effort based on tasks."""
        # Simple heuristic based on task count and complexity indicators
        complexity_indicators = [
            "complex", "difficult", "challenging", "advanced",
            "optimize", "refactor", "migrate", "integrate"
        ]

        complexity_score = sum(
            1 for indicator in complexity_indicators
            if indicator in self.impl_content.lower()
        )

        if self.tasks["total"] <= 5:
            self.tasks["effort"] = "Small (1-2 days)"
        elif self.tasks["total"] <= 15:
            if complexity_score > 3:
                self.tasks["effort"] = "Large (1-2 weeks)"
            else:
                self.tasks["effort"] = "Medium (3-5 days)"
        else:
            self.tasks["effort"] = "Extra Large (2+ weeks)"

    def _check_architecture_coverage(self):
        """Check if implementation covers all architecture components."""
        # Extract component names from architecture
        component_pattern = r"#{2,3}\s+([A-Z][A-Za-z\s]+Component|Service|Module|Layer)"
        arch_components = re.findall(component_pattern, self.arch_content)

        if not arch_components:
            # Try alternative pattern
            component_pattern = r"(?:component|service|module|layer):\s*([A-Za-z]+)"
            arch_components = re.findall(component_pattern, self.arch_content, re.IGNORECASE)

        if arch_components:
            covered = 0
            missing = []
            for component in arch_components:
                if component.lower() in self.impl_content.lower():
                    covered += 1
                else:
                    missing.append(component)

            self.coverage["percentage"] = int((covered / len(arch_components)) * 100)
            self.coverage["missing"] = missing[:5]  # Limit to first 5

            if self.coverage["percentage"] < 80:
                self.issues.append(
                    f"Low architecture coverage: {self.coverage['percentage']}%"
                )

    def _validate_implementation_steps(self):
        """Validate implementation steps are clear and actionable."""
        # Check for vague instructions
        vague_terms = [
            "somehow", "maybe", "possibly", "might",
            "figure out", "work out", "think about"
        ]

        lines = self.impl_content.split("\n")
        for i, line in enumerate(lines, 1):
            for term in vague_terms:
                if term in line.lower():
                    self.issues.append(
                        f"Line {i}: Vague instruction contains '{term}'"
                    )

    def _calculate_complexity(self):
        """Calculate overall implementation complexity score."""
        score = 5  # Base score

        # Adjust based on task count
        if self.tasks["total"] > 20:
            score += 3
        elif self.tasks["total"] > 10:
            score += 2
        elif self.tasks["total"] > 5:
            score += 1

        # Adjust based on dependencies
        if self.tasks["dependencies"] > 5:
            score += 1

        # Adjust based on content length
        if len(self.impl_content) > 5000:
            score += 1

        return min(score, 10)  # Cap at 10


def main():
    if len(sys.argv) < 2:
        print("Usage: implementation_analyzer.py <implementation.md> [architecture.md] [requirements.md]")
        sys.exit(1)

    impl_file = sys.argv[1]
    arch_file = sys.argv[2] if len(sys.argv) > 2 else None
    req_file = sys.argv[3] if len(sys.argv) > 3 else None

    analyzer = ImplementationAnalyzer(impl_file, arch_file, req_file)
    result = analyzer.analyze()

    # Write results to JSON file
    with open("implementation_review.json", "w") as f:
        json.dump(result, f, indent=2)

    # Exit with appropriate code
    sys.exit(0 if result['passed'] else 1)


if __name__ == "__main__":
    main()