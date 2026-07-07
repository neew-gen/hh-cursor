# Tasks: Resume Intelligence

**Input**: Design documents from `/specs/001-resume-intelligence/`

**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md,
data-model.md, contracts/

**Tests**: Focused unit tests are included because deterministic synthesis and report
rendering benefit from regression coverage.

**Organization**: Tasks are grouped by user story to enable independent implementation and
testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [ ] T001 Create package skeleton in `src/resume_intelligence/__init__.py`,
  `src/resume_intelligence/cli.py`, `src/resume_intelligence/models.py`,
  `src/resume_intelligence/fetchers.py`, `src/resume_intelligence/registry.py`,
  `src/resume_intelligence/report.py`, `src/resume_intelligence/runner.py`, and
  `src/resume_intelligence/synthesis.py`
- [ ] T002 Create output and test directories in `artifacts/.gitkeep`, `tests/unit/`,
  and `tests/integration/.gitkeep`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be
implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T003 Implement shared dataclasses in `src/resume_intelligence/models.py`
- [ ] T004 [P] Implement curated source registry in `src/resume_intelligence/registry.py`
- [ ] T005 [P] Implement HTML fetch and text extraction helpers in
  `src/resume_intelligence/fetchers.py`
- [ ] T006 [P] Implement deterministic Markdown renderer in `src/resume_intelligence/report.py`
- [ ] T007 Implement pipeline orchestration and file output in `src/resume_intelligence/runner.py`
- [ ] T008 Implement CLI entrypoint in `src/resume_intelligence/cli.py`

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Build Current Resume Intelligence Brief (Priority: P1) 🎯 MVP

**Goal**: Generate a live structured report describing how HR and ATS currently process
resumes.

**Independent Test**: Run `PYTHONPATH=src python3 -m resume_intelligence.cli` and verify
that `artifacts/resume-intelligence.md` is created with `Summary`,
`HowHRAndATSProcessResumesNow`, `Sources`, and `FreshnessAndLimitations`.

### Tests for User Story 1 ⚠️

- [ ] T009 [P] [US1] Add report rendering unit test in `tests/unit/test_report.py`
- [ ] T010 [P] [US1] Add screening synthesis unit test in `tests/unit/test_synthesis.py`

### Implementation for User Story 1

- [ ] T011 [US1] Implement screening claim extraction rules in
  `src/resume_intelligence/synthesis.py`
- [ ] T012 [US1] Wire source fetching, synthesis, and artifact writing for the screening
  sections in `src/resume_intelligence/runner.py`
- [ ] T013 [US1] Ensure `artifacts/resume-intelligence.md` includes source inventory and
  run freshness in `src/resume_intelligence/report.py`

**Checkpoint**: At this point, User Story 1 should be fully functional and testable
independently

---

## Phase 4: User Story 2 - Get Actionable Resume Guidance (Priority: P2)

**Goal**: Extend the report with what-to-write and how-to-build recommendations.

**Independent Test**: Run the CLI and verify that the artifact includes `WhatToWrite`,
`HowToBuildResume`, confidence labels, and recommendation citations.

### Tests for User Story 2 ⚠️

- [ ] T014 [P] [US2] Extend synthesis coverage tests for recommendation generation in
  `tests/unit/test_synthesis.py`
- [ ] T015 [P] [US2] Extend report rendering tests for recommendation sections in
  `tests/unit/test_report.py`

### Implementation for User Story 2

- [ ] T016 [US2] Implement recommendation synthesis rules for content and formatting in
  `src/resume_intelligence/synthesis.py`
- [ ] T017 [US2] Render recommendation sections with confidence labels and citations in
  `src/resume_intelligence/report.py`
- [ ] T018 [US2] Propagate recommendation results through the end-to-end runner in
  `src/resume_intelligence/runner.py`

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Reuse the Result in Cursor (Priority: P3)

**Goal**: Make the final artifact stable and explicit enough for downstream Cursor steps.

**Independent Test**: Open `artifacts/resume-intelligence.md` and verify that the stable
section structure, conflict section, and limitation notes are sufficient to reuse the file
in a follow-up prompt without reformatting.

### Tests for User Story 3 ⚠️

- [ ] T019 [P] [US3] Add stable-section structure assertions in `tests/unit/test_report.py`

### Implementation for User Story 3

- [ ] T020 [US3] Implement conflict grouping and heuristic labeling in
  `src/resume_intelligence/synthesis.py`
- [ ] T021 [US3] Render `SourceQualityAndConflicts` and limitation details in
  `src/resume_intelligence/report.py`
- [ ] T022 [US3] Finalize CLI options for output path and source limits in
  `src/resume_intelligence/cli.py`

**Checkpoint**: All user stories should now be independently functional

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T023 [P] Update usage documentation in `README.md`
- [ ] T024 Run quickstart validation from `specs/001-resume-intelligence/quickstart.md`
- [ ] T025 [P] Verify artifact naming and output location remain aligned with
  `artifacts/resume-intelligence.md`

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
- **Polish (Phase 6)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other
  stories
- **User Story 2 (P2)**: Depends on US1 data flow and extends the same artifact
- **User Story 3 (P3)**: Depends on US1 and US2 because it stabilizes the final report

### Within Each User Story

- Tests before implementation updates in the same area
- Models and registry before synthesis
- Synthesis before report rendering
- Rendering before CLI validation and documentation

### Parallel Opportunities

- T004, T005, and T006 can run in parallel after T003
- Tests inside each story can be updated in parallel
- Documentation and artifact location verification can run in parallel during polish

---

## Parallel Example: User Story 1

```bash
Task: "Add report rendering unit test in tests/unit/test_report.py"
Task: "Add screening synthesis unit test in tests/unit/test_synthesis.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational
3. Complete Phase 3: User Story 1
4. Validate that `artifacts/resume-intelligence.md` is created and usable

### Incremental Delivery

1. Build foundation for fetching, synthesis, and rendering
2. Deliver screening brief
3. Add actionable recommendations
4. Stabilize the artifact for Cursor reuse
5. Finalize README and quickstart validation

### Parallel Team Strategy

With multiple developers:

1. One developer owns registry and fetchers
2. One developer owns synthesis and report rendering
3. One developer owns CLI, validation, and documentation once the core flow exists
