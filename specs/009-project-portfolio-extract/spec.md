# Feature Specification: Project Portfolio Extract

**Feature Branch**: `009-project-portfolio-extract`

**Created**: 2026-08-23

**Status**: Draft

**Input**: User description: "Extract portfolio-ready project description from GitHub URL, ZIP, or local path"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Portfolio Text from GitHub URL (Priority: P1)

As a user, I provide a public GitHub project URL and receive a YAML artifact with
`title`, `description`, `project_url`, and `skills` ready to paste into a freelancer portfolio.

**Why this priority**: Core value — portfolio copy without manual README rewriting.

**Independent Test**: Run extract on a public repo URL and verify
`artifacts/project-portfolio-extract/<slug>.yaml` contains non-empty portfolio fields.

**Acceptance Scenarios**:

1. **Given** a public GitHub URL, **When** the user runs the skill, **Then** an artifact is
   created with portfolio-ready `title`, `description`, `project_url`, and `skills`.
2. **Given** extracted facts from README and manifests, **When** the agent composes
   `description`, **Then** text contains no invented metrics or clients.

---

### User Story 2 - Fallback Without Repo Access (Priority: P1)

As a user, when clone fails (private repo, 403, no git), I provide a ZIP download or local
folder path and receive the same portfolio artifact format.

**Why this priority**: Many projects are private or clone-blocked; ZIP/local is the fallback.

**Independent Test**: Point extract at a fixture directory or unpacked ZIP and verify artifact.

**Acceptance Scenarios**:

1. **Given** clone fails, **When** the user supplies a ZIP path, **Then** the system unpacks
   to gitignored temp and produces the same artifact schema.
2. **Given** the user supplies a local project folder, **When** extract runs, **Then** facts
   are read from that path without clone.

---

### User Story 3 - Multi-Project Selection (Priority: P2)

As a user, I provide several project URLs; the agent asks which to parse and flags stale
projects (~2+ years without activity) unless I explicitly approve them.

**Why this priority**: Avoids polluting portfolio with outdated work.

**Independent Test**: Provide two URLs (one recent, one stale mock) and verify only approved
projects appear in artifacts.

**Acceptance Scenarios**:

1. **Given** multiple URLs, **When** the agent lists candidates with last activity, **Then**
   the user selects which to parse before artifacts are written.
2. **Given** a stale project not selected, **When** extract completes, **Then** no artifact
   is written for that project.

---

### User Story 4 - Reuse in Upwork Profile Fill (Priority: P3)

As a user, a downstream step (`upwork-profile-create`) reads portfolio artifacts and fills
Upwork Portfolio modals without re-parsing repositories.

**Why this priority**: Separates extract from browser fill; enables reuse.

**Independent Test**: Artifact paths and fields match contract consumed by feature 008.

**Acceptance Scenarios**:

1. **Given** a portfolio artifact exists, **When** feature 008 runs portfolio fill, **Then**
   it uses artifact `title`, `description`, `project_url`, `skills` without clone.

### Edge Cases

- Invalid or non-GitHub URL — clear error; suggest ZIP or local path.
- Empty README — description composed from package manifest or folder name only.
- No `package.json` / `pyproject.toml` — skills inferred from file extensions only.
- Private repo without ZIP — agent stops and asks for local path or ZIP.
- User declines GitHub/clone consent — skill stops without writing artifacts.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST produce portfolio artifact with `title`, `description`, `project_url`, `skills`.
- **FR-002**: System MUST obtain user consent before clone or reading local/ZIP sources.
- **FR-003**: System MUST support GitHub URL, ZIP file, and local directory as sources.
- **FR-004**: System MUST use shallow clone only into gitignored temp paths.
- **FR-005**: System MUST ask user which projects to parse when multiple URLs are given.
- **FR-006**: System MUST NOT add stale projects without explicit user approval.
- **FR-007**: System MUST compose descriptions from repo facts only — no invented metrics.
- **FR-008**: System MUST write artifacts to `artifacts/project-portfolio-extract/<slug>.yaml`.
- **FR-009**: System MUST expose CLI for acquire, extract-facts, and write-artifact.

### Key Entities

- **ProjectFacts**: raw extract from README, manifests, git metadata.
- **PortfolioArtifact**: portfolio-ready fields plus provenance metadata.
- **SourceAcquireResult**: local path, source type, repo URL optional.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Public GitHub URL produces valid portfolio artifact on sample repos.
- **SC-002**: ZIP/local path produces same schema as URL path.
- **SC-003**: 100% of `skills` in artifact trace to manifest or file evidence.
- **SC-004**: Feature 008 can fill Portfolio from artifact without re-clone.

## Assumptions

- Public repos are cloneable with system `git` CLI.
- Portfolio copy is English unless user requests otherwise.
- Browser Tab is not required for MVP.
- Thumbnail/screenshot upload remains manual on Upwork.
