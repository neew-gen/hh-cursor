# Tasks: Upwork Intelligence

**Input**: Design documents from `/specs/005-upwork-intelligence/`

**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md,
contracts/

**Tests**: Focused unit tests for report rendering and runner orchestration.

**Organization**: Tasks are grouped by user story to enable independent implementation and
testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [ ] T001 Create package skeleton in `src/upwork_intelligence/__init__.py`,
  `src/upwork_intelligence/cli.py`, `src/upwork_intelligence/models.py`,
  `src/upwork_intelligence/fetchers.py`, `src/upwork_intelligence/registry.py`,
  `src/upwork_intelligence/report.py`, `src/upwork_intelligence/runner.py`, and
  `src/upwork_intelligence/synthesis.py`
- [ ] T002 [P] Create SDD docs in `specs/005-upwork-intelligence/spec.md`,
  `specs/005-upwork-intelligence/plan.md`, `specs/005-upwork-intelligence/research.md`,
  `specs/005-upwork-intelligence/quickstart.md`, `specs/005-upwork-intelligence/tasks.md`,
  `specs/005-upwork-intelligence/contracts/report-format.md`,
  `specs/005-upwork-intelligence/contracts/source-adapter.md`, and
  `specs/005-upwork-intelligence/checklists/requirements.md`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be
implemented

- [ ] T003 Implement shared dataclasses in `src/upwork_intelligence/models.py`
- [ ] T004 [P] Implement curated Upwork source registry in
  `src/upwork_intelligence/registry.py`
- [ ] T005 [P] Implement HTML fetch and text extraction helpers in
  `src/upwork_intelligence/fetchers.py` with
  `USER_AGENT=hh-cursor-upwork-intelligence/1.0`
- [ ] T006 [P] Implement deterministic Markdown renderer in
  `src/upwork_intelligence/report.py`
- [ ] T007 Implement pipeline orchestration and file output in
  `src/upwork_intelligence/runner.py`
- [ ] T008 Implement CLI entrypoint in `src/upwork_intelligence/cli.py`

**Checkpoint**: Foundation ready - user story implementation can now begin

---

## Phase 3: User Story 1 - Build Current Upwork Proposal Intelligence Brief (Priority: P1) 🎯 MVP

**Goal**: Generate a live structured report describing how clients review proposals.

**Independent Test**: Run `PYTHONPATH=src python3 -m upwork_intelligence.cli` and verify
that `artifacts/upwork-intelligence.md` is created with `Summary`,
`HowClientsReviewProposalsNow`, `Sources`, and `FreshnessAndLimitations`.

### Tests for User Story 1

- [ ] T009 [P] [US1] Add runner unit test in
  `tests/unit/test_upwork_intelligence_runner.py`
- [ ] T010 [P] [US1] Add report rendering unit test in
  `tests/unit/test_upwork_intelligence_report.py`

### Implementation for User Story 1

- [ ] T011 [US1] Implement proposal-review claim extraction rules in
  `src/upwork_intelligence/synthesis.py`
- [ ] T012 [US1] Wire source fetching, synthesis, and artifact writing in
  `src/upwork_intelligence/runner.py`
- [ ] T013 [US1] Ensure `artifacts/upwork-intelligence.md` includes source inventory and
  run freshness in `src/upwork_intelligence/report.py`

**Checkpoint**: User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Get Actionable Proposal and Profile Guidance (Priority: P2)

**Goal**: Add proposal-writing and profile-building recommendations, including Uma synergy.

- [ ] T014 [US2] Implement `WhatToWriteInProposals` synthesis themes in
  `src/upwork_intelligence/synthesis.py`
- [ ] T015 [US2] Implement `HowToBuildProfile` synthesis themes in
  `src/upwork_intelligence/synthesis.py`
- [ ] T016 [US2] Add Uma draft-first and profile-alignment conflict notes in
  `src/upwork_intelligence/synthesis.py`

**Checkpoint**: User Story 2 recommendations appear in rendered artifact

---

## Phase 5: User Story 3 - Reuse the Result in Cursor (Priority: P3)

**Goal**: Stabilize artifact contract for downstream Upwork features.

- [ ] T017 [US3] Document report contract in
  `specs/005-upwork-intelligence/contracts/report-format.md`
- [ ] T018 [US3] Document source adapter contract in
  `specs/005-upwork-intelligence/contracts/source-adapter.md`
- [ ] T019 [US3] Add quickstart validation steps in
  `specs/005-upwork-intelligence/quickstart.md`
- [ ] T020 [US3] Ignore generated artifact via `.gitignore` entry for
  `artifacts/upwork-intelligence.md`

**Checkpoint**: Artifact is stable, documented, and safe to regenerate locally

---

## Final Validation

- [ ] T021 Run `PYTHONPATH=src python3 -m unittest tests.unit.test_upwork_intelligence_report tests.unit.test_upwork_intelligence_runner`
- [ ] T022 Run quickstart from `specs/005-upwork-intelligence/quickstart.md` and verify
  `artifacts/upwork-intelligence.md`

---

## Phase 6: Browser-first fetch (post-MVP fix)

- [ ] T023 [US1] Implement browser cache ingest in `src/upwork_intelligence/fetchers.py`
  and `src/upwork_intelligence/cli.py` (`list-sources`, `ingest-text`, `run --sources-dir`)
- [ ] T024 [P] [US1] Add contracts `specs/005-upwork-intelligence/contracts/browser-flow.md`
  and `source-cache-format.md`; update `source-adapter.md`, `plan.md`, `spec.md`
- [ ] T025 [US3] Update `.cursor/skills/upwork-intelligence/SKILL.md` for Browser Tab workflow
- [ ] T026 [P] Add cache-preference test in `tests/unit/test_upwork_intelligence_runner.py`
