# Contract: CLI Input

## Purpose

Define the local invocation contract for running Resume Intelligence.

## Expected Invocation

```bash
python3 -m resume_intelligence.cli [options]
```

## Inputs

- `--output PATH`
  - Optional
  - Default: `artifacts/resume-intelligence.md`
  - Defines the final artifact path

- `--max-sources N`
  - Optional
  - Default: use all configured sources
  - Limits how many configured sources are fetched during a run

- `--timeout SECONDS`
  - Optional
  - Default: implementation-defined safe timeout
  - Defines per-source fetch timeout

## Behavior

- The command MUST attempt to fetch configured live sources.
- The command MUST continue on partial failures.
- The command MUST create the final Markdown artifact even when some sources fail.
- The command MUST exit non-zero only when it cannot produce any final artifact.
