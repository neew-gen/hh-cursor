<!--
Sync Impact Report
Version change: 1.0.0 -> 1.1.0
Modified principles:
- I. Browser-First Evidence Collection — extended to target platforms (hh.ru, upwork.com)
Added sections:
- None
Removed sections:
- None
Templates requiring updates:
- ✅ runtime docs aligned in feature work: README.md, .cursor/rules/spec-kit.mdc
Deferred follow-up TODOs:
- None
-->
# hh-cursor Constitution

## Core Principles

### I. Browser-First Evidence Collection
All workflows that require interaction with a target platform (`hh.ru`, `upwork.com`, or
future platforms added via SDD) MUST prefer Browser Tab or the project's browser-capable
automation path over unofficial APIs or hidden browser state. Plans MUST document the exact
UI path per platform, expected manual checkpoints, and explicit stop conditions for login,
captcha, paywalls, Connects confirmation, KYC, or permission prompts. This keeps the
project aligned with the observable user experience and reduces brittle hidden integrations.

### II. Minimal Scope, Maximum Traceability
Every feature MUST start with the smallest independently valuable slice and MUST preserve
traceability from user need to output artifact. Specs define only what and why, plans
define how, and tasks define exact file-level execution. Unrelated code or process changes
MUST NOT be bundled into the same feature. This protects the repository from speculative
growth and keeps reviewable diffs small.

### III. Source Trust Ranking
Any feature that synthesizes hiring guidance, resume advice, or market claims MUST classify
sources by trust tier and MUST keep citations attached to derived recommendations.
Primary evidence includes official platform rules/help (`hh`, Upwork Help), first-party
vendor documentation, and academic research. Secondary evidence includes career media,
recruiter interviews, and market reviews. Heuristic evidence includes SEO-style
aggregators, resume checkers, and other low-accountability advice sources. Contradictions
across tiers MUST be surfaced, never silently flattened.

### IV. Reusable Artifact Output
Features that generate guidance for later agent steps MUST produce stable, reusable
artifacts rather than only ephemeral chat output. Final user-facing artifacts MUST live in
`artifacts/` and MUST use a deterministic structure that is readable by both humans and
Cursor. When a feature emits recommendations, the artifact MUST clearly separate confirmed
findings, heuristics, conflicts, freshness, and limitations.

### V. Secret-Safe Automation
Secrets, cookies, tokens, login exports, and personal credentials MUST NOT be committed to
the repository. Sensitive runtime state MUST stay in local ignored files, environment
variables, or interactive browser sessions. Features MUST degrade safely when external
access is unavailable and MUST never require storing private session material in repo
artifacts.

## Operational Constraints

- `README.md` MUST document how to run each shipped user-facing workflow and where its
  resulting artifacts are written.
- Tests SHOULD be added when they materially reduce regression risk; tests MUST NOT contain
  comments inside the test bodies.
- Any artifact that claims current-market relevance SHOULD record freshness or run date.
- Generated recommendations MUST distinguish evidence-backed advice from inferred heuristics.
- If browser automation encounters login, captcha, or another manual gate, the workflow
  MUST pause and expose that stop point instead of attempting repeated opaque retries.

## Delivery Workflow

- Non-trivial work MUST follow the Spec Kit sequence:
  `constitution -> specify -> plan -> tasks -> implement`.
- `spec.md` MUST stay technology-agnostic and use prioritized, independently testable user
  stories with `FR-*` and `SC-*` identifiers.
- `plan.md` MUST include a constitution check, technical context, project structure, and
  any browser stop points or trust-model decisions relevant to the feature.
- `tasks.md` MUST use task IDs, exact file paths, and story grouping so MVP delivery can
  stop after the first independently valuable story.
- Implementation MUST follow approved tasks; if requirements change, the spec MUST be
  updated before code changes continue.

## Governance

This constitution overrides informal local habits for this repository. Every feature plan,
task list, and implementation review MUST verify compliance with these principles.

Amendment policy:
- Amendments MUST be documented in `constitution.md`.
- MAJOR version bumps are required for incompatible principle changes or removals.
- MINOR version bumps are required for new principles or materially expanded governance.
- PATCH version bumps are required for wording-only clarifications.

Compliance policy:
- Before implementation, reviewers MUST confirm that spec, plan, and tasks align with this
  constitution.
- Any justified exception MUST be documented in the feature's `plan.md` under constitution
  or complexity tracking.
- If a feature cannot satisfy a principle, the blocking reason and mitigation MUST be
  explicit in the feature artifacts.

**Version**: 1.1.0 | **Ratified**: 2026-07-07 | **Last Amended**: 2026-08-22
