# Contract: Source Cache Format

**Feature**: 005-upwork-intelligence

## Purpose

Define browser-cached source files used when HTTP fetch returns 403.

## Path

`tmp/upwork-intelligence-sources/<source-id>.txt`

## Registry file names

| source-id | URL |
|-----------|-----|
| `upwork-help-proposals` | https://support.upwork.com/hc/en-us/articles/211062998-How-to-submit-a-proposal-on-Upwork |
| `upwork-beginners-guide` | https://www.upwork.com/resources/upwork-for-beginners |
| `upwork-profile-tips` | https://www.upwork.com/resources/freelancer-profile-tips |

## Content rules

- Plain UTF-8 text extracted from visible page body (Browser Tab / CDP `innerText`)
- No HTML required; HTML is normalized if passed through `ingest-text`
- Minimum useful length: 200 characters after normalization
- MUST NOT contain cookies, auth tokens, or private account data — article text only

## Ingest command

```bash
PYTHONPATH=src python3 -m upwork_intelligence.cli ingest-text \
  --source-id upwork-help-proposals \
  --input tmp/upwork-help-proposals-raw.txt
```

## Fetch priority at `run`

1. If `<sources-dir>/<source-id>.txt` exists and non-empty → `fetch_channel: browser_cache`
2. Else try HTTP fetch → `fetch_channel: http` (often `unavailable` / 403 on Upwork)
