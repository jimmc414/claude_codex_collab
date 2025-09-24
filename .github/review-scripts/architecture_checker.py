#!/usr/bin/env python3
"""
Architecture Document Checker
Validates architecture documents for completeness and alignment with requirements.
"""

import json
import re
import sys
from pathlib import Path
from typing import List, Dict, Any


class ArchitectureChecker:
    """Validates architecture documents."""

    REQUIRED_SECTIONS = [
        "System Overview",
        "Architecture Principles",
        "Component Design",
        "Data Model",
        "API Design",
        "Security Architecture",
        "Deployment Architecture",
        "Technology Stack"
    ]

    ARCHITECTURE_PATTERNS = [
        "MVC", "MVP", "MVVM", "Microservices", "Monolithic",
        "Event-Driven", "Layered", "Hexagonal", "Clean Architecture"
    ]

    def __init__(self, arch_filepath: str, req_filepath: str = None):
        self.arch_filepath = Path(arch_filepath)
        self.req_filepath = Path(req_filepath) if req_filepath else None
        self.arch_content = ""
        self.req_content = ""
        self.issues = []
        self.suggestions = []
        self.alignment = 100

    def validate(self) -> Dict[str, Any]:
        """Run all validation checks."""
        if not self.arch_filepath.exists():
            return {
                "passed": False,
                "issues": [f"Architecture file not found: {self.arch_filepath}"],
                "suggestions": [],
                "alignment": 0
            }

        self.arch_content = self.arch_filepath.read_text()

        if self.req_filepath and self.req_filepath.exists():
            self.req_content = self.req_filepath.read_text()

        self._check_structure()
        self._check_completeness()
        self._check_design_patterns()
        self._check_technology_choices()
        self._check_diagrams()
        if self.req_content:
            self._check_requirements_coverage()

        passed = len(self.issues) == 0

        return {
            "passed": passed,
            "issues": self.issues,
            "suggestions": self.suggestions,
            "alignment": self.alignment
        }

    def _check_structure(self):
        """Check if all required sections are present."""
        missing_sections = []
        for section in self.REQUIRED_SECTIONS:
            if section.lower() not in self.arch_content.lower():
                missing_sections.append(section)

        if missing_sections:
            self.issues.append(
                f"Missing architecture sections: {', '.join(missing_sections)}"
            )

    def _check_completeness(self):
        """Check for incomplete sections."""
        incomplete_indicators = ["TBD", "TODO", "WIP", "???", "FIXME"]

        for indicator in incomplete_indicators:
            if indicator in self.arch_content:
                lines = self.arch_content.split("\n")
                for i, line in enumerate(lines, 1):
                    if indicator in line:
                        self.issues.append(
                            f"Line {i}: Incomplete section contains '{indicator}'"
                        )

    def _check_design_patterns(self):
        """Verify architectural patterns are documented."""
        pattern_found = False
        for pattern in self.ARCHITECTURE_PATTERNS:
            if pattern.lower() in self.arch_content.lower():
                pattern_found = True
                break

        if not pattern_found:
            self.suggestions.append(
                "Consider explicitly stating the architectural pattern used"
            )

    def _check_technology_choices(self):
        """Validate technology stack documentation."""
        tech_keywords = [
            "database", "framework", "language", "library",
            "server", "cloud", "container", "deployment"
        ]

        tech_coverage = sum(
            1 for keyword in tech_keywords
            if keyword in self.arch_content.lower()
        )

        if tech_coverage < len(tech_keywords) * 0.5:
            self.suggestions.append(
                "Technology stack documentation could be more comprehensive"
            )

    def _check_diagrams(self):
        """Check for architecture diagrams."""
        diagram_indicators = [
            "```mermaid", "```plantuml", "```graphviz",
            "![", "[diagram]", "[figure]", ".png", ".jpg", ".svg"
        ]

        has_diagram = any(
            indicator in self.arch_content
            for indicator in diagram_indicators
        )

        if not has_diagram:
            self.issues.append(
                "No architecture diagrams found. Visual representations are required"
            )

    def _check_requirements_coverage(self):
        """Check if architecture covers all requirements."""
        # Extract requirement IDs from requirements document
        req_pattern = re.compile(r"([A-Z]+-\d+):")
        req_ids = req_pattern.findall(self.req_content)

        if not req_ids:
            return

        # Check how many requirements are referenced in architecture
        referenced = 0
        for req_id in req_ids:
            if req_id in self.arch_content:
                referenced += 1

        self.alignment = int((referenced / len(req_ids)) * 100) if req_ids else 100

        if self.alignment < 80:
            missing = [
                req_id for req_id in req_ids
                if req_id not in self.arch_content
            ]
            self.issues.append(
                f"Low requirements coverage ({self.alignment}%). "
                f"Missing: {', '.join(missing[:5])}"
            )


def main():
    if len(sys.argv) < 2:
        print("Usage: architecture_checker.py <architecture.md> [requirements.md]")
        sys.exit(1)

    arch_file = sys.argv[1]
    req_file = sys.argv[2] if len(sys.argv) > 2 else None

    checker = ArchitectureChecker(arch_file, req_file)
    result = checker.validate()

    # Write results to JSON file
    with open("architecture_review.json", "w") as f:
        json.dump(result, f, indent=2)

    # Generate markdown report
    with open("architecture_report.md", "w") as f:
        f.write("### Architecture Validation Report\n\n")
        f.write(f"**Status:** {'✅ Passed' if result['passed'] else '❌ Failed'}\n")
        f.write(f"**Requirements Alignment:** {result['alignment']}%\n\n")

        if result['issues']:
            f.write("**Issues:**\n")
            for issue in result['issues']:
                f.write(f"- {issue}\n")
            f.write("\n")

        if result['suggestions']:
            f.write("**Suggestions:**\n")
            for suggestion in result['suggestions']:
                f.write(f"- {suggestion}\n")

    # Exit with appropriate code
    sys.exit(0 if result['passed'] else 1)


if __name__ == "__main__":
    main()