# Contract: Source Acquire Flow

Internal workflow — not the user-facing purpose of the feature.

## Consent (mandatory)

Before acquire:

1. Tell user the agent will clone GitHub and/or read ZIP/local files.
2. Wait for URLs or paths (and project selection when multiple).

## Acquire paths

| Input | Action | Output path |
|-------|--------|-------------|
| Public GitHub URL | `git clone --depth 1 <url> tmp/github-clones/{owner}-{repo}` | local tree |
| ZIP file | unzip to `tmp/project-unpacks/{slug}/` | local tree |
| Local directory | validate exists, use as-is | same path |

## Failure handling

| Error | Agent action |
|-------|--------------|
| `git clone` 403 / private | Ask user for GitHub ZIP (Code → Download ZIP) or local folder |
| Invalid URL | Report error; ask for corrected URL or ZIP |
| Missing ZIP | Ask user to provide file path |
| No git binary | Ask user for ZIP or local path only |

## Idempotency

- Re-clone: remove existing target dir or `git pull` if same remote
- Shallow clone only — no full history

## Security

- No credentials in repo
- Temp paths under `tmp/` only
- Do not commit acquired trees
