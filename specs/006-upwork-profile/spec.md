# Feature Specification: Upwork Profile Collection

**Feature Branch**: `006-upwork-profile`

**Created**: 2026-08-23

**Status**: Draft

**Input**: User description: "Collect Upwork freelancer profile data via optional profile link and gap questionnaire; output one YAML artifact `artifacts/upwork-profile/<profile-title-slug>.yaml`. Mirror resume-profile pattern for Upwork fields. No upwork-intelligence dependency and no profile publishing."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Questionnaire Without Link (Priority: P1)

As a freelancer, I complete the questionnaire, skip the Upwork profile link, and answer gap
questions for required Upwork profile fields to get a data file for the next profile-fill step.

**Why this priority**: Minimal path without Browser Tab and without an existing Upwork profile.

**Independent Test**: Complete the questionnaire without a link and verify
`artifacts/upwork-profile/<profile-title-slug>.yaml` is created with `input_mode: questionnaire_only`
and required MVP Upwork fields filled.

**Acceptance Scenarios**:

1. **Given** the user skips Q1 (profile link), **When** they answer gap questions for title,
   overview, rate, skills, and experience, **Then** the system creates
   `artifacts/upwork-profile/<profile-title-slug>.yaml` with provenance `from_user_answer` for
   collected fields.
2. **Given** the user indicates no work experience, **When** the questionnaire is complete,
   **Then** the artifact contains `work_experience_status: none` and empty `work_experience`.

---

### User Story 2 - Prefill From Profile Link (Priority: P2)

As a freelancer, I provide my Upwork profile URL; the system extracts data via Browser Tab and
asks gap questions only for unfilled required fields.

**Why this priority**: Reduces manual input when a public Upwork profile already exists.

**Independent Test**: Provide a valid `upwork.com/freelancers/...` link (after manual login if
needed) and verify some fields have `from_resume_link` provenance and gap questions cover only
gaps.

**Acceptance Scenarios**:

1. **Given** the user enters a valid Upwork profile link and the page is accessible,
   **When** the agent opens the profile in Browser Tab and captures page text,
   **Then** the artifact is prefilled with title, overview, skills, and experience where present.
2. **Given** extraction is partial, **When** gaps are computed, **Then** the user receives gap
   questions only for empty required MVP fields.

---

### User Story 3 - Artifact Ready For Upwork Profile Fill (Priority: P3)

As a freelancer, I receive an artifact whose fields match Upwork profile sections so a later
step (feature 008) can fill the profile without additional questions.

**Why this priority**: Completes the value of data collection — ready input for fill workflow.

**Independent Test**: Verify YAML contains all required MVP Upwork fields and excludes fields
not on Upwork (e.g. separate `key_phrases`).

**Acceptance Scenarios**:

1. **Given** collection succeeds, **When** the user opens
   `artifacts/upwork-profile/<profile-title-slug>.yaml`, **Then** the file contains
   `profile_title`, `overview`, `hourly_rate`, `skills`, `work_experience` or
   `work_experience_status: none`, plus metadata `collected_at`, `input_mode`, `limitations`.
2. **Given** a required field is missing, **When** the user tries to finalize collection,
   **Then** the system does not write the final artifact and re-asks for that field.

---

### Edge Cases

- User skips Q1 — collection via gap questionnaire only.
- Invalid or non-Upwork URL — error message, offer skip or new link.
- Login wall on Upwork — pause, user authenticates manually, agent continues.
- Partial extraction from link — gap questions for empty required fields.
- «No work experience» — allowed with explicit `work_experience_status: none`.
- Empty answer on required gap — artifact not created, re-prompt.
- Duplicate slug — new file with `(2)`, `(3)` suffix instead of overwrite.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST ask Q1 for an optional Upwork profile link; skip MUST be allowed.
- **FR-002**: System MUST extract profile fields from Upwork via Browser Tab when a valid link
  is provided.
- **FR-003**: System MUST ask gap questions only for empty required Upwork profile fields.
- **FR-004**: System MUST NOT read or depend on upwork-intelligence (feature 005).
- **FR-005**: System MUST NOT publish or edit the Upwork profile (feature 008 scope).
- **FR-006**: System MUST write exactly one final artifact to
  `artifacts/upwork-profile/<profile-title-slug>.yaml`.
- **FR-007**: System MUST record provenance per field: `from_resume_link`, `from_user_answer`,
  or `inferred`.
- **FR-008**: System MUST mirror Upwork profile sections in artifact schema (no separate
  key_phrases or tools fields).
- **FR-009**: System MUST require MVP fields: `profile_title`, `overview`, `hourly_rate`,
  `skills`, `work_experience` or explicit no-experience status.
- **FR-010**: System MUST pause and report when login blocks Upwork access.
- **FR-011**: System MUST NOT store secrets, cookies, or credentials in repository artifacts.
- **FR-012**: Users MUST be able to run collection via documented Cursor skill workflow.
- **FR-013**: System MUST validate Upwork links matching `upwork.com/freelancers/`.
- **FR-014**: When derived artifact path already exists, system MUST create a suffixed filename
  `(2)`, `(3)`, etc., without overwriting.

### Key Entities

- **UpworkProfile**: collected freelancer profile aligned with Upwork profile form sections.
- **WorkExperienceEntry**: shared dataclass (freelancer_core) for one job entry.
- **EducationEntry**: shared dataclass for education record.
- **GapField**: unfilled required field and gap question text.
- **CollectionRun**: one collection pass (input_mode, timestamps, source counts).

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: After successful collection, exactly one final file
  `artifacts/upwork-profile/<profile-title-slug>.yaml` exists.
- **SC-002**: Artifact contains all required MVP Upwork fields or explicit no-experience flag.
- **SC-003**: When Q1 is skipped, collected fields have provenance `from_user_answer`.
- **SC-004**: When extract from link succeeds, at least one field has `from_resume_link`.
- **SC-005**: Artifact has no fields absent from Upwork profile form (key_phrases, tools).

## Assumptions

- Next step (feature 008) fills Upwork profile in Browser Tab using this artifact.
- Feature 005 remains in repo but is not used at runtime for feature 006.
- Hourly rate stored as user-provided string (e.g. `50` or `50-75`).
- Extraction is browser-first with deterministic page-text parsing; no LLM synthesis.
