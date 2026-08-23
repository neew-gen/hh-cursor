# Implementation Plan: Project Portfolio Extract

**Branch**: `009-project-portfolio-extract` | **Date**: 2026-08-23 | **Spec**: `specs/009-project-portfolio-extract/spec.md`

## Summary

Platform-agnostic CLI + slash skill: from GitHub URL, ZIP, or local folder extract
portfolio-ready `title`, `description`, `project_url`, `skills` into
`artifacts/project-portfolio-extract/<slug>.yaml`. Shallow clone and unzip are internal
acquire steps only.

## Technical Context

**Language/Version**: Python 3.11+

**Primary Dependencies**: stdlib; system `git` for shallow clone

**Storage**:
- `artifacts/project-portfolio-extract/*.yaml` (output, gitignored)
- `tmp/github-clones/`, `tmp/project-unpacks/` (cache, gitignored via `tmp/`)

**Testing**: `unittest` on extract/compose with fixture mini-repo

**Target Platform**: Local macOS/Linux shell

**Constraints**: no secrets in repo; facts-only descriptions; consent before acquire

## Constitution Check

- **Browser-First**: N/A for MVP (no browser required).
- **Minimal Scope**: one package, one skill, no hh/Upwork coupling in core.
- **Secret-Safe**: clones and ZIP in `tmp/`, artifacts local gitignored.
- **Reusable Artifact**: YAML consumed by feature 008.

## Project Structure

```text
specs/009-project-portfolio-extract/
├── spec.md
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── tasks.md
├── contracts/
│   ├── portfolio-artifact-format.md
│   ├── source-acquire-flow.md
│   ├── extract-format.md
│   └── portfolio-compose-rules.md
└── checklists/requirements.md

src/project_portfolio_extract/
├── __init__.py
├── cli.py
├── models.py
├── artifacts.py
├── acquire.py
├── extract.py
├── compose.py
└── writer.py

tests/unit/test_project_portfolio_extract_extract.py
tests/fixtures/sample-vue-repo/
```
