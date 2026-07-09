---
name: "resume-intelligence"
description: "Fetch current HR/ATS resume guidance from the web and write artifacts/resume-intelligence.md. Optional; used by resume-create and job-apply."
compatibility: "Requires internet access; Python package resume_intelligence"
metadata:
  author: "hh-cursor"
---

## User Input

```text
$ARGUMENTS
```

Collect up-to-date signals about how HR and ATS process resumes, what to write, and how to structure them.
Output: `artifacts/resume-intelligence.md`.

Optional step — skip if the artifact already exists and is fresh enough for the user.

## Agent communication (mandatory)

The user sees a short result summary, not a dev log.

**Forbidden in user-facing messages:**
- Announcing fetch/registry/synthesis internals step by step
- Preambles before running («сейчас запущу CLI»)

**Allowed:**
- Blockers (no internet, all sources failed, SSL errors — point to README troubleshooting)
- Final message with artifact path and brief coverage note (e.g. sources ok/failed)

## Workflow

### 1. Run pipeline

```bash
PYTHONPATH=src python3 -m resume_intelligence.cli
```

Optional flags from `$ARGUMENTS` when user asks:
- `--output <path>` — custom artifact path
- `--max-sources N` — limit fetched sources
- `--timeout N` — per-source timeout in seconds

### 2. Validate artifact

Open `artifacts/resume-intelligence.md` and confirm required sections per
`specs/001-resume-intelligence/contracts/report-format.md`:
`Summary`, `HowHRAndATSProcessResumesNow`, `WhatToWrite`, `HowToBuildResume`,
`SourceQualityAndConflicts`, `Sources`, `FreshnessAndLimitations`.

If some sources failed, the artifact must still exist and list degraded coverage.

### 3. Report to user

Reply with artifact path and one-line coverage summary. No need to paste the full report.

## Out of scope

- Collecting user profile data (use `/resume-profile`)
- Creating or editing hh.ru resume (use `/resume-create`)
- Applying to vacancies (use `/job-apply`)
