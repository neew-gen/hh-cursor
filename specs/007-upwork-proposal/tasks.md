# Tasks: Upwork Proposal

**Input**: Design documents from `/specs/007-upwork-proposal/`

## Phase 1 — Setup

- [x] T001 Create feature directory `specs/007-upwork-proposal/`
- [x] T002 [P] Write spec.md, plan.md, research.md, data-model.md, contracts, checklist
- [x] T003 [P] Add `artifacts/upwork-proposal/` to `.gitignore` and package skeleton `src/upwork_proposal/__init__.py`

## Phase 2 — US1 Compose Proposal Plan (P1)

**Goal**: CLI compose + validate proposal-plan from profile + job + proposal draft.

- [x] T004 [US1] Implement `models.py` — JobSnapshot, ProposalCoverLetter, ScreeningAnswer, ProposalPlan
- [x] T005 [US1] Implement `slug.py` — job_slug_from_url
- [x] T006 [US1] Implement `artifacts.py` — paths, resolve proposal-plan path
- [x] T007 [US1] Implement `loader.py` — list profiles, load job extract, load inputs
- [x] T008 [US1] Implement `composer.py` — merge job + profile + draft
- [x] T009 [US1] Implement `validator.py` — factual integrity of EN proposal (300–5000 chars)
- [x] T010 [US1] Implement `writer.py` — render/load proposal-plan YAML
- [x] T011 [US1] Implement CLI: `list-profiles`, `load-inputs`, `compose`, `validate`, `artifact-path`
- [x] T012 [P] [US1] Unit tests: composer, validator + fixtures

**Checkpoint US1**: `compose` + `validate` succeeds on fixture + sample profile.

## Phase 3 — US2 Browser Proposal (P2)

- [x] T013 [US2] Implement CLI `write-report`
- [ ] T014 [US2] Create `.cursor/skills/upwork-proposal/SKILL.md` — Q job URL, Q profile, extract, letter, apply

## Phase 4 — US3 Polish (P3)

- [x] T015 [US3] Write `quickstart.md`
- [ ] T016 [P] [US3] Update README.md pipeline step for Upwork proposal

## Dependencies

- T004 blocks T005–T012
- T012 checkpoint before T014 skill
- T013 before T014 report section

## Parallel Opportunities

- T003 parallel with T004 after T002
- T012 parallel with T013 after T011
