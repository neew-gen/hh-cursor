# Implementation Plan: Resume Intelligence

**Branch**: `001-resume-intelligence` | **Date**: 2026-07-07 | **Spec**: `specs/001-resume-intelligence/spec.md`

**Input**: Feature specification from `/specs/001-resume-intelligence/spec.md`

## Summary

Build a local CLI-style mechanism that fetches live public sources about resume screening,
classifies them by trust tier, extracts resume-relevant signals, and writes one reusable
artifact at `artifacts/resume-intelligence.md`. The first version favors a curated source
registry plus deterministic synthesis over open-ended crawling so the result stays small,
traceable, and stable for reuse in Cursor.

## Technical Context

**Language/Version**: Python 3.11+

**Primary Dependencies**: Python standard library only (`argparse`, `dataclasses`,
`html.parser`, `json`, `pathlib`, `re`, `urllib`)

**Storage**: Repository files (`artifacts/` for final output, optional local cache files under
`tmp/` or in-memory runtime state only)

**Testing**: `unittest`

**Target Platform**: Local macOS/Linux shell environment

**Project Type**: CLI-style local automation tool

**Performance Goals**: Complete a typical run against the curated source registry in under
60 seconds on a normal local connection

**Constraints**:
- no secrets in repository
- artifact output must be `Markdown`
- final user-facing output must live in `artifacts/`
- partial source outages must not prevent artifact generation
- first version must stay deterministic and reviewable rather than introducing opaque
  ranking or model-based summarization

**Scale/Scope**: One curated registry, one final artifact, one local user per run, tens of
source pages rather than large-scale crawling

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **Browser-First Evidence Collection**: Pass. The feature consumes public web content and
  can defer Browser Tab interactions for future `hh.ru` UI-specific flows; the MVP does not
  require hidden integrations.
- **Minimal Scope, Maximum Traceability**: Pass. MVP is limited to one stable artifact and a
  curated source registry with citation-preserving synthesis.
- **Source Trust Ranking**: Pass. Plan includes explicit trust tiers, conflict handling, and
  evidence-backed recommendations.
- **Reusable Artifact Output**: Pass. Output is a deterministic `Markdown` artifact in
  `artifacts/`.
- **Secret-Safe Automation**: Pass. No credentials or persistent sessions are stored.

## Project Structure

### Documentation (this feature)

```text
specs/001-resume-intelligence/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/
│   ├── cli-input.md
│   ├── report-format.md
│   └── source-adapter.md
└── tasks.md
```

### Source Code (repository root)

```text
src/
└── resume_intelligence/
    ├── __init__.py
    ├── cli.py
    ├── fetchers.py
    ├── models.py
    ├── registry.py
    ├── report.py
    ├── runner.py
    └── synthesis.py

tests/
└── unit/
    ├── test_report.py
    └── test_synthesis.py

artifacts/
└── .gitkeep
```

**Structure Decision**: Use a single small Python project rooted at `src/` with a focused
package `resume_intelligence`. This keeps implementation compact, testable, and aligned with
the constitution's minimal-scope rule while preserving a stable `artifacts/` boundary for
user-facing results.

## Complexity Tracking

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| None | N/A | N/A |
