# Contract: Browser Flow — Upwork Intelligence

**Feature**: 005-upwork-intelligence

## Why Browser Tab

Upwork Help (`support.upwork.com`) and Resources (`upwork.com/resources/...`) return
**HTTP 403** to direct `urllib` fetch. Browser Tab is the primary evidence path for live
source text.

## Cache Directory

- Default: `tmp/upwork-intelligence-sources/`
- One file per registry source: `<source-id>.txt` (plain text, UTF-8)
- Gitignored via `tmp/` — never commit cached pages or cookies

## Extract Sources (per registry entry)

1. `browser_navigate` → source URL from `list-sources`
2. If login/captcha wall → **STOP**, ask user to authenticate manually, then continue
3. Extract readable page text:
   - Preferred: `browser_cdp` → `Runtime.evaluate` with
     `document.body?.innerText || ''`
   - Fallback: `browser_snapshot` and concatenate `name` fields from article body nodes
4. Write raw extract to `tmp/<source-id>-raw.txt`
5. Ingest into cache:

```bash
PYTHONPATH=src python3 -m upwork_intelligence.cli ingest-text \
  --source-id <source-id> \
  --input tmp/<source-id>-raw.txt
```

6. Repeat for all registry sources before synthesis

## Compose Artifact

```bash
PYTHONPATH=src python3 -m upwork_intelligence.cli run \
  --sources-dir tmp/upwork-intelligence-sources
```

`run` is also the default when invoking `python3 -m upwork_intelligence.cli` with flags only.

## Lock Workflow

```
browser_lock → navigate/extract each source → ingest-text → browser_unlock → cli run
```

If a browser tab already exists: `browser_lock` first.

## Stop Conditions

| Condition | Action |
|-----------|--------|
| Login wall | Pause; user logs in; resume |
| Captcha | Pause; user solves; resume |
| Page moved / 404 | Mark source unavailable; continue other sources |
| Empty extract | Retry snapshot once; if still empty → blocker for that source |
| All sources failed | Still run `cli run` — artifact with fallback + limitations |

## HTTP Fallback (optional)

```bash
PYTHONPATH=src python3 -m upwork_intelligence.cli run --http-only
```

Use only for debugging. Expect 403 on Upwork domains in most environments.

## Final User Message

After successful run with cached sources:

> Upwork intelligence готов: `artifacts/upwork-intelligence.md` (N/N sources из Browser Tab cache).
