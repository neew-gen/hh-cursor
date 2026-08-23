# Contract: Extract Format

JSON output from CLI `extract-from-url` / `extract-from-path`.

## Schema

```json
{
  "name": "vue-use-api-call",
  "summary": "Vue composable for API calls",
  "readme_excerpt": "First paragraphs from README...",
  "dependencies": ["vue"],
  "dev_dependencies": ["vitest", "typescript"],
  "stack": ["Vue 3", "Vitest", "TypeScript"],
  "languages_hint": ["TypeScript"],
  "last_commit_date": "2025-03-15",
  "last_commit_sha": "abc1234",
  "repo_url": "https://github.com/example/vue-use-api-call",
  "local_path": "tmp/github-clones/example-vue-use-api-call",
  "source_type": "github_url"
}
```

## Field sources

| Field | Source priority |
|-------|-----------------|
| `name` | README H1 → package.json name → folder name |
| `summary` | package.json description → first README sentence |
| `readme_excerpt` | README body after H1, skip badges-only lines |
| `dependencies` | package.json / pyproject.toml |
| `stack` | mapped deps + manifest keywords |
| `languages_hint` | file extensions in tree (cap sample) |
| `last_commit_*` | `git log -1` when `.git` present |
| `repo_url` | from clone URL or `--repo-url` flag |
| `source_type` | acquire method |

## Stale detection

If `last_commit_date` is more than ~730 days before run date, CLI adds:

```json
"stale": true,
"stale_reason": "last commit older than 2 years"
```

Agent must confirm with user before writing artifact.
