# Implementation Plan: Upwork Profile Create

**Branch**: `008-upwork-profile-create` | **Date**: 2026-08-22 | **Spec**: `specs/008-upwork-profile-create/spec.md`

**Input**: Feature specification from `/specs/008-upwork-profile-create/spec.md`

## Summary

Combine `artifacts/upwork-intelligence.md` (how to write) and
`artifacts/upwork-profile/<slug>.yaml` (what to include) into a fill-plan artifact, then
fill Upwork profile form via Browser Tab. Agent rewrites `overview`, `profile_title`,
experience descriptions, and skill tags; Python validates factual integrity and
orchestrates CLI merge.

## Technical Context

**Language/Version**: Python 3.11+

**Primary Dependencies**: Python standard library; reuse `resume_profile.slug` and `yaml_io`

**Storage**: `artifacts/upwork-profile-create/<slug>.yaml` (fill-plan), `<slug>-report.yaml` (fill-report); intermediate JSON in `tmp/`

**Testing**: `unittest`

**Target Platform**: Local macOS/Linux + Cursor agent with Browser Tab

**Project Type**: Python library + Cursor skill orchestration

**Constraints**:
- browser-first for Upwork form fill
- no auto-publish
- no secrets in artifacts
- facts only from profile YAML

## Constitution Check

- **Browser-First**: Pass. Upwork create/edit via Browser Tab; login/captcha stop documented.
- **Minimal Scope**: Pass. MVP = compose + fill overview, title, skills, employment.
- **Source Trust Ranking**: Pass. Intelligence citations preserved in fill-plan metadata.
- **Reusable Artifact Output**: Pass — fill-plan and fill-report in `artifacts/upwork-profile-create/`.
- **Secret-Safe**: Pass — no cookies/tokens in artifacts.

## Browser Stop Points

1. Navigate to `https://www.upwork.com/freelancer/settings/profile` (create) or `profile_link` (edit).
2. Login/captcha → pause, user authenticates manually.
3. Fill form sections per `contracts/upwork-form-mapping.md`.
4. Stop before final publish/submit — user reviews manually.

## Project Structure

```text
specs/008-upwork-profile-create/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── checklists/requirements.md
├── contracts/
│   ├── fill-plan-format.md
│   ├── upwork-form-mapping.md
│   ├── browser-flow.md
│   └── rewrite-rules.md
└── tasks.md

src/upwork_profile_create/
├── __init__.py
├── models.py
├── loader.py
├── composer.py
├── validator.py
├── mapper.py
├── artifacts.py
├── writer.py
└── cli.py

tests/unit/
└── test_upwork_profile_create_composer.py
```

## Dependencies

- Feature 005: `artifacts/upwork-intelligence.md` (optional)
- Feature 006: `artifacts/upwork-profile/<slug>.yaml` (required)
