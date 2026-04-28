# Submitting a Conformance Report

This directory contains conformance reports submitted by MCS API implementers.

## Directory Structure

```
reports/
  <api-version>/
    <impl-slug>/
      report.yaml
      report1.yaml   (optional, additional reports)
      report2.yaml
```

For example:

```
reports/
  v0.4.1/
    submariner/
      report.yaml
    gke/
      report.yaml
      report1.yaml
```

## How to Submit

1. **Run the conformance suite** against your implementation. See the
   [mcs-api conformance tests](https://github.com/kubernetes-sigs/mcs-api/tree/master/conformance)
   for instructions. Make sure to set the implementation flags:
   - `--organization` — your organization name (e.g., "Google Cloud")
   - `--project` — your project name (e.g., "GKE Multi Cluster Service")
   - `--version` — your implementation version (e.g., "1.2.0")
   - `--url` — link to your project's documentation

2. **Copy the generated `report.yaml`** into the appropriate directory:
   `reports/<api-version>/<impl-slug>/report.yaml`

   - `<api-version>` is the version of the MCS API your implementation targets (e.g., `v0.4.1`)
   - `<impl-slug>` is a lowercase identifier for your implementation (e.g., `submariner`, `gke`, `cilium`)
   - An organization can submit multiple reports for the same API version by naming additional files `report1.yaml`, `report2.yaml`, etc.

3. **Open a pull request** against the
   [sig-multicluster-site](https://github.com/kubernetes-sigs/sig-multicluster-site) repository.

## Requirements

The `report.yaml` must contain non-empty values for the following fields under `implementation`:

- `organization`
- `project`
- `version`
- `url`
