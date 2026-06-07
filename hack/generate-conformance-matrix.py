#!/usr/bin/env python3
# Copyright The Kubernetes Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Generate per-version MCS API conformance comparison page from submitted YAML reports.

Scans the mcs-implementations reports/ subdirectory for reports as YAML files and
generates a comparison Markdown page in the mcs-implementations directory.

Expected layout:
site-src/
    implementations/
        mcs-implementations/
            reports/
                v0.5.0/submariner/v0.23.0.yaml    (submitted)
                v0.5.0/gke/2026-01-01.yaml        (submitted)
                v0.5.0/gke/2026-07-01.yaml        (submitted)
            conformance-matrix.md                 (generated)
"""

from __future__ import annotations

import pathlib
from dataclasses import dataclass
from dataclasses import field
from typing import Any

import yaml

REPO_URL = "https://github.com/kubernetes-sigs/sig-multicluster-site"
MCS_IMPLEMENTATIONS_DIR = "site-src/implementations/mcs-implementations"


@dataclass
class SubmittedReport:
    """A single submitted conformance report by an implementer"""
    report_yaml: dict[str, Any]
    report_file: pathlib.Path

    def row(self) -> str:
        """Generates each table row in the comparisons page"""
        report_link = f"[{self.report_file.name}]({REPO_URL}/blob/main/{self.report_file.as_posix()})"
        cols: list[str] = []
        required_passed, required_total = self.required_counts()
        cols.append(self.organization())
        cols.append(self.project_col())
        cols.append(self.version())
        cols.append(self.tests_col(required_passed, required_total)) # Required Tests
        cols.append(self.tests_col(self.passed(), self.total())) # Total Tests
        cols.append(report_link) # Report
        return "| " + " | ".join(cols) + " |"

    def tests_col(self, passed: int, total: int) -> str:
        green_tick = " :white_check_mark:" if passed == total else ""
        return f"{passed}/{total}{green_tick}"

    def project_col(self) -> str:
        if self.url():
            return f"[{self.project()}]({self.url()})"
        return self.project()

    def required_counts(self) -> tuple[int, int]:
        required_passed = 0
        required_total = 0

        for group in self.report_yaml["groups"]:
            if group["name"] != "Required":
                continue  # skip non-required groups

            for test in group["tests"]:
                required_total += 1
                if test["passed"]:
                    required_passed += 1

        return required_passed, required_total

    def project(self) -> str:
        return self.report_yaml["implementation"].get("project", "")

    def version(self) -> str:
        return self.report_yaml["implementation"].get("version", "")

    def url(self) -> str:
        return self.report_yaml["implementation"].get("url", "")

    def passed(self) -> int:
        return self.report_yaml["passed"]

    def total(self) -> int:
        return self.report_yaml["total"]

    def organization(self) -> str:
        return self.report_yaml["implementation"].get("organization", "")


@dataclass
class ConformanceMatrix:
    """Collects submitted reports by MCS API version and renders the comparison matrix."""
    reports_by_version: dict[str, list[SubmittedReport]] = field(default_factory=dict)

    @staticmethod
    def header() -> list[str]:
        return [
            "| Organization | Project | Version | Required Tests | Total Tests | Report |",
            "|---|---|---|---|---|---|",
        ]

    def matrix(self, mcs_api_ver: str, submitted_reports: list[SubmittedReport]) -> str:
        """Generates comparisons tables for a single MCS version"""
        lines: list[str] = [f"## {mcs_api_ver}"]
        lines.extend(self.header())
        for submitted_report in submitted_reports:
            lines.append(submitted_report.row())
        return "\n".join(lines)

    def add_report(self, mcs_api_ver: str, submitted_report: SubmittedReport) -> None:
        self.reports_by_version.setdefault(mcs_api_ver, []).append(submitted_report)

    def generate_reports(self) -> str:
        """Generates all the tables in mcs-implementations/comparisons/"""
        self.sort()
        tables: list[str] = []
        # Iterate in descending order of MCS version
        for mcs_api_ver in sorted(self.reports_by_version.keys(), reverse=True):
            tables.append(self.matrix(mcs_api_ver, self.reports_by_version[mcs_api_ver]))
        return "\n\n".join(tables)

    def sort(self) -> None:
        """Sort reports per MCS ver in ascending order of organization name then project name"""
        for submitted_reports in self.reports_by_version.values():
            submitted_reports.sort(key=lambda r: (r.organization().lower(), r.project().lower()))


def main() -> None:
    project_dir = pathlib.Path(MCS_IMPLEMENTATIONS_DIR)
    reports_dir = project_dir / "reports"

    matrix = ConformanceMatrix()
    for report_file in sorted(reports_dir.glob("*/*/*.yaml")):
        with open(report_file) as f:
            report_yaml: dict[str, Any] = yaml.safe_load(f)
        mcs_api_ver = report_file.parent.parent.name
        submitted_report = SubmittedReport(
            report_yaml=report_yaml,
            report_file=report_file,
        )
        matrix.add_report(mcs_api_ver, submitted_report)

    output_file = project_dir / "conformance-matrix.md"
    sections = matrix.generate_reports()
    output_file.write_text(sections)
    print(f"Generated {output_file}")


if __name__ == "__main__":
    main()
