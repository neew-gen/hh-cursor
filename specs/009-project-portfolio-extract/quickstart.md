# Quickstart: Project Portfolio Extract

## Prerequisites

- Python 3.11+
- `git` on PATH (for public GitHub URLs)
- `PYTHONPATH=src`

## Extract from GitHub URL

```bash
PYTHONPATH=src python3 -m project_portfolio_extract.cli extract-from-url \
  --url https://github.com/example/vue-use-api-call \
  --output tmp/project-facts.json
```

## Extract from local folder

```bash
PYTHONPATH=src python3 -m project_portfolio_extract.cli extract-from-path \
  --path /path/to/project \
  --repo-url https://github.com/owner/repo \
  --output tmp/project-facts.json
```

## Unpack ZIP (fallback)

```bash
PYTHONPATH=src python3 -m project_portfolio_extract.cli unpack \
  --zip ~/Downloads/project.zip \
  --slug my-project

PYTHONPATH=src python3 -m project_portfolio_extract.cli extract-from-path \
  --path tmp/project-unpacks/my-project \
  --output tmp/project-facts.json
```

## Compose portfolio skeleton (CLI heuristics)

```bash
PYTHONPATH=src python3 -m project_portfolio_extract.cli compose-portfolio \
  --facts tmp/project-facts.json \
  --output tmp/portfolio-draft.json
```

Agent edits `description` in draft, then:

```bash
PYTHONPATH=src python3 -m project_portfolio_extract.cli write-artifact \
  --input tmp/portfolio-final.json \
  --project-slug vue-use-api-call
```

Output: `artifacts/project-portfolio-extract/vue-use-api-call.yaml`

## Slash skill

Run `/project-portfolio-extract` in Cursor — consent, URLs, project pick, artifact write.

## Downstream

Use artifacts with `/upwork-profile-create` portfolio fill (feature 008).
