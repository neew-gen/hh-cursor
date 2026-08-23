# Implementation Plan: Upwork Intelligence

**Branch**: `005-upwork-intelligence` | **Date**: 2026-08-23 | **Spec**: `specs/005-upwork-intelligence/spec.md`

**Input**: Feature specification from `/specs/005-upwork-intelligence/spec.md`

## Summary

Build a local CLI + Browser Tab workflow that collects live public Upwork sources about
proposal review, cover-letter guidance, profile optimization, and Uma AI synergy.
Browser-cached text in `tmp/upwork-intelligence-sources/` is the primary fetch path because
Upwork returns HTTP 403 to direct fetch. Deterministic synthesis writes
`artifacts/upwork-intelligence.md`.

## Technical Context

**Language/Version**: Python 3.11+

**Primary Dependencies**: Python standard library; Cursor Browser Tab for source extract

**Storage**: `artifacts/upwork-intelligence.md` (final); `tmp/upwork-intelligence-sources/*.txt` (cache, gitignored)

**Testing**: `unittest`

**Target Platform**: Local macOS/Linux shell environment

**Project Type**: CLI-style local automation tool

**Performance Goals**: Complete a typical run against the curated three-source registry in
under 60 seconds on a normal local connection

**Constraints**:
- no secrets in repository
- artifact output must be `Markdown`
- final user-facing output must live in `artifacts/`
- partial source outages must not prevent artifact generation
- browser-first for Upwork help/resources (HTTP 403 fallback documented)
- first version must stay deterministic and reviewable

**Scale/Scope**: One curated registry with three primary sources, one final artifact, one
local user per run

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **Browser-First Evidence Collection**: Pass. Upwork sources are collected via Browser
  Tab → `ingest-text` → `run --sources-dir`. HTTP fetch remains optional fallback.
- **Minimal Scope, Maximum Traceability**: Pass. MVP is limited to one stable artifact and
  a curated three-source registry with citation-preserving synthesis.
- **Source Trust Ranking**: Pass. Plan includes explicit trust tiers, conflict handling, and
  evidence-backed recommendations.
- **Reusable Artifact Output**: Pass. Output is a deterministic `Markdown` artifact in
  `artifacts/`.
- **Secret-Safe Automation**: Pass. No credentials or persistent sessions are stored.

## Project Structure

### Documentation (this feature)

```text
specs/005-upwork-intelligence/
├── plan.md
├── research.md
├── quickstart.md
├── contracts/
│   ├── report-format.md
│   ├── source-adapter.md
│   ├── source-cache-format.md
│   └── browser-flow.md
├── checklists/
│   └── requirements.md
└── tasks.md
```

### Source Code (repository root)

```text
src/
└── upwork_intelligence/
    ├── __init__.py
    ├── cli.py
    ├── models.py
    ├── fetchers.py
    ├── registry.py
    ├── synthesis.py
    ├── report.py
    └── runner.py

tests/unit/
├── test_upwork_intelligence_report.py
└── test_upwork_intelligence_runner.py
```

## Design Notes

- Mirror `src/resume_intelligence/` package boundaries and dataclass model shapes.
- Adapt report sections to Upwork proposal/profile semantics.
- Include English synthesis themes for proposals, profile blocks, and Uma synergy.
- Registry ids: `upwork-help-proposals`, `upwork-beginners-guide`, `upwork-profile-tips`.

## Browser / UI Path

See `contracts/browser-flow.md`. For each registry URL: Browser Tab extract →
`ingest-text` → `run --sources-dir tmp/upwork-intelligence-sources`.
