# Tasks: Resume Profile Collection

**Input**: Design documents from `/specs/002-resume-profile/`

## Phase 1: Setup

- [x] T001 Create `specs/002-resume-profile/` with spec, plan, research, data-model, contracts
- [x] T002 Create package skeleton in `src/resume_profile/`

## Phase 2: Foundational

- [x] T003 Implement models in `src/resume_profile/models.py`
- [x] T004 Implement schema and gap questions in `src/resume_profile/schema.py`
- [x] T005 Implement gap detection in `src/resume_profile/gaps.py`
- [x] T006 Implement YAML writer in `src/resume_profile/writer.py`
- [x] T007 Implement page text extractor in `src/resume_profile/extractor.py`
- [x] T008 Implement runner and CLI in `src/resume_profile/runner.py`, `cli.py`

## Phase 3: User Story 1 (P1)

- [x] T009 [US1] Gap CLI command for questionnaire-only flow
- [x] T010 [US1] Write artifact when profile complete

## Phase 4: User Story 2 (P2)

- [x] T011 [US2] extract-text command for Browser Tab page snapshots
- [x] T012 [US2] hh.ru resume link validation

## Phase 5: User Story 3 (P3)

- [x] T013 [US3] validate command and forbidden key guard
- [x] T014 [US3] Cursor skill `resume-profile`

## Phase 6: Tests & Docs

- [x] T015 Unit tests in `tests/unit/test_writer.py`, `test_gaps.py`, `test_extractor.py`
- [x] T016 quickstart.md workflow documentation
