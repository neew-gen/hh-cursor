# Research: Upwork Profile Create

**Date**: 2026-08-22

## Upwork Profile Sections (MVP)

| Section | Upwork UI label | Fill-plan field |
|---------|-----------------|-----------------|
| Title | Professional title | `profile_title` |
| Overview | Overview / bio | `overview` |
| Skills | Skills tags | `skills` |
| Employment | Employment history | `work_experience[].description` |

Structural fields (company, position, dates) come from profile unchanged; only
descriptions are rewritten.

## Intelligence Format

Mirror feature 001/005 markdown structure:

- `## WhatToWrite` — content recommendations
- `## HowToBuildProfile` — structure recommendations (Upwork-specific section name)
- `## FreshnessAndLimitations`
- `## Sources` with backtick source ids

Parser reuses same bullet extraction as `resume_create.loader`.

## Profile Artifact (feature 006)

Expected path: `artifacts/upwork-profile/<slug>.yaml`

Key fields:
- `profile_title`, `overview`, `profile_link`
- `work_experience[]` with company, position, dates, description
- `skills` as string list (tags)

## Validation Rules

Facts that MUST NOT change after rewrite:
- work_experience companies, positions, dates
- skill tag names (normalized case-insensitive)

Fields that MAY change after rewrite:
- `overview`, `profile_title`, descriptions, skill ordering/casing

## Browser Selectors

Upwork DOM changes frequently. MVP uses `data-test` selectors with label fallbacks
documented in `contracts/upwork-form-mapping.md`. Agent should prefer accessibility
labels when selectors fail.

## Decisions

| Decision | Rationale |
|----------|-----------|
| Reuse `resume_profile.slug` | Consistent slug algorithm across features |
| Separate profile I/O in `loader.py` | Profile loading without separate upwork_profile package (006 pending) |
| English default tone | Upwork marketplace expectation |
| No auto-publish | Constitution + user trust |
