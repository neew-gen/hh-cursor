---
name: "upwork-intelligence"
description: "Fetch current Upwork proposal and profile guidance via Browser Tab cache and write artifacts/upwork-intelligence.md. Optional; used by upwork-profile-create and upwork-proposal."
compatibility: "Requires Browser Tab for Upwork source fetch; Python package upwork_intelligence"
metadata:
  author: "hh-cursor"
---

## User Input

```text
$ARGUMENTS
```

Collect up-to-date signals about how clients review Upwork proposals, what to write in cover letters, and how to structure freelancer profiles (including proposal–profile synergy).
Output: `artifacts/upwork-intelligence.md`.

Optional step — skip if the artifact already exists and is fresh enough for the user.

## Agent communication (mandatory)

The user sees a short result summary, not a dev log.

**Forbidden in user-facing messages:**
- Announcing fetch/registry/synthesis internals step by step
- Preambles before running («сейчас запущу CLI»)

**Allowed:**
- Blockers (login/captcha on Upwork, empty extract, all sources failed)
- Final message with artifact path and coverage note (e.g. `3/3 sources from browser cache`)

## Workflow

Upwork blocks direct HTTP fetch (403). **Browser Tab is mandatory** for live sources.

### 0. List sources (internal)

```bash
PYTHONPATH=src python3 -m upwork_intelligence.cli list-sources
```

### 1. Browser extract → cache (each source)

Follow `specs/005-upwork-intelligence/contracts/browser-flow.md`.

For **each** registry entry:

1. `browser_lock` (if not already locked)
2. `browser_navigate` → source `url`
3. Login/captcha → **stop**, user authenticates, then continue
4. Extract page text via `browser_cdp` → `Runtime.evaluate`:
   - expression: `document.body?.innerText || ''`
   - save to `tmp/<source-id>-raw.txt`
5. Ingest:

```bash
PYTHONPATH=src python3 -m upwork_intelligence.cli ingest-text \
  --source-id <source-id> \
  --input tmp/<source-id>-raw.txt
```

6. `browser_unlock` when all sources cached

Registry ids: `upwork-help-proposals`, `upwork-beginners-guide`, `upwork-profile-tips`.

### 2. Synthesize artifact

```bash
PYTHONPATH=src python3 -m upwork_intelligence.cli run \
  --sources-dir tmp/upwork-intelligence-sources
```

Optional flags from `$ARGUMENTS`:
- `--output <path>`
- `--max-sources N`
- `--timeout N` (HTTP fallback only; not used when cache hits)

Do **not** use `--http-only` unless user explicitly asks to test HTTP fallback.

### 3. Validate artifact

Open `artifacts/upwork-intelligence.md` and confirm required sections per
`specs/005-upwork-intelligence/contracts/report-format.md`:
`Summary`, `HowClientsReviewProposalsNow`, `WhatToWriteInProposals`, `HowToBuildProfile`,
`SourceQualityAndConflicts`, `Sources`, `FreshnessAndLimitations`.

`Sources` section MUST show `browser_cache` channel when cache was used.

If some sources failed, the artifact must still exist and list degraded coverage.

### 4. Report to user

Reply with artifact path and one-line coverage summary (e.g. `3/3 sources from browser cache`).

## Out of scope

- Collecting user profile data (use `/upwork-profile`)
- Creating or editing Upwork profile (use `/upwork-profile-create`)
- Submitting proposals (use `/upwork-proposal`)

## References

- Spec: `specs/005-upwork-intelligence/spec.md`
- Browser flow: `specs/005-upwork-intelligence/contracts/browser-flow.md`
- Source cache: `specs/005-upwork-intelligence/contracts/source-cache-format.md`
- Report format: `specs/005-upwork-intelligence/contracts/report-format.md`
- Quickstart: `specs/005-upwork-intelligence/quickstart.md`
