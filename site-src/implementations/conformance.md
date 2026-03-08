# MCS-API Conformance Report Program

The MCS-API Conformance Report Program tracks the conformance status of
Multicluster Services API implementations. It provides a structured way for
implementors to submit conformance test results, helping users understand which
implementations have been validated against the API specification.

## Conformance Categories

Implementations are categorized based on their conformance report status:

| Category | Description |
|----------|-------------|
| **Conformant** | Passes all required conformance tests |
| **Partially Conformant** | Has submitted a conformance report but does not pass all required tests |
| **Stale** | Last report is more than 1 year old |

Implementations that have not yet submitted a report are listed on the
[Implementations page](index.md) but do not appear in the conformance table
until a report is submitted. Reports from release candidates are also accepted.

## Submitting a Conformance Report

There are two ways to submit a conformance report:

### Option 1: GitHub Issue (Recommended)

1. Run the MCS-API conformance test suite against your implementation
2. Save the unmodified HTML report output
3. Open a [Conformance Report issue](https://github.com/kubernetes-sigs/sig-multicluster-site/issues/new?template=conformance-report.yml) on GitHub
4. Fill in the required fields and attach your HTML report
5. A maintainer will process your submission

### Option 2: Pull Request

1. Run the MCS-API conformance test suite against your implementation
2. Save the unmodified HTML report output
3. Create or update your implementation directory under
   `site-src/conformance/reports/<implementation-slug>/`
4. Add your HTML report file named `report-YYYY-MM.html` (e.g. `report-2026-03.html`)
5. Update the `metadata.yaml` file in your directory with the latest report details
6. [Open a pull request](https://github.com/kubernetes-sigs/sig-multicluster-site/compare?template=conformance-report.md)
   using the conformance report PR template

## Report Format

Conformance reports must be the unmodified HTML output from the MCS-API
conformance test suite. Do not alter the report content — the raw output is
what gets published.

## Directory Structure (for PR Submissions)

```
site-src/conformance/reports/<implementation-slug>/
  metadata.yaml
  report-YYYY-MM.html
```

## Metadata Schema

Each implementation has a `metadata.yaml` file with the following format:

```yaml
organization: "Organization Name"
project: "Project Name"
slug: "directory-name"
url: "https://project-url.example.com"
contact:
  - "@github-handle"
# latestReport is added when the first report is submitted:
# latestReport:
#   date: "YYYY-MM-DD"
#   projectVersion: "x.y.z"
#   mcsAPIVersion: "vX.Y.Z"
#   conformanceSuiteCommit: "abc1234"  # optional
#   reportFile: "report-YYYY-MM.html"
#   result: conformant  # one of: conformant, partially-conformant
```

### Required Fields

| Field | Description |
|-------|-------------|
| `organization` | The organization behind the implementation |
| `project` | The project or product name |
| `slug` | Directory name (lowercase, hyphenated) |
| `url` | URL to the project's homepage or repository |
| `contact` | List of GitHub handles or emails for maintainers |

### Report Fields (under `latestReport`)

| Field | Description |
|-------|-------------|
| `date` | Date the conformance tests were run (YYYY-MM-DD) |
| `projectVersion` | Version of the implementation tested |
| `mcsAPIVersion` | Version of the MCS-API tested against (optional) |
| `conformanceSuiteCommit` | Git commit of the conformance suite used (optional) |
| `reportFile` | Filename of the HTML report in the same directory |
| `result` | One of: `conformant`, `partially-conformant` |

## Staleness Policy

To ensure conformance data remains current:

- Reports older than **1 year** are marked as **Stale**
- Staleness is reviewed **twice per year**, around KubeCon EU and KubeCon NA
- When a report is marked stale, the implementation maintainers are notified
  via a GitHub issue
- Maintainers have **30 days** after notification to submit an updated report

Because the MCS-API changes at a slower pace than some other Kubernetes APIs,
stale reports may still be informative. Stale implementations remain listed
with their last known result and report date so users can judge the relevance
for themselves.

## Grace Period

Existing implementations listed on the [Implementations page](index.md) have a
**6-month grace period** from the launch of this program to submit their first
conformance report.

## Good Faith Policy

Conformance reports are accepted at face value. Implementors are expected to:

- Use the latest available version of the MCS-API conformance test suite
- Submit unmodified test output
- Accurately report their conformance result

SIG-Multicluster trusts implementors to submit honest results and does not
independently verify each report.
