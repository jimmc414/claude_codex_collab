#!/usr/bin/env python3
"""
Traceability Matrix Generator
Creates a matrix showing how requirements map to architecture, implementation, and code.
"""

import re
import sys
from pathlib import Path
from typing import Dict, List, Set


def extract_requirement_ids(content: str) -> List[str]:
    """Extract requirement IDs from content."""
    pattern = re.compile(r"([A-Z]+-\d+):")
    return pattern.findall(content)


def find_references(content: str, req_id: str) -> bool:
    """Check if a requirement ID is referenced in content."""
    return req_id in content


def scan_code_files(src_dir: Path, req_id: str) -> List[str]:
    """Scan source code for requirement references."""
    files_with_reference = []

    if not src_dir.exists():
        return files_with_reference

    for file_path in src_dir.rglob("*"):
        if file_path.is_file() and file_path.suffix in [".py", ".js", ".ts", ".java", ".cpp", ".c"]:
            try:
                content = file_path.read_text()
                if req_id in content:
                    files_with_reference.append(str(file_path.relative_to(src_dir)))
            except:
                pass

    return files_with_reference


def generate_matrix(req_file: str, arch_file: str, impl_file: str, src_dir: str):
    """Generate the traceability matrix."""
    req_path = Path(req_file)
    arch_path = Path(arch_file)
    impl_path = Path(impl_file)
    src_path = Path(src_dir)

    # Read content
    req_content = req_path.read_text() if req_path.exists() else ""
    arch_content = arch_path.read_text() if arch_path.exists() else ""
    impl_content = impl_path.read_text() if impl_path.exists() else ""

    # Extract requirement IDs
    req_ids = extract_requirement_ids(req_content)

    if not req_ids:
        print("No requirements found in the format 'ID-NUM:'")
        return

    # Generate matrix header
    print("# Requirements Traceability Matrix\n")
    print("| Requirement ID | Description | Architecture | Implementation | Code Files | Status |")
    print("|----------------|-------------|--------------|----------------|------------|--------|")

    total_reqs = len(req_ids)
    fully_traced = 0

    for req_id in req_ids:
        # Extract description
        desc_match = re.search(f"{req_id}:([^\n]+)", req_content)
        description = desc_match.group(1).strip()[:50] if desc_match else "N/A"

        # Check presence in each artifact
        in_arch = "✅" if find_references(arch_content, req_id) else "❌"
        in_impl = "✅" if find_references(impl_content, req_id) else "❌"

        # Check in code
        code_files = scan_code_files(src_path, req_id)
        in_code = ", ".join(code_files[:3]) if code_files else "❌"

        # Determine status
        if in_arch == "✅" and in_impl == "✅" and code_files:
            status = "✅ Complete"
            fully_traced += 1
        elif in_arch == "✅" or in_impl == "✅" or code_files:
            status = "⚠️ Partial"
        else:
            status = "❌ Missing"

        print(f"| {req_id} | {description} | {in_arch} | {in_impl} | {in_code} | {status} |")

    # Summary
    coverage = (fully_traced / total_reqs * 100) if total_reqs > 0 else 0
    print(f"\n## Summary\n")
    print(f"- **Total Requirements:** {total_reqs}")
    print(f"- **Fully Traced:** {fully_traced}")
    print(f"- **Coverage:** {coverage:.1f}%")


def main():
    if len(sys.argv) != 5:
        print("Usage: traceability_matrix.py <requirements.md> <architecture.md> <implementation.md> <src_dir>")
        sys.exit(1)

    generate_matrix(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])


if __name__ == "__main__":
    main()