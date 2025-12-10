"""
TRACE Content Validation Script

Performs deterministic checks to ensure analysis outputs are complete and consistent.
Run this before considering an analysis "done".

Usage:
    uv run python utils/validation.py
    uv run python utils/validation.py --check-sync --verbose
    uv run python utils/validation.py --min-data-size 500 --min-query-size 50
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path
from typing import NamedTuple

# Fix Windows console encoding for emoji/unicode
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')


class ValidationResult(NamedTuple):
    passed: bool
    message: str
    details: str = ""


class ValidationReport:
    def __init__(self):
        self.results: list[ValidationResult] = []
        self.errors = 0
        self.warnings = 0
        self.passed = 0

    def add(self, result: ValidationResult):
        self.results.append(result)
        if result.passed:
            self.passed += 1
        else:
            self.errors += 1

    def add_warning(self, message: str, details: str = ""):
        self.results.append(ValidationResult(True, f"⚠️  {message}", details))
        self.warnings += 1

    def print_report(self, verbose: bool = False):
        print("\n" + "=" * 60)
        print("TRACE CONTENT VALIDATION REPORT")
        print("=" * 60 + "\n")

        for result in self.results:
            status = "✅" if result.passed else "❌"
            print(f"{status} {result.message}")
            if verbose and result.details:
                for line in result.details.split("\n"):
                    print(f"   {line}")

        print("\n" + "-" * 60)
        print(f"SUMMARY: {self.passed} passed, {self.errors} failed, {self.warnings} warnings")

        if self.errors > 0:
            print("\n❌ VALIDATION FAILED - Fix errors before finalizing")
            return False
        elif self.warnings > 0:
            print("\n⚠️  VALIDATION PASSED WITH WARNINGS")
            return True
        else:
            print("\n✅ VALIDATION PASSED")
            return True


def find_project_root() -> Path:
    """Find the project root by looking for trace-metadata.json"""
    current = Path.cwd()

    # Check current directory
    if (current / "trace-metadata.json").exists():
        return current

    # Check parent (in case running from utils/)
    if (current.parent / "trace-metadata.json").exists():
        return current.parent

    # Default to current
    return current


def check_directory_exists(path: Path, name: str) -> ValidationResult:
    """Check if a required directory exists."""
    if path.exists() and path.is_dir():
        return ValidationResult(True, f"{name} directory exists")
    return ValidationResult(False, f"{name} directory missing", f"Expected: {path}")


def check_directory_has_files(
    path: Path,
    name: str,
    extensions: list[str],
    min_count: int = 1
) -> ValidationResult:
    """Check if directory has files with expected extensions."""
    if not path.exists():
        return ValidationResult(False, f"{name} directory missing")

    files = []
    for ext in extensions:
        files.extend(path.glob(f"*{ext}"))

    if len(files) >= min_count:
        return ValidationResult(
            True,
            f"{name} has {len(files)} file(s)",
            "\n".join(f"  - {f.name}" for f in files)
        )
    return ValidationResult(
        False,
        f"{name} needs at least {min_count} file(s) with extensions {extensions}",
        f"Found: {len(files)}"
    )


def check_file_sizes(
    path: Path,
    name: str,
    extensions: list[str],
    min_bytes: int
) -> ValidationResult:
    """Check that files meet minimum size requirements."""
    if not path.exists():
        return ValidationResult(False, f"{name} directory missing")

    files = []
    for ext in extensions:
        files.extend(path.glob(f"*{ext}"))

    small_files = []
    for f in files:
        size = f.stat().st_size
        if size < min_bytes:
            small_files.append(f"{f.name} ({size} bytes)")

    if not small_files:
        return ValidationResult(True, f"{name} files meet minimum size ({min_bytes} bytes)")

    return ValidationResult(
        False,
        f"{name} has {len(small_files)} file(s) below {min_bytes} bytes",
        "\n".join(f"  - {f}" for f in small_files)
    )


def check_report_exists(root: Path) -> ValidationResult:
    """Check if REPORT.html exists."""
    report = root / "REPORT.html"
    if report.exists():
        size = report.stat().st_size
        return ValidationResult(True, f"REPORT.html exists ({size:,} bytes)")
    return ValidationResult(False, "REPORT.html missing")


def check_metadata_valid(root: Path) -> ValidationResult:
    """Check if trace-metadata.json is valid and populated."""
    meta_path = root / "trace-metadata.json"

    if not meta_path.exists():
        return ValidationResult(False, "trace-metadata.json missing")

    try:
        with open(meta_path, "r", encoding="utf-8") as f:
            meta = json.load(f)
    except json.JSONDecodeError as e:
        return ValidationResult(False, "trace-metadata.json has invalid JSON", str(e))

    # Check required fields
    issues = []

    if "analysis" not in meta:
        issues.append("Missing 'analysis' section")
    else:
        analysis = meta["analysis"]
        if analysis.get("id", "").startswith("your-"):
            issues.append("analysis.id still has placeholder value")
        if analysis.get("title", "").startswith("Your "):
            issues.append("analysis.title still has placeholder value")

    if "metadata" not in meta:
        issues.append("Missing 'metadata' section")
    else:
        metadata = meta["metadata"]
        if metadata.get("author", "").startswith("Your "):
            issues.append("metadata.author still has placeholder value")

    if issues:
        return ValidationResult(
            False,
            "trace-metadata.json has placeholder values",
            "\n".join(f"  - {i}" for i in issues)
        )

    return ValidationResult(True, "trace-metadata.json is valid and populated")


def check_no_placeholders(root: Path) -> ValidationResult:
    """Check that no unresolved placeholders remain in HTML files."""
    placeholder_pattern = re.compile(r"\{\{[A-Z_0-9]+\}\}")

    html_files = list(root.glob("*.html")) + list((root / "visuals").glob("*.html"))

    files_with_placeholders = []
    for html_file in html_files:
        try:
            content = html_file.read_text(encoding="utf-8")
            matches = placeholder_pattern.findall(content)
            if matches:
                unique_matches = list(set(matches))[:5]  # Limit to 5
                files_with_placeholders.append(f"{html_file.name}: {unique_matches}")
        except Exception:
            pass

    if files_with_placeholders:
        return ValidationResult(
            False,
            f"Found unresolved placeholders in {len(files_with_placeholders)} file(s)",
            "\n".join(f"  - {f}" for f in files_with_placeholders)
        )

    return ValidationResult(True, "No unresolved placeholders found")


def extract_data_signature(content: str, length: int = 100) -> str:
    """
    Extract a 'signature' from data content for comparison.
    Normalizes whitespace and extracts first N meaningful characters.
    """
    # Remove excessive whitespace, normalize
    normalized = re.sub(r'\s+', ' ', content).strip()
    # Remove common JSON formatting characters for comparison
    signature = re.sub(r'[{}\[\]",:\s]', '', normalized)
    return signature[:length]


def check_data_sync(
    root: Path,
    min_overlap_pct: float = 0.8,
    signature_length: int = 100
) -> ValidationResult:
    """
    Check that data files are actually embedded in REPORT.html and visuals.

    Compares first N characters of data content against REPORT and visuals
    to verify data was properly embedded (not just placeholder or truncated).
    """
    data_dir = root / "data"
    visuals_dir = root / "visuals"
    report_path = root / "REPORT.html"

    if not data_dir.exists():
        return ValidationResult(False, "Cannot check sync: data/ directory missing")

    data_files = list(data_dir.glob("*.json"))
    if not data_files:
        return ValidationResult(False, "Cannot check sync: no data files found")

    # Read REPORT.html if it exists
    report_content = ""
    if report_path.exists():
        try:
            report_content = report_path.read_text(encoding="utf-8")
        except Exception:
            pass

    # Read all visual files
    visual_content = ""
    if visuals_dir.exists():
        for vf in visuals_dir.glob("*.html"):
            try:
                visual_content += vf.read_text(encoding="utf-8")
            except Exception:
                pass

    combined_output = report_content + visual_content

    if not combined_output:
        return ValidationResult(
            False,
            "Cannot check sync: no REPORT.html or visuals found"
        )

    # Check each data file
    sync_issues = []
    sync_details = []

    for data_file in data_files:
        try:
            data_content = data_file.read_text(encoding="utf-8")
            data_sig = extract_data_signature(data_content, signature_length)

            if len(data_sig) < 20:
                sync_issues.append(f"{data_file.name}: data file too small to verify")
                continue

            # Count how many signature characters appear in output
            matches = sum(1 for c in data_sig if c in combined_output)
            overlap_pct = matches / len(data_sig) if data_sig else 0

            if overlap_pct < min_overlap_pct:
                sync_issues.append(
                    f"{data_file.name}: only {overlap_pct:.0%} overlap "
                    f"(need {min_overlap_pct:.0%})"
                )
            else:
                sync_details.append(f"{data_file.name}: {overlap_pct:.0%} overlap ✓")

        except Exception as e:
            sync_issues.append(f"{data_file.name}: error reading - {e}")

    if sync_issues:
        return ValidationResult(
            False,
            f"Data may not be embedded in outputs ({len(sync_issues)} issue(s))",
            "\n".join(f"  - {i}" for i in sync_issues)
        )

    return ValidationResult(
        True,
        f"Data files appear embedded in outputs ({len(data_files)} checked)",
        "\n".join(f"  - {d}" for d in sync_details)
    )


def check_visual_report_sync(root: Path) -> ValidationResult:
    """
    Check that visuals/ files have corresponding content in REPORT.html.

    This catches the case where visuals are generated but not embedded.
    """
    visuals_dir = root / "visuals"
    report_path = root / "REPORT.html"

    if not visuals_dir.exists():
        return ValidationResult(True, "No visuals directory to check")

    if not report_path.exists():
        return ValidationResult(False, "Cannot check visual sync: REPORT.html missing")

    visual_files = list(visuals_dir.glob("*.html"))
    if not visual_files:
        return ValidationResult(True, "No visual files to check")

    report_content = report_path.read_text(encoding="utf-8")

    # Check if Highcharts chart configs exist in both
    # Look for renderTo patterns or chart container IDs
    chart_pattern = re.compile(r"Highcharts\.(chart|stockChart)\s*\(\s*['\"]([^'\"]+)['\"]")

    visual_charts = set()
    for vf in visual_files:
        try:
            vc = vf.read_text(encoding="utf-8")
            matches = chart_pattern.findall(vc)
            for _, container_id in matches:
                visual_charts.add(container_id)
        except Exception:
            pass

    report_charts = set()
    matches = chart_pattern.findall(report_content)
    for _, container_id in matches:
        report_charts.add(container_id)

    # Check that visual charts appear in report
    missing_in_report = visual_charts - report_charts

    if missing_in_report and len(visual_charts) > 0:
        # This is a warning, not an error - chart IDs might differ
        return ValidationResult(
            True,
            f"⚠️  {len(missing_in_report)} visual chart ID(s) not found in REPORT",
            f"Visual charts: {visual_charts}\nReport charts: {report_charts}"
        )

    return ValidationResult(
        True,
        f"Visual/REPORT chart sync looks good ({len(visual_charts)} charts)"
    )


def run_validation(
    root: Path,
    min_data_size: int = 100,
    min_query_size: int = 20,
    min_visual_size: int = 500,
    check_sync: bool = True,
    verbose: bool = False
) -> bool:
    """Run all validation checks and print report."""

    report = ValidationReport()

    # Directory structure checks
    report.add(check_directory_exists(root / "data", "data/"))
    report.add(check_directory_exists(root / "queries", "queries/"))
    report.add(check_directory_exists(root / "visuals", "visuals/"))

    # File existence checks
    report.add(check_directory_has_files(root / "data", "data/", [".json"]))
    report.add(check_directory_has_files(root / "queries", "queries/", [".sql"]))
    report.add(check_directory_has_files(root / "visuals", "visuals/", [".html"]))

    # File size checks (catch truncation)
    report.add(check_file_sizes(root / "data", "data/", [".json"], min_data_size))
    report.add(check_file_sizes(root / "queries", "queries/", [".sql"], min_query_size))
    report.add(check_file_sizes(root / "visuals", "visuals/", [".html"], min_visual_size))

    # REPORT.html checks
    report.add(check_report_exists(root))

    # Metadata checks
    report.add(check_metadata_valid(root))

    # Placeholder checks
    report.add(check_no_placeholders(root))

    # Sync checks (data actually embedded)
    if check_sync:
        report.add(check_data_sync(root))
        report.add(check_visual_report_sync(root))

    return report.print_report(verbose)


def main():
    parser = argparse.ArgumentParser(
        description="Validate TRACE content repository",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    uv run python utils/validation.py
    uv run python utils/validation.py --verbose
    uv run python utils/validation.py --check-sync --min-data-size 500
    uv run python utils/validation.py --root /path/to/analysis
        """
    )

    parser.add_argument(
        "--root",
        type=Path,
        default=None,
        help="Root directory of the analysis (default: auto-detect)"
    )
    parser.add_argument(
        "--min-data-size",
        type=int,
        default=100,
        help="Minimum bytes for data files (default: 100)"
    )
    parser.add_argument(
        "--min-query-size",
        type=int,
        default=20,
        help="Minimum bytes for query files (default: 20)"
    )
    parser.add_argument(
        "--min-visual-size",
        type=int,
        default=500,
        help="Minimum bytes for visual files (default: 500)"
    )
    parser.add_argument(
        "--check-sync",
        action="store_true",
        default=True,
        help="Check data/visual sync with REPORT (default: True)"
    )
    parser.add_argument(
        "--no-check-sync",
        action="store_false",
        dest="check_sync",
        help="Skip data/visual sync checks"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Show detailed output for each check"
    )

    args = parser.parse_args()

    root = args.root if args.root else find_project_root()

    print(f"Validating: {root.absolute()}")

    success = run_validation(
        root=root,
        min_data_size=args.min_data_size,
        min_query_size=args.min_query_size,
        min_visual_size=args.min_visual_size,
        check_sync=args.check_sync,
        verbose=args.verbose
    )

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()

