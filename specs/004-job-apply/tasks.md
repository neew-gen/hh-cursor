# Tasks: Job Apply for hh.ru

**Input**: Design documents from `/specs/004-job-apply/`

## Phase 1 — Setup

- [x] T001 Create feature directory `specs/004-job-apply/`
- [x] T002 [P] Write spec.md, plan.md, research.md, data-model.md, contracts, checklist
- [x] T003 [P] Add `artifacts/job-apply/` to `.gitignore` and package skeleton `src/job_apply/__init__.py`

## Phase 2 — US1 Compose Application Plan (P1)

**Goal**: CLI compose + validate application-plan from profile + vacancy + cover letter draft.

- [x] T004 [US1] Implement `models.py` — VacancySnapshot, CoverLetter, ApplicationPlan, ApplicationReport
- [x] T005 [US1] Implement `slug.py` — vacancy_slug_from_url
- [x] T006 [US1] Implement `artifacts.py` — paths, resolve application-plan path
- [x] T007 [US1] Implement `loader.py` — list profiles, load vacancy extract, load inputs
- [x] T008 [US1] Implement `composer.py` — merge vacancy + profile + draft
- [x] T009 [US1] Implement `validator.py` — factual integrity of cover letter
- [x] T010 [US1] Implement `writer.py` — render/load application-plan YAML
- [x] T011 [US1] Implement CLI: `list-profiles`, `load-inputs`, `compose`, `validate`, `artifact-path`
- [x] T012 [P] [US1] Unit tests: composer, validator, slug + fixture vacancy-extract.json

**Checkpoint US1**: `compose` + `validate` succeeds on fixture + sample profile.

## Phase 3 — US2 Browser Apply (P2)

- [x] T013 [US2] Implement CLI `write-report`
- [x] T014 [US2] Create `.cursor/skills/job-apply/SKILL.md` — Q vacancy URL, Q profile, extract, letter, apply

## Phase 4 — US3 Polish (P3)

- [x] T015 [US3] Write `quickstart.md`
- [x] T016 [P] [US3] Update README.md step 4 pipeline

## Phase 5 — US2b Persistent Resume Choice (P2)

- [x] T017 [US2b] Contract `resume-selection-format.md`
- [ ] T018 [US2b] CLI `show-resume-selection`, `clear-resume-selection`; read/write `tmp/resume-selection.json`
- [ ] T019 [US2b] Update SKILL browser step: preference → AskQuestion → save; no auto-pick by vacancy
- [ ] T020 [P] [US2b] Unit tests for resume preference load/save/clear

**Checkpoint US2b**: second apply reuses same resume from tmp; reset clears and re-prompts.

## Dependencies

- T004 blocks T005–T012
- T012 checkpoint before T014 skill
- T013 before T014 report section

## Parallel Opportunities

- T003 parallel with T004 after T002
- T012 parallel with T013 after T011
