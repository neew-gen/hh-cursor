# Contract: Source Adapter

## Purpose

Define behavior for collecting Upwork source text into `SourceFetchResult`.

## Adapters (priority order)

### 1. Browser cache adapter (primary)

**Input**:
- `SourceDescriptor`
- Cached file `tmp/upwork-intelligence-sources/<source-id>.txt`

**Output**: `SourceFetchResult` with `status: ok`, `fetch_channel: browser_cache`

Populated by skill workflow + `ingest-text` CLI (see `browser-flow.md`).

### 2. HTTP adapter (fallback)

**Input**:
- `SourceDescriptor`
- Timeout value

**Output**: `SourceFetchResult` with `fetch_channel: http`

**Note**: Upwork domains often return HTTP 403; do not rely on this adapter alone.

## Required Guarantees

- Preserve originating source identifier.
- Return status `ok`, `unavailable`, or `empty`.
- Surface failures as data instead of crashing the run.
- Do not write cookies, tokens, or private session data to repo files.
- HTTP adapter uses `User-Agent: hh-cursor-upwork-intelligence/1.0`.

## Registry IDs

- `upwork-help-proposals`
- `upwork-beginners-guide`
- `upwork-profile-tips`

## CLI

- `list-sources` — registry + cache paths
- `ingest-text --source-id ID --input PATH` — write cache file
- `run --sources-dir DIR` — synthesize artifact (cache first, then HTTP)

## Non-Goals

- Authenticated Upwork sessions in repo
- Auto-navigation without Browser Tab skill orchestration
