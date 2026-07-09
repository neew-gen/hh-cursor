# Implementation Plan: Resume Create for hh.ru

**Branch**: `003-resume-create` | **Date**: 2026-07-09 | **Spec**: `specs/003-resume-create/spec.md`

**Input**: Feature specification from `/specs/003-resume-create/spec.md`

## Summary

Combine `artifacts/resume-intelligence.md` (how to write) and
`artifacts/resume-profile/<slug>.yaml` (what to include) into a fill-plan artifact, then
fill hh.ru resume form via Browser Tab. Agent rewrites `about_me` and experience
descriptions; Python validates factual integrity and orchestrates CLI merge.

## Technical Context

**Language/Version**: Python 3.11+

**Primary Dependencies**: Python standard library; reuse `resume_profile` for YAML I/O and slug

**Storage**: `artifacts/resume-create/<slug>.yaml` (fill-plan), `artifacts/resume-create/<slug>-report.yaml` (fill-report); intermediate JSON in `tmp/`

**Testing**: `unittest`

**Target Platform**: Local macOS/Linux + Cursor agent with Browser Tab

**Project Type**: Python library + Cursor skill orchestration

**Constraints**:
- browser-first for hh.ru form fill
- no auto-publish
- no secrets in artifacts
- facts only from profile YAML

## Constitution Check

- **Browser-First**: Pass. hh.ru create/edit via Browser Tab; login/captcha stop documented.
- **Minimal Scope**: Pass. MVP = compose + fill required blocks; no vacancy tailoring.
- **Source Trust Ranking**: Pass. Intelligence citations preserved in fill-plan metadata.
- **Reusable Artifact Output**: Pass — fill-plan and fill-report in `artifacts/resume-create/`.
- **Secret-Safe**: Pass — no cookies/tokens in artifacts.

## Browser Stop Points

1. Navigate to `hh.ru/applicant/resumes` (create) or `resume_link` (edit).
2. Login/captcha → pause, user authenticates manually.
3. Fill form sections per `contracts/hh-form-mapping.md`.
4. Stop before final «Опубликовать» / «Сохранить и опубликовать» — user reviews manually.

## Project Structure

```text
specs/003-resume-create/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── checklists/requirements.md
├── contracts/
│   ├── fill-plan-format.md
│   ├── hh-form-mapping.md
│   ├── browser-flow.md
│   └── rewrite-rules.md
└── tasks.md

src/resume_create/
├── __init__.py
├── models.py
├── loader.py
├── composer.py
├── validator.py
├── mapper.py
├── artifacts.py
├── writer.py
└── cli.py

.cursor/skills/resume-create/
└── SKILL.md

tests/unit/
├── test_loader.py
├── test_composer.py
├── test_validator.py
└── test_mapper.py
```

**Structure Decision**: Python package handles load, compose, validate, artifact paths.
Cursor skill drives AskQuestion, text rewrite, and Browser Tab fill.

## Complexity Tracking

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| None | N/A | N/A |
