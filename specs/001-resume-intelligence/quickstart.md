# Quickstart: Resume Intelligence

## Purpose

Validate that the feature can fetch live sources and produce a reusable Markdown artifact.

## Prerequisites

- Python 3.11 or newer
- Internet access
- Repository checkout with the `src/` tree available

## Run

```bash
PYTHONPATH=src python3 -m resume_intelligence.cli
```

## Expected Outcome

- The command completes without requiring credentials.
- The repository contains `artifacts/resume-intelligence.md`.
- The artifact includes all required sections from the report contract.
- If some sources fail, the artifact still exists and lists degraded coverage.

## Validation Checks

1. Open `artifacts/resume-intelligence.md`.
2. Confirm the sections `Summary`, `HowHRAndATSProcessResumesNow`, `WhatToWrite`,
   `HowToBuildResume`, `SourceQualityAndConflicts`, `Sources`, and
   `FreshnessAndLimitations` are present.
3. Confirm at least one recommendation carries a confidence label and source reference.
4. Confirm missing or failed sources, if any, are surfaced in the limitations or conflict
   section.
