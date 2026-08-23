# Quickstart: Upwork Intelligence

## Purpose

Validate browser-first source collection and artifact generation.

## Prerequisites

- Python 3.11 or newer
- Cursor Browser Tab enabled
- Repository checkout with the `src/` tree available

## Step 1 — List sources

```bash
PYTHONPATH=src python3 -m upwork_intelligence.cli list-sources
```

## Step 2 — Browser extract (agent or manual)

For each source URL, open in Browser Tab, copy/extract visible article text to
`tmp/<source-id>-raw.txt`, then ingest:

```bash
PYTHONPATH=src python3 -m upwork_intelligence.cli ingest-text \
  --source-id upwork-help-proposals \
  --input tmp/upwork-help-proposals-raw.txt
```

Repeat for `upwork-beginners-guide` and `upwork-profile-tips`.

See `contracts/browser-flow.md` for CDP extract steps.

## Step 3 — Run synthesis

```bash
PYTHONPATH=src python3 -m upwork_intelligence.cli run \
  --sources-dir tmp/upwork-intelligence-sources
```

## Expected Outcome

- `artifacts/upwork-intelligence.md` exists with all required sections.
- `Sources` lists `browser_cache` channel for cached files.
- If cache missing, HTTP fallback may return 403 — artifact still created with limitations.

## Validation Checks

1. Open `artifacts/upwork-intelligence.md`.
2. Confirm sections per `contracts/report-format.md`.
3. Confirm recommendations include confidence labels and source references when cache ok.
4. Confirm `FreshnessAndLimitations` mentions browser cache when HTTP blocked.

## Debug (HTTP only — expect 403)

```bash
PYTHONPATH=src python3 -m upwork_intelligence.cli run --http-only
```
