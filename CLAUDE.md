# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is the documentation website for [SIG-Multicluster](https://multicluster.sigs.k8s.io/), a Kubernetes special interest group. The site is built with MkDocs using the Material theme and deployed via Netlify.

## Build Commands

```bash
# Install dependencies (creates a Python venv and installs packages)
make install

# Build the site (outputs to site/)
make docs

# Serve locally for development (after running make install)
source ./venv/bin/activate && mkdocs serve
# Then navigate to localhost:8000

# Clean up venv and built site
make cleanup

# Deploy to gh-pages branch
mkdocs gh-deploy
```

## Architecture

- **`site-src/`** — All documentation content (Markdown). This is the `docs_dir` for MkDocs.
  - `api-types/` — API type reference docs (ClusterSet, ServiceExport, ServiceImport)
  - `concepts/` — Conceptual docs (MCS API, Work API, ClusterProfile API, namespace sameness)
  - `guides/` — Implementation guides (CoreDNS, Istio, GKE, Submariner, Gateway API)
  - `references/` — API spec and glossary
  - `blog/` — Announcements
  - `contributing/` — Contribution guides and FAQ
- **`apis/`** — Go source for Multicluster Services API types (ServiceExport, ServiceImport). These are the canonical API type definitions.
- **`mkdocs.yml`** — Site configuration, navigation structure, theme settings, and plugins
- **`netlify.toml`** — Netlify build config (runs `make docs`, publishes `site/`)
- **`OWNERS`** — Kubernetes-style reviewers/approvers list

## Key Details

- Navigation structure is defined in `mkdocs.yml` under the `nav:` key — update it when adding/removing pages.
- The site uses `mkdocs-awesome-pages-plugin`, `mkdocs-redirects`, and `mkdocs-macros-plugin` (see `requirements.txt`).
- Redirect mappings are configured in `mkdocs.yml` under `plugins > redirects > redirect_maps`.
- The project requires a Kubernetes CLA for contributions.
