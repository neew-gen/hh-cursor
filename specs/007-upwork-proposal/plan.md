# Implementation Plan: Upwork Proposal

**Branch**: `007-upwork-proposal` | **Date**: 2026-08-23 | **Spec**: `specs/007-upwork-proposal/spec.md`

**Input**: Feature specification from `/specs/007-upwork-proposal/spec.md`

## Summary

Extract Upwork job via Browser Tab, generate tailored EN proposal from
`upwork-profile` YAML (facts) and optional `upwork-intelligence.md` (style), compose
proposal-plan artifact, then fill Upwork proposal form — stop before Send with Connects checkpoint.

## Technical Context

**Language/Version**: Python 3.11+

**Primary Dependencies**: Python standard library; reuse `resume_profile`, `resume_create.loader`

**Storage**: `artifacts/upwork-proposal/<job-slug>.yaml`, `-report.yaml`; tmp JSON in `tmp/`

**Testing**: `unittest`

**Target Platform**: Local macOS/Linux + Cursor agent with Browser Tab

**Project Type**: Python library + Cursor skill orchestration

**Constraints**:
- browser-first for job extract and apply
- no auto-submit
- Connects checkpoint before Send
- no secrets in artifacts
- facts only from profile YAML in proposal

## Constitution Check

- **Browser-First**: Pass. Job extract and proposal fill via Browser Tab; stop points documented.
- **Minimal Scope**: Pass. P1 = compose plan without submit; no profile tailoring.
- **Source Trust Ranking**: Pass. Intelligence citations in proposal-plan metadata.
- **Reusable Artifact Output**: Pass — proposal-plan and report in `artifacts/upwork-proposal/`.
- **Secret-Safe**: Pass — no cookies/tokens in artifacts.

## Browser Stop Points

1. Navigate to job URL for extract and proposal fill.
2. Login/captcha → pause, user authenticates manually.
3. Fill proposal form: cover letter, screening questions, contract terms.
4. Connects checkpoint — report required Connects; pause for user confirmation.
5. Stop before Send — user reviews and submits manually.

## Project Structure

```text
specs/007-upwork-proposal/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── checklists/requirements.md
├── contracts/
│   ├── proposal-plan-format.md
│   ├── job-extract-format.md
│   ├── cover-letter-rules.md
│   └── browser-flow.md
└── tasks.md

src/upwork_proposal/
├── __init__.py
├── models.py
├── slug.py
├── artifacts.py
├── loader.py
├── composer.py
├── validator.py
├── writer.py
└── cli.py

tests/unit/
├── test_upwork_proposal_composer.py
└── test_upwork_proposal_validator.py
```
