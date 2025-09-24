#!/usr/bin/env python3
"""
Requirements Document Validator
Validates that requirements follow RFC 2119 language and best practices.
"""

import json
import re
import sys
from pathlib import Path
from typing import List, Dict, Any


class RequirementsValidator:
    """Validates requirements documents for completeness and clarity."""

    RFC2119_KEYWORDS = [
        "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT",
        "SHOULD", "SHOULD NOT", "RECOMMENDED", "MAY", "OPTIONAL"
    ]

    REQUIRED_SECTIONS = [
        "Functional Requirements",
        "Non-Functional Requirements",
        "Constraints",
        "Assumptions",
        "Acceptance Criteria"
    ]

    def __init__(self, filepath: str):
        self.filepath = Path(filepath)
        self.content = ""
        self.issues = []
        self.warnings = []
        self.stats = {}

    def validate(self) -> Dict[str, Any]:
        """Run all validation checks."""
        if not self.filepath.exists():
            return {
                "passed": False,
                "issues": [f"Requirements file not found: {self.filepath}"],
                "warnings": [],
                "stats": {}
            }

        self.content = self.filepath.read_text()

        self._check_structure()
        self._check_rfc2119_usage()
        self._check_requirement_format()
        self._check_testability()
        self._check_completeness()
        self._gather_statistics()

        passed = len(self.issues) == 0

        return {
            "passed": passed,
            "issues": self.issues,
            "warnings": self.warnings,
            "stats": self.stats
        }

    def _check_structure(self):
        """Check if all required sections are present."""
        for section in self.REQUIRED_SECTIONS:
            if section.lower() not in self.content.lower():
                self.issues.append(f"Missing required section: {section}")

    def _check_rfc2119_usage(self):
        """Verify proper use of RFC 2119 keywords."""
        lines = self.content.split("\n")
        requirement_lines = [
            (i, line) for i, line in enumerate(lines, 1)
            if line.strip().startswith("- ") or re.match(r"^\d+\.", line.strip())
        ]

        for line_num, line in requirement_lines:
            has_keyword = any(keyword in line.upper() for keyword in self.RFC2119_KEYWORDS)
            if not has_keyword:
                self.warnings.append(
                    f"Line {line_num}: Requirement lacks RFC 2119 keyword: {line[:50]}..."
                )

        # Check for lowercase RFC 2119 keywords
        for keyword in self.RFC2119_KEYWORDS:
            if keyword.lower() in self.content and keyword not in self.content:
                self.warnings.append(
                    f"RFC 2119 keyword '{keyword}' should be uppercase"
                )

    def _check_requirement_format(self):
        """Check requirement formatting and numbering."""
        lines = self.content.split("\n")
        req_pattern = re.compile(r"^[A-Z]+-\d+:")

        requirements = []
        for i, line in enumerate(lines, 1):
            if req_pattern.match(line.strip()):
                requirements.append((i, line.strip()))

        # Check for unique IDs
        ids = [req[1].split(":")[0] for req in requirements]
        duplicates = [id for id in ids if ids.count(id) > 1]
        if duplicates:
            self.issues.append(f"Duplicate requirement IDs found: {set(duplicates)}")

        # Check for missing requirements in sequence
        for prefix in ["FR", "NFR", "CON"]:
            prefix_reqs = [id for id in ids if id.startswith(prefix)]
            if prefix_reqs:
                numbers = [int(id.split("-")[1]) for id in prefix_reqs]
                expected = set(range(1, max(numbers) + 1))
                actual = set(numbers)
                missing = expected - actual
                if missing:
                    self.warnings.append(
                        f"Missing {prefix} requirements: {sorted(missing)}"
                    )

    def _check_testability(self):
        """Ensure requirements are testable."""
        vague_terms = [
            "user-friendly", "easy to use", "fast", "efficient",
            "secure", "reliable", "scalable", "flexible"
        ]

        lines = self.content.split("\n")
        for i, line in enumerate(lines, 1):
            for term in vague_terms:
                if term in line.lower() and not re.search(r"\d+", line):
                    self.warnings.append(
                        f"Line {i}: Vague term '{term}' without measurable criteria"
                    )

    def _check_completeness(self):
        """Check for incomplete requirements."""
        incomplete_indicators = ["TBD", "TODO", "XXX", "???", "...", "etc"]

        for indicator in incomplete_indicators:
            if indicator in self.content:
                lines = self.content.split("\n")
                for i, line in enumerate(lines, 1):
                    if indicator in line:
                        self.issues.append(
                            f"Line {i}: Incomplete requirement contains '{indicator}'"
                        )

    def _gather_statistics(self):
        """Gather statistics about the requirements."""
        lines = self.content.split("\n")

        # Count requirements by type
        functional = len([l for l in lines if re.match(r"^FR-\d+:", l.strip())])
        non_functional = len([l for l in lines if re.match(r"^NFR-\d+:", l.strip())])
        constraints = len([l for l in lines if re.match(r"^CON-\d+:", l.strip())])

        # Count RFC 2119 keywords
        keyword_counts = {}
        for keyword in self.RFC2119_KEYWORDS:
            keyword_counts[keyword] = self.content.count(keyword)

        self.stats = {
            "total_requirements": functional + non_functional + constraints,
            "functional_requirements": functional,
            "non_functional_requirements": non_functional,
            "constraints": constraints,
            "rfc2119_keywords": keyword_counts,
            "document_lines": len(lines),
            "document_words": len(self.content.split())
        }


def main():
    if len(sys.argv) != 2:
        print("Usage: requirements_validator.py <requirements.md>")
        sys.exit(1)

    validator = RequirementsValidator(sys.argv[1])
    result = validator.validate()

    # Write results to JSON file
    with open("review_output.json", "w") as f:
        json.dump(result, f, indent=2)

    # Generate markdown report
    with open("requirements_report.md", "w") as f:
        f.write("### Requirements Validation Report\n\n")
        f.write(f"**Status:** {'PASSED' if result['passed'] else 'FAILED'}\n\n")

        if result['issues']:
            f.write("**Issues:**\n")
            for issue in result['issues']:
                f.write(f"- {issue}\n")
            f.write("\n")

        if result['warnings']:
            f.write("**Warnings:**\n")
            for warning in result['warnings']:
                f.write(f"- {warning}\n")
            f.write("\n")

        if result['stats']:
            f.write("**Statistics:**\n")
            f.write(f"- Total Requirements: {result['stats'].get('total_requirements', 0)}\n")
            f.write(f"- Functional: {result['stats'].get('functional_requirements', 0)}\n")
            f.write(f"- Non-Functional: {result['stats'].get('non_functional_requirements', 0)}\n")
            f.write(f"- Constraints: {result['stats'].get('constraints', 0)}\n")

    # Exit with appropriate code
    sys.exit(0 if result['passed'] else 1)


if __name__ == "__main__":
    main()