# Tasks: Upwork Profile Create

**Input**: Design documents from `/specs/008-upwork-profile-create/`

## Phase 1 — Setup

- [x] T001 Create feature directory `specs/008-upwork-profile-create/`
- [x] T002 [P] Write spec.md, plan.md, research.md, data-model.md, contracts, checklist
- [x] T003 [P] Add `artifacts/upwork-profile-create/` to `.gitignore` and package skeleton `src/upwork_profile_create/__init__.py`

## Phase 2 — US1 Compose Fill Plan (P1)

**Goal**: CLI compose + validate fill-plan from profile + rewritten texts.

- [x] T004 [US1] Implement `models.py` — FillPlan, IntelligenceBrief, FillReport, UpworkProfile
- [x] T005 [US1] Implement `loader.py` — load profile YAML, parse intelligence MD
- [x] T006 [US1] Implement `composer.py` — merge profile + agent rewritten texts + metadata
- [x] T007 [US1] Implement `validator.py` — factual integrity vs source profile
- [x] T008 [US1] Implement `writer.py` — render fill-plan YAML
- [x] T009 [US1] Implement `artifacts.py` — paths, resolve fill-plan path
- [x] T010 [US1] Implement CLI: `list-profiles`, `load-inputs`, `compose`, `validate`, `artifact-path`
- [x] T011 [P] [US1] Unit test: `test_upwork_profile_create_composer.py`

**Checkpoint US1**: `compose` + `validate` succeeds on sample profile with rewritten JSON draft.

## Phase 3 — US2/US3 Browser Fill (P2)

- [x] T012 [US2] [US3] Implement `mapper.py` — field mappings, date normalization
- [x] T013 [US2] [US3] Implement CLI `write-report`, `form-mappings`
- [ ] T014 [US2] [US3] Create `.cursor/skills/upwork-profile-create/SKILL.md` — Q0 profile, Q1 mode, rewrite, browser fill

## Phase 4 — US4 Polish (P3)

- [x] T015 [US4] Write `quickstart.md`
- [ ] T016 [P] [US4] End-to-end validation on sample profile + upwork-intelligence.md

## Phase 5 — US5 Portfolio from GitHub (P2)

- [x] T017 [US5] Contract `contracts/portfolio-from-github.md` + form-mapping / browser-flow / rewrite-rules / fill-plan updates
- [x] T018 [US5] Skill §4b — consent, links, stale filter, analyze, browser Portfolio fill
- [ ] T019 [US5] E2E: user links → draft portfolio items → Upwork Portfolio modal (Save policy)

## Dependencies

- T004 blocks T005–T011
- T011 checkpoint before T014 skill
- T012 before T014 browser section
- T017–T018 before T019 portfolio E2E

## Parallel Opportunities

- T003 parallel with T004 after T002
- T011 parallel with T012 after T010
