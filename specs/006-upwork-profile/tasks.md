# Tasks: Upwork Profile Collection

**Input**: Design documents from `/specs/006-upwork-profile/`

## Phase 1: Setup

- [x] T001 Create `specs/006-upwork-profile/` with spec, plan, research, data-model, contracts
- [x] T002 Create `src/freelancer_core/` shared dataclasses and yaml_io
- [x] T003 Create package skeleton in `src/upwork_profile/`

## Phase 2: Foundational

- [x] T004 Implement models in `src/upwork_profile/models.py`
- [x] T005 Implement schema and gap questions in `src/upwork_profile/schema.py`
- [x] T006 Implement gap detection in `src/upwork_profile/gaps.py`
- [x] T007 Implement YAML writer in `src/upwork_profile/writer.py`
- [x] T008 Implement page text extractor in `src/upwork_profile/extractor.py`
- [x] T009 Implement runner and CLI in `src/upwork_profile/runner.py`, `cli.py`

## Phase 3: User Story 1 (P1)

- [x] T010 [US1] Gap CLI command for questionnaire-only flow
- [x] T011 [US1] Write artifact when profile complete

## Phase 4: User Story 2 (P2)

- [x] T012 [US2] extract-text command for Browser Tab page snapshots
- [x] T013 [US2] Upwork profile link validation

## Phase 5: User Story 3 (P3)

- [x] T014 [US3] validate command and forbidden key guard
- [x] T015 [US3] artifact-path and init-draft commands

## Phase 6: Tests & Docs

- [x] T016 Unit tests in `tests/unit/test_upwork_profile_gaps.py`, `test_upwork_profile_slug.py`
- [x] T017 quickstart.md workflow documentation
- [x] T018 Update `.gitignore` for `artifacts/upwork-profile/`
