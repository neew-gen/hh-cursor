# Data Model: Project Portfolio Extract

## ProjectFacts

Intermediate extract from repository (CLI output).

**Fields**
- `name`: project name from README H1, package name, or folder
- `summary`: one-line from README or package description
- `readme_excerpt`: first meaningful README paragraphs
- `dependencies`: package dependency names
- `dev_dependencies`: dev dependency names
- `stack`: detected frameworks/tools
- `languages_hint`: inferred from extensions
- `last_commit_date`: ISO date or null
- `last_commit_sha`: short hash or null
- `repo_url`: canonical URL if known
- `local_path`: path to acquired source tree
- `source_type`: `github_url` | `zip_upload` | `local_path`

## PortfolioFields

Portfolio-ready subset (primary deliverable).

**Fields**
- `title`: string, ≤ 70 chars ideal
- `description`: multiline English text for portfolio form
- `project_url`: repo or demo URL
- `skills`: list of skill tag strings

## PortfolioArtifact

**Fields**
- `parsed_at`: ISO-8601 timestamp
- `project_slug`: filesystem-safe slug
- `title`, `description`, `project_url`, `skills`: PortfolioFields
- `source_type`, `repo_url`, `local_path`: provenance
- `last_commit_date`, `last_commit_sha`: optional activity
- `stack`: list of strings
- `readme_excerpt`: optional block for review
- `approved_by_user`: boolean
- `limitations`: list of strings

## Relationships

- One acquire operation produces one `ProjectFacts`.
- Agent composes `description` from `ProjectFacts` → `PortfolioArtifact`.
- Feature 008 reads `PortfolioArtifact` for browser fill.
