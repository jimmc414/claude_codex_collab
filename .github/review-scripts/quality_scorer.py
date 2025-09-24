#!/usr/bin/env python3
"""
Quality Score Calculator
Calculates overall project quality score based on various metrics.
"""

import json
import sys
from pathlib import Path
from typing import Dict, Any


class QualityScorer:
    """Calculate quality scores for the project."""

    def __init__(self):
        self.scores = {}
        self.improvements = []

    def calculate_score(
        self,
        requirements_coverage: Dict,
        documentation_report: Dict,
        test_results: str
    ) -> Dict[str, Any]:
        """Calculate overall quality score."""

        # Requirements coverage score (30 points max)
        req_score = self._calculate_requirements_score(requirements_coverage)

        # Documentation score (20 points max)
        doc_score = self._calculate_documentation_score(documentation_report)

        # Test coverage score (30 points max)
        test_score = self._calculate_test_score(test_results)

        # Code quality score (20 points max)
        code_score = 20  # Default if no code quality metrics available

        # Calculate total
        total_score = req_score + doc_score + test_score + code_score

        # Determine improvements needed
        if req_score < 25:
            self.improvements.append("Improve requirements coverage")
        if doc_score < 17:
            self.improvements.append("Enhance documentation completeness")
        if test_score < 25:
            self.improvements.append("Increase test coverage")
        if code_score < 17:
            self.improvements.append("Address code quality issues")

        return {
            "total_score": total_score,
            "requirements_coverage": req_score / 0.3,  # Convert to percentage
            "documentation_score": doc_score / 0.2,
            "test_coverage": test_score / 0.3,
            "code_quality": code_score / 0.2,
            "breakdown": {
                "requirements": f"{req_score}/30",
                "documentation": f"{doc_score}/20",
                "tests": f"{test_score}/30",
                "code": f"{code_score}/20"
            },
            "improvements": self.improvements
        }

    def _calculate_requirements_score(self, coverage: Dict) -> int:
        """Calculate requirements coverage score (max 30)."""
        if not coverage:
            return 15

        try:
            covered_percentage = coverage.get("covered_percentage", 50)
            return int(covered_percentage * 0.3)
        except:
            return 15

    def _calculate_documentation_score(self, report: Dict) -> int:
        """Calculate documentation score (max 20)."""
        if not report:
            return 10

        try:
            completeness = report.get("completeness", 50)
            return int(completeness * 0.2)
        except:
            return 10

    def _calculate_test_score(self, test_results: str) -> int:
        """Calculate test coverage score (max 30)."""
        if not test_results or not Path(test_results).exists():
            return 15

        # Parse test results (simplified)
        try:
            # This is a simplified calculation
            # In reality, you'd parse the actual test results XML/JSON
            return 20  # Default moderate score
        except:
            return 15


def main():
    if len(sys.argv) < 2:
        print("Usage: quality_scorer.py <requirements_coverage.json> [documentation_report.json] [test_results.xml]")
        sys.exit(1)

    # Load input files
    req_coverage = {}
    doc_report = {}
    test_results = ""

    try:
        with open(sys.argv[1], 'r') as f:
            req_coverage = json.load(f)
    except:
        req_coverage = {"covered_percentage": 50}

    if len(sys.argv) > 2:
        try:
            with open(sys.argv[2], 'r') as f:
                doc_report = json.load(f)
        except:
            doc_report = {"completeness": 50}

    if len(sys.argv) > 3:
        test_results = sys.argv[3]

    # Calculate score
    scorer = QualityScorer()
    result = scorer.calculate_score(req_coverage, doc_report, test_results)

    # Write output
    with open("quality_score.json", "w") as f:
        json.dump(result, f, indent=2)

    # Exit based on score
    sys.exit(0 if result["total_score"] >= 85 else 1)


if __name__ == "__main__":
    main()