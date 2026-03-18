"""
Specify Pipeline Validator

Validates .specify/ artifacts produced by the Prometheus → Specify pipeline.
Based on github/spec-kit structural requirements.

Usage (standalone):
    python spec_validator.py .specify/specs/expense-tracker/
"""

import re
import sys
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class CheckResult:
    name: str
    passed: bool
    detail: str = ""


@dataclass
class ValidationResult:
    artifact: str
    checks: list  # list[CheckResult]

    @property
    def passed(self) -> bool:
        return all(c.passed for c in self.checks)

    @property
    def failures(self) -> list:
        return [c for c in self.checks if not c.passed]


@dataclass
class PipelineReport:
    feature_dir: str
    results: list = field(default_factory=list)

    @property
    def passed(self) -> bool:
        return all(r.passed for r in self.results)

    @property
    def summary(self) -> str:
        passed = sum(1 for r in self.results if r.passed)
        return f"{passed}/{len(self.results)} artifacts valid"

    def print_report(self) -> None:
        print(f"\n{'='*60}")
        print("Specify Pipeline Validation Report")
        print(f"Feature: {self.feature_dir}")
        print(f"{'='*60}")
        for result in self.results:
            status = "PASS" if result.passed else "FAIL"
            print(f"\n  [{status}]  {result.artifact}")
            for check in result.checks:
                icon = "+" if check.passed else "x"
                detail = f" -- {check.detail}" if check.detail else ""
                print(f"       {icon} {check.name}{detail}")
        print(f"\n{'='*60}")
        label = "ALL ARTIFACTS VALID" if self.passed else "VALIDATION FAILED"
        print(f"  Result: {label}  ({self.summary})")
        print(f"{'='*60}\n")


class SpecifyValidator:
    """Validates .specify/ pipeline artifacts against spec-kit structural requirements."""

    TASK_PATTERN = re.compile(r"- \[[ xX]\] T\d{3}", re.MULTILINE)

    # ------------------------------------------------------------------ #
    #  Per-artifact validators                                             #
    # ------------------------------------------------------------------ #

    def validate_constitution(self, content: str) -> ValidationResult:
        checks = []

        for section in ["## Principles", "## Version"]:
            found = section.lower() in content.lower()
            checks.append(CheckResult(
                f"Has section '{section}'", found,
                "" if found else "Missing required section"
            ))

        has_version = bool(
            re.search(r"\*\*Version\*\*.*\|.*\*\*Ratified\*\*", content) or
            re.search(r"Version.*\d+\.\d+\.\d+", content)
        )
        checks.append(CheckResult(
            "Has version metadata (Version | Ratified | Last Amended)",
            has_version,
            "" if has_version else "Missing version/ratification metadata"
        ))

        return ValidationResult("constitution.md", checks)

    def validate_spec(self, content: str) -> ValidationResult:
        checks = []

        for section in ["## User Stories", "## Functional Requirements", "## Success Criteria"]:
            found = section.lower() in content.lower()
            checks.append(CheckResult(
                f"Has section '{section}'", found,
                "" if found else "Missing required section"
            ))

        has_fr = bool(re.search(r"FR-\d{3}", content))
        checks.append(CheckResult(
            "Has functional requirements (FR-001..)",
            has_fr,
            "" if has_fr else "No FR-NNN references found"
        ))

        has_gwt = bool(re.search(
            r"\bGiven\b.+\bWhen\b.+\bThen\b", content, re.DOTALL | re.IGNORECASE
        ))
        checks.append(CheckResult(
            "Has acceptance scenarios (Given/When/Then)",
            has_gwt,
            "" if has_gwt else "No Given/When/Then acceptance scenarios found"
        ))

        return ValidationResult("spec.md", checks)

    def validate_plan(self, content: str) -> ValidationResult:
        checks = []

        for section in ["## Technical Context", "## Implementation Phases"]:
            found = section.lower() in content.lower()
            checks.append(CheckResult(
                f"Has section '{section}'", found,
                "" if found else "Missing required section"
            ))

        has_phases = bool(re.search(r"### Phase \d+|## Phase \d+", content))
        checks.append(CheckResult(
            "Has numbered implementation phases",
            has_phases,
            "" if has_phases else "No '### Phase N' headings found"
        ))

        has_tech = bool(re.search(
            r"(Language|Version|Python|Java|Node|Stack|Framework|Dependencies)",
            content, re.IGNORECASE
        ))
        checks.append(CheckResult(
            "Has tech stack info",
            has_tech,
            "" if has_tech else "No language/framework references found"
        ))

        return ValidationResult("plan.md", checks)

    def validate_tasks(self, content: str) -> ValidationResult:
        checks = []

        tasks = self.TASK_PATTERN.findall(content)
        has_enough = len(tasks) >= 3
        checks.append(CheckResult(
            "Has >= 3 tasks in T001..Tnnn format",
            has_enough,
            f"{len(tasks)} tasks found" if not has_enough else f"{len(tasks)} tasks"
        ))

        has_t001 = bool(re.search(r"\bT001\b", content))
        checks.append(CheckResult(
            "Tasks start from T001",
            has_t001,
            "" if has_t001 else "T001 not found -- tasks may not follow standard numbering"
        ))

        has_phases = bool(re.search(r"### Phase \d+|## Phase \d+|# Phase \d+", content))
        checks.append(CheckResult(
            "Tasks are organized in phases",
            has_phases,
            "" if has_phases else "No phase structure found"
        ))

        return ValidationResult("tasks.md", checks)

    # ------------------------------------------------------------------ #
    #  File-level and pipeline-level entry points                         #
    # ------------------------------------------------------------------ #

    def validate_file(self, path: Path, artifact_type: str) -> ValidationResult:
        """Validate a single artifact file by type."""
        if not path.exists():
            return ValidationResult(
                path.name,
                [CheckResult(
                    f"File exists at {path.name}", False,
                    f"File not found: {path}"
                )]
            )
        content = path.read_text(encoding="utf-8")
        validators = {
            "constitution": self.validate_constitution,
            "spec": self.validate_spec,
            "plan": self.validate_plan,
            "tasks": self.validate_tasks,
        }
        if artifact_type not in validators:
            raise ValueError(f"Unknown artifact type: {artifact_type!r}")
        return validators[artifact_type](content)

    def validate_pipeline(self, feature_dir: Path) -> PipelineReport:
        """Validate all pipeline artifacts for a .specify/specs/<feature>/ directory."""
        report = PipelineReport(str(feature_dir))

        # constitution lives in .specify/memory/ (two levels up from feature_dir)
        constitution_path = feature_dir.parent.parent / "memory" / "constitution.md"

        artifact_map = [
            (constitution_path, "constitution"),
            (feature_dir / "spec.md", "spec"),
            (feature_dir / "plan.md", "plan"),
            (feature_dir / "tasks.md", "tasks"),
        ]
        for path, artifact_type in artifact_map:
            report.results.append(self.validate_file(path, artifact_type))

        return report


# ------------------------------------------------------------------ #
#  Standalone CLI                                                      #
# ------------------------------------------------------------------ #

if __name__ == "__main__":
    feature_dir = (
        Path(sys.argv[1]) if len(sys.argv) > 1
        else Path(__file__).parent / ".specify" / "specs" / "expense-tracker"
    )
    report = SpecifyValidator().validate_pipeline(feature_dir)
    report.print_report()
    sys.exit(0 if report.passed else 1)
