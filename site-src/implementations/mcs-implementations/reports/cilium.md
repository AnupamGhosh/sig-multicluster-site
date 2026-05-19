# How to reproduce Cilium conformance reports

Cilium generally submits conformance reports from CI runs, which are
linked in the commit or PR description that adds a specific report.

Alternatively, you can run the tests with the official MCS-API conformance
suite version of your choice against any Cilium Cluster Mesh setup with
EndpointSliceSync and MCS-API support enabled.

For instructions on how to set up a Cilium Cluster Mesh environment, check out
these links to the Cilium documentation:
- https://docs.cilium.io/en/stable/network/clustermesh/clustermesh/
- https://docs.cilium.io/en/stable/network/clustermesh/mcsapi/
- https://docs.cilium.io/en/stable/network/clustermesh/services/#endpointslicesync
