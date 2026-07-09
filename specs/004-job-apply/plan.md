# Implementation Plan: Job Apply for hh.ru

**Branch**: `004-job-apply` | **Date**: 2026-07-09 | **Spec**: `specs/004-job-apply/spec.md`

**Input**: Feature specification from `/specs/004-job-apply/spec.md`

## Summary

Extract vacancy from hh.ru via Browser Tab, generate tailored cover letter from
`resume-profile` YAML (facts) and optional `resume-intelligence.md` (style), compose
application-plan artifact, then fill hh.ru response form — stop before submit.

## Technical Context

**Language/Version**: Python 3.11+

**Primary Dependencies**: Python standard library; reuse `resume_profile`, `resume_create.loader`

**Storage**: `artifacts/job-apply/<vacancy-slug>.yaml`, `-report.yaml`; tmp JSON in `tmp/`

**Testing**: `unittest`

**Target Platform**: Local macOS/Linux + Cursor agent with Browser Tab

**Project Type**: Python library + Cursor skill orchestration

**Constraints**:
- browser-first for vacancy extract and apply
- no auto-submit
- no secrets in artifacts
- facts only from profile YAML in cover letter

## Constitution Check

- **Browser-First**: Pass. Vacancy extract and apply via Browser Tab; stop points documented.
- **Minimal Scope**: Pass. P1 = compose plan without submit; no resume tailoring.
- **Source Trust Ranking**: Pass. Intelligence citations in application-plan metadata.
- **Reusable Artifact Output**: Pass — application-plan and report in `artifacts/job-apply/`.
- **Secret-Safe**: Pass — no cookies/tokens in artifacts.

## Browser Stop Points

1. Navigate to vacancy URL for extract and apply.
2. Login/captcha → pause, user authenticates manually.
3. Fill response modal: select resume, paste cover letter.
4. Stop before «Отправить отклик» — user reviews manually.

## Project Structure

```text
specs/004-job-apply/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── checklists/requirements.md
├── contracts/
│   ├── application-plan-format.md
│   ├── vacancy-extract-format.md
│   ├── cover-letter-rules.md
│   └── browser-flow.md
└── tasks.md

src/job_apply/
├── __init__.py
├── models.py
├── slug.py
├── artifacts.py
├── loader.py
├── composer.py
├── validator.py
├── writer.py
└── cli.py

.cursor/skills/job-apply/
└── SKILL.md

tests/unit/
├── test_job_apply_composer.py
├── test_job_apply_validator.py
└── test_job_apply_slug.py
```

**Structure Decision**: Python package handles compose, validate, artifact paths.
Cursor skill drives AskQuestion, vacancy extract, cover letter writing, browser apply.

## Complexity Tracking

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| None | N/A | N/A |
