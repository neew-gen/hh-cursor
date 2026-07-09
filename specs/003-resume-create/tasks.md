# Tasks: Resume Create for hh.ru

**Input**: Design documents from `/specs/003-resume-create/`

## Phase 1 — Setup

- [x] T001 Create feature directory `specs/003-resume-create/` via create-new-feature.sh
- [x] T002 [P] Write spec.md, plan.md, research.md, data-model.md, contracts, checklist
- [x] T003 [P] Add `artifacts/resume-create/` to `.gitignore` and package skeleton `src/resume_create/__init__.py`

## Phase 2 — US1 Compose Fill Plan (P1)

**Goal**: CLI compose + validate fill-plan from profile + rewritten texts.

- [x] T004 [US1] Implement `models.py` — FillPlan, IntelligenceBrief, FillReport, SectionStatus
- [x] T005 [US1] Implement `loader.py` — load profile YAML, parse intelligence MD sections
- [x] T006 [US1] Implement `composer.py` — merge profile + agent rewritten texts + metadata
- [x] T007 [US1] Implement `validator.py` — factual integrity vs source profile
- [x] T008 [US1] Implement `writer.py` — render fill-plan YAML
- [x] T009 [US1] Implement `artifacts.py` — paths, list profiles, resolve fill-plan path
- [x] T010 [US1] Implement CLI: `list-profiles`, `load-inputs`, `compose`, `validate`, `artifact-path`
- [x] T011 [P] [US1] Unit tests: `test_loader.py`, `test_composer.py`, `test_validator.py`

**Checkpoint US1**: `compose` + `validate` succeeds on sample profile with rewritten JSON draft.

## Phase 3 — US2/US3 Browser Fill (P2)

- [x] T012 [US2] [US3] Implement `mapper.py` — field mappings, date normalization, skill level labels
- [x] T013 [P] [US2] Unit test `test_mapper.py`
- [x] T014 [US2] [US3] Implement CLI `write-report`
- [x] T015 [US2] [US3] Create `.cursor/skills/resume-create/SKILL.md` — Q0 profile, Q1 mode, rewrite, browser fill

## Phase 4 — US4 Polish (P3)

- [x] T016 [US4] Write `quickstart.md`
- [x] T017 [P] [US4] End-to-end validation on `frontend-developer-vue.yaml` + `resume-intelligence.md`

## Dependencies

- T004 blocks T005–T011
- T011 checkpoint before T015 skill
- T012 before T015 browser section

## Parallel Opportunities

- T003 parallel with T004 after T002
- T011 parallel with T012 after T010
- T013 parallel with T014
