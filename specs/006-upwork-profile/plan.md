# Implementation Plan: Upwork Profile Collection

**Branch**: `006-upwork-profile` | **Date**: 2026-08-23 | **Spec**: `specs/006-upwork-profile/spec.md`

**Input**: Feature specification from `/specs/006-upwork-profile/spec.md`

## Summary

Collect freelancer data required to fill an Upwork profile on a later step. Q1 is an optional
Upwork profile link (Browser Tab extract); subsequent questions are dynamic gap questions for
empty required Upwork profile fields. Output: `artifacts/upwork-profile/<profile-title-slug>.yaml`.
Feature 005 (upwork-intelligence) is not used.

## Technical Context

**Language/Version**: Python 3.11+

**Primary Dependencies**: Python standard library only (`argparse`, `dataclasses`, `json`,
`pathlib`, `re`, `datetime`)

**Storage**: one final YAML artifact at `artifacts/upwork-profile/<profile-title-slug>.yaml`;
optional intermediate JSON draft in `tmp/` (gitignored)

**Testing**: `unittest`

**Target Platform**: Local macOS/Linux + Cursor agent with Browser Tab

**Project Type**: Python library + Cursor skill orchestration

**Constraints**:
- no dependency on upwork-intelligence artifact
- artifact fields mirror Upwork profile form only
- browser-first for Upwork profile page extract
- no LLM synthesis in runtime
- no secrets in repo artifacts
- shared dataclasses in `freelancer_core` (no resume_profile refactor yet)

## Constitution Check

- **Browser-First**: Pass. Upwork profile link extraction via Browser Tab; login stop.
- **Minimal Scope**: Pass. Data collection only; no profile publishing (008).
- **Source Trust Ranking**: N/A — user-provided data with field-level provenance.
- **Reusable Artifact Output**: Pass — deterministic YAML in `artifacts/`.
- **Secret-Safe**: Pass — no cookies/tokens in artifacts.

## Browser Stop Points

1. Open profile URL from Q1 in Browser Tab.
2. If login wall → pause, ask user to authenticate manually, then continue.
3. Capture page text snapshot via `browser_snapshot` for deterministic extract.
4. Do not store session cookies in repo.

## Project Structure

```text
specs/006-upwork-profile/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/
│   ├── profile-format.md
│   └── questionnaire-flow.md
└── tasks.md

src/freelancer_core/
├── models.py
└── yaml_io.py

src/upwork_profile/
├── models.py
├── schema.py
├── gaps.py
├── slug.py
├── writer.py
├── artifacts.py
├── extractor.py
├── runner.py
└── cli.py

tests/unit/
├── test_upwork_profile_gaps.py
└── test_upwork_profile_slug.py
```

**Structure Decision**: Python package handles schema, gap detection, page-text extract, YAML
write, and CLI. Shared freelancer dataclasses live in `freelancer_core` without refactoring
`resume_profile` yet.

## Complexity Tracking

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| None | N/A | N/A |
