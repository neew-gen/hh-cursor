---
name: "project-portfolio-extract"
description: "Extract portfolio-ready project title, description, skills, and URL from GitHub link, ZIP, or local folder; write artifacts/project-portfolio-extract/<slug>.yaml."
compatibility: "Requires Python package project_portfolio_extract; optional git for public GitHub URLs"
metadata:
  author: "hh-cursor"
---

## User Input

```text
$ARGUMENTS
```

Extract **portfolio-ready text** from a project source — not tied to hh.ru or Upwork.

Output: `artifacts/project-portfolio-extract/<project-slug>.yaml` with `title`, `description`, `project_url`, `skills`.

## Agent communication (mandatory)

The user sees questions and final summary, not a dev log.

**Forbidden in user-facing messages:**
- Announcing CLI internals step by step
- Preambles before consent («сейчас клонирую»)

**Allowed:**
- Consent + request for URLs / ZIP / local path
- `AskQuestion` for project selection (multi-URL, stale projects)
- Optional preview of portfolio text before write
- Final message with artifact paths

## Workflow

### 0. Consent and input

Tell the user clearly:

> Пришлите ссылку на проект (GitHub) — я составлю **title и description для portfolio**.
> Для этого мне нужно прочитать код: shallow clone, или ваш ZIP / локальная папка, если repo закрыт.

Collect:
- One or more GitHub URLs, and/or
- Path to ZIP archive, and/or
- Path to local project folder

Offer skip if user only wanted info.

### 1. Acquire source (internal)

Follow `specs/009-project-portfolio-extract/contracts/source-acquire-flow.md`.

```bash
PYTHONPATH=src python3 -m project_portfolio_extract.cli extract-from-url \
  --url <github-url> \
  --output tmp/project-facts-<slug>.json
```

On failure (private / 403 / no git):

> Скачайте ZIP на GitHub (Code → Download ZIP) или укажите локальный путь к проекту.

```bash
PYTHONPATH=src python3 -m project_portfolio_extract.cli unpack \
  --zip <path> --slug <slug>

PYTHONPATH=src python3 -m project_portfolio_extract.cli extract-from-path \
  --path tmp/project-unpacks/<slug> \
  --source-type zip_upload \
  --output tmp/project-facts-<slug>.json
```

Local folder:

```bash
PYTHONPATH=src python3 -m project_portfolio_extract.cli extract-from-path \
  --path <local-dir> \
  --repo-url <optional-url> \
  --output tmp/project-facts-<slug>.json
```

### 2. Stale filter + project pick

If facts JSON has `"stale": true`, flag for user and **do not write artifact** unless they approve.

Multiple URLs: `AskQuestion` — which projects to include.

### 3. Compose portfolio text

```bash
PYTHONPATH=src python3 -m project_portfolio_extract.cli compose-portfolio \
  --facts tmp/project-facts-<slug>.json \
  --output tmp/portfolio-draft-<slug>.json
```

Agent **must** review and polish `description` per
`specs/009-project-portfolio-extract/contracts/portfolio-compose-rules.md` (English, facts-only).

Optional: show preview to user before write.

Save polished draft to `tmp/portfolio-final-<slug>.json`.

### 4. Write artifact

```bash
PYTHONPATH=src python3 -m project_portfolio_extract.cli write-artifact \
  --facts tmp/project-facts-<slug>.json \
  --draft tmp/portfolio-final-<slug>.json \
  --project-slug <slug> \
  --approved-by-user true
```

Repeat per approved project.

### 5. Final message

> Portfolio texts ready.
>
> Artifacts: `artifacts/project-portfolio-extract/<slug>.yaml`
>
> Paste into Upwork Portfolio manually, or run `/upwork-profile-create` to fill the form.

## Out of Scope

- Upwork browser fill (use `/upwork-profile-create`)
- GitHub API / private repo auth
- Thumbnail/screenshot generation
- Inventing metrics or clients

## References

- Spec: `specs/009-project-portfolio-extract/spec.md`
- Artifact: `specs/009-project-portfolio-extract/contracts/portfolio-artifact-format.md`
- Compose rules: `specs/009-project-portfolio-extract/contracts/portfolio-compose-rules.md`
- Quickstart: `specs/009-project-portfolio-extract/quickstart.md`
