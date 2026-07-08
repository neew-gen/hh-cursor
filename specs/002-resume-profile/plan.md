# Implementation Plan: Resume Profile Collection

**Branch**: `002-resume-profile` | **Date**: 2026-07-08 | **Spec**: `specs/002-resume-profile/spec.md`

**Input**: Feature specification from `/specs/002-resume-profile/spec.md`

## Summary

Collect user data required to fill an hh.ru resume form on a later step. Q1 is an optional
hh.ru resume link (Browser Tab extract); subsequent questions are dynamic gap questions
strictly for empty required hh form fields. Output: `artifacts/resume-profile/<target-role-slug>.yaml`.
Feature 001 (resume-intelligence) is not used.

## Technical Context

**Language/Version**: Python 3.11+

**Primary Dependencies**: Python standard library only (`argparse`, `dataclasses`, `json`,
`pathlib`, `re`, `datetime`)

**Storage**: one final YAML artifact at `artifacts/resume-profile/<target-role-slug>.yaml`; optional intermediate JSON draft in `tmp/` (gitignored)

**Testing**: `unittest`

**Target Platform**: Local macOS/Linux + Cursor agent with Browser Tab

**Project Type**: Python library + Cursor skill orchestration

**Constraints**:
- no dependency on resume-intelligence artifact
- artifact fields mirror hh.ru resume form only
- browser-first for hh.ru resume page extract
- no LLM synthesis in runtime
- no secrets in repo artifacts

## Constitution Check

- **Browser-First**: Pass. hh.ru resume link extraction via Browser Tab; login/captcha stop.
- **Minimal Scope**: Pass. Data collection only; no resume generation (003).
- **Source Trust Ranking**: N/A — user-provided data with field-level provenance.
- **Reusable Artifact Output**: Pass — deterministic YAML in `artifacts/`.
- **Secret-Safe**: Pass — contacts optional; no cookies/tokens in artifacts.

## Browser Stop Points

1. Open resume URL from Q1 in Browser Tab.
2. If login wall or captcha → pause, ask user to authenticate manually, then continue.
3. Click `Скачать` and choose `Простой текст · txt` to open the `resume_converter/...type=txt`
   document in the same browser session.
4. Treat the `type=txt` response as download HTML and pass it to deterministic extract.
5. Use `browser_snapshot` / page text only as fallback when download HTML is unavailable.
6. Do not store session cookies in repo.

## Project Structure

```text
specs/002-resume-profile/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/
│   ├── profile-format.md
│   └── questionnaire-flow.md
└── tasks.md

src/resume_profile/
├── __init__.py
├── models.py
├── schema.py
├── gaps.py
├── extractor.py
├── writer.py
├── runner.py
└── cli.py

.cursor/skills/resume-profile/
└── SKILL.md

tests/unit/
├── test_writer.py
├── test_gaps.py
└── test_extractor.py
```

**Structure Decision**: Python package handles schema, gap detection, download HTML/page-text
extract, YAML write, and CLI merge. Cursor skill orchestrates AskQuestion + Browser Tab + CLI calls.

## Complexity Tracking

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| None | N/A | N/A |
