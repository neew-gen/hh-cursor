# Contract: Portfolio Artifact Format

**Path**: `artifacts/project-portfolio-extract/<project-slug>.yaml`

Primary deliverable — fields for pasting into Upwork or other portfolio forms.

## Required fields

| Field | Type | Notes |
|-------|------|-------|
| `parsed_at` | ISO-8601 string | when artifact was written |
| `project_slug` | string | slug from repo name or URL |
| `title` | string | portfolio card title, ≤ 70 chars ideal |
| `description` | block string | 2–4 sentences, English, facts-only |
| `project_url` | string | repo or live demo URL |
| `skills` | string[] | tags from stack evidence |
| `approved_by_user` | boolean | user selected this project |

## Provenance (recommended)

| Field | Type | Notes |
|-------|------|-------|
| `source_type` | `github_url` \| `zip_upload` \| `local_path` | how source was acquired |
| `repo_url` | string \| null | canonical GitHub URL |
| `local_path` | string | gitignored path to source tree |
| `last_commit_date` | string \| null | `YYYY-MM-DD` |
| `last_commit_sha` | string \| null | short hash |
| `stack` | string[] | detected tools/frameworks |
| `readme_excerpt` | block string \| null | for user review |
| `limitations` | string[] | e.g. "no thumbnail", "private repo via ZIP" |

## Example

```yaml
parsed_at: "2026-08-23T19:00:00+00:00"
project_slug: vue-use-api-call
title: vue-use-api-call
description: |
  TanStack Query-style composable library for Vue 3 with tests and docs.
  Built with TypeScript and Vitest.
project_url: "https://github.com/example/vue-use-api-call"
skills:
  - Vue.js
  - TypeScript
source_type: github_url
repo_url: "https://github.com/example/vue-use-api-call"
local_path: tmp/github-clones/example-vue-use-api-call
last_commit_date: "2025-03-15"
last_commit_sha: abc1234
stack:
  - Vue 3
  - Vitest
readme_excerpt: |
  A Vue composable for API calls...
approved_by_user: true
limitations: []
```

## Validation

Artifact is valid when `title`, `description`, `project_url`, and `skills` are non-empty.
