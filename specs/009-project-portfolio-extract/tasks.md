# Tasks: Project Portfolio Extract

**Input**: Design documents from `/specs/009-project-portfolio-extract/`

## Phase 1 — Setup

- [x] T001 Scaffold `specs/009-project-portfolio-extract/` (spec, plan, research, data-model, contracts, checklist, tasks, quickstart)
- [x] T002 Add `artifacts/project-portfolio-extract/` to `.gitignore` and package skeleton `src/project_portfolio_extract/__init__.py`

## Phase 2 — US1 Extract Portfolio Text (P1)

- [x] T003 [US1] Implement `models.py` — ProjectFacts, PortfolioArtifact
- [x] T004 [US1] Implement `artifacts.py` — paths, slug from URL/name
- [x] T005 [US1] Implement `acquire.py` — shallow clone, unzip, validate path
- [x] T006 [US1] Implement `extract.py` — README, package.json, git meta
- [x] T007 [US1] Implement `compose.py` — title, skills, skeleton description
- [x] T008 [US1] Implement `writer.py` — render portfolio artifact YAML
- [x] T009 [US1] Implement CLI: `extract-from-url`, `extract-from-path`, `unpack`, `compose-portfolio`, `write-artifact`, `artifact-path`
- [x] T010 [P] [US1] Unit test `tests/unit/test_project_portfolio_extract_extract.py` + fixture repo

**Checkpoint US1**: extract + compose + write-artifact on fixture repo.

## Phase 3 — US2/US3 Skill (P1/P2)

- [x] T011 [US2] [US3] Create `.cursor/skills/project-portfolio-extract/SKILL.md` — consent, ZIP fallback, stale pick, artifact write

## Phase 4 — US4 Integration + Polish (P3)

- [x] T012 [US4] Update `specs/008-upwork-profile-create/contracts/portfolio-from-github.md` and skill §4b to consume 009 artifacts
- [x] T013 [P] [US4] Update `.cursor/rules/spec-kit.mdc`, README, `.specify/feature.json`

## Dependencies

- T003 blocks T004–T010
- T010 checkpoint before T011
- T011 before T012 integration test path
