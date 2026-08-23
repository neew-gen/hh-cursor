---
name: "upwork-profile-create"
description: "Create or edit Upwork freelancer profile from upwork-intelligence guidance and upwork-profile YAML; compose fill-plan and fill form via Browser Tab."
compatibility: "Requires Browser Tab for upwork.com; Python package upwork_profile_create; artifacts from features 005 and 006"
metadata:
  author: "hh-cursor"
---

## User Input

```text
$ARGUMENTS
```

Create or update an Upwork profile using:
- `artifacts/upwork-intelligence.md` (how to write — feature 005)
- `artifacts/upwork-profile/<slug>.yaml` (facts — feature 006)

Output: `artifacts/upwork-profile-create/<slug>.yaml` fill-plan + browser fill.

## Agent communication (mandatory)

The user sees questions and final summary, not a dev log.

**Forbidden in user-facing messages:**
- Announcing CLI/bootstrap steps, validation internals, browser/CDP mechanics
- Preambles before questions («сейчас загружу профиль»)

**Allowed:**
- `AskQuestion` prompts (profile choice, fill mode, portfolio project pick)
- Blockers (login/captcha, missing artifacts)
- Optional short preview of rewritten `overview` before browser fill
- Final message with artifact paths and manual save reminder
- Per-section pause while waiting for the user to Save (unless they opted out)
- Portfolio consent: warn before GitHub/clone access; ask for links and which projects to parse

## Workflow

### 0. Check prerequisites

```bash
PYTHONPATH=src python3 -m upwork_profile_create.cli list-profiles
```

- If empty: tell user to run `/upwork-profile` first. **Stop.**
- If one profile: use it silently.
- If multiple: `AskQuestion` to pick profile (show `profile_title` from list).

Check intelligence:

```bash
PYTHONPATH=src python3 -m upwork_profile_create.cli load-inputs --profile <profile-yaml>
```

- If `intelligence_available: false`: warn that rewrite uses default rules; offer continue or run feature 005 first.

### 1. Q1 — Fill mode

`AskQuestion` only when profile has `profile_link`:

- Prompt: «Create a new Upwork profile section or edit your existing profile?»
- Options:
  - `create_new` — «Fill profile from scratch on Upwork»
  - `edit_existing` — «Edit existing profile» (default when `profile_link` present)

If no `profile_link`: use `create_new` without asking.

### 2. Rewrite texts

Read `artifacts/upwork-intelligence.md` sections `WhatToWriteInProposals` and `HowToBuildProfile`.
Follow `specs/008-upwork-profile-create/contracts/rewrite-rules.md`.

Rewrite **only**:
- `overview`
- `profile_title` (if intelligence suggests clearer title — facts only)
- each `work_experience[].description` (outcome statements for Uma matching;
  **≤ 500 chars** — rewrite to fit, never hard-truncate mid-sentence)
- `skills` tags (reorder/clarify only — no invented skills)

Do **not** rewrite `hourly_rate` — copy as-is from the profile YAML (USD number/string).

Build draft JSON at `tmp/upwork-fill-draft.json`:

```json
{
  "overview": "...",
  "profile_title": "...",
  "skills": ["JavaScript", "TypeScript"],
  "work_experience": [{"description": "..."}, ...],
  "rewrite_applied": {
    "overview": true,
    "profile_title": false,
    "work_experience_descriptions": true,
    "skills_tags": false
  },
  "intelligence_citations": ["upwork-help-proposals"]
}
```

`work_experience` array length MUST equal profile entry count.

### 3. Compose and validate fill-plan

```bash
PYTHONPATH=src python3 -m upwork_profile_create.cli compose \
  --profile <profile-yaml> \
  --draft tmp/upwork-fill-draft.json \
  --fill-mode create_new
```

Use `--fill-mode edit_existing` when user chose edit.

```bash
PYTHONPATH=src python3 -m upwork_profile_create.cli validate \
  --input artifacts/upwork-profile-create/<slug>.yaml \
  --profile <profile-yaml>
```

### 4. Browser fill (core sections)

Follow `specs/008-upwork-profile-create/contracts/browser-flow.md` and `upwork-form-mapping.md`.

```bash
PYTHONPATH=src python3 -m upwork_profile_create.cli form-mappings
```

1. `browser_navigate` → profile settings URL from fill-plan `target_url`
2. Login/captcha → **stop**, user authenticates
3. Fill sections in step order from fill-plan, including **`hourly_rate`**
4. Apply **Save policy** below
5. Then run **§4b Portfolio** (unless user skips)

Use `browser_lock` before multi-step fill; `browser_unlock` when waiting or done.

#### Save policy (mandatory)

**Default:** never click Save / Publish / Submit. After filling a section (or modal), stop, unlock the browser if needed, and wait until the user saves and says to continue.

**Exception:** click Save yourself only when the user **explicitly** says not to wait and to save (e.g. «сохраняй сам», «не жди», «save yourself», «don't wait»). Without that wording, always wait.

Still never auto-publish the whole profile unless the user explicitly asks for that too.

### 4b. Portfolio (mandatory step unless skipped)

Follow `specs/008-upwork-profile-create/contracts/portfolio-from-github.md`.

**First:** run `/project-portfolio-extract` (feature 009) if `artifacts/project-portfolio-extract/<slug>.yaml` do not exist yet.

**Then:** browser fill from 009 artifacts only — do not re-clone or re-compose inline.

#### 4b.1 Extract (feature 009)

If no portfolio artifacts:

> Запустите `/project-portfolio-extract` или дайте ссылки — сначала нужны артефакты с title/description/skills.

Offer profile `portfolio_links` as URL candidates for 009.

#### 4b.2 Project pick

Which 009 artifacts to publish on Upwork; stale projects only with user approval.

Ask keep / update / replace for existing Upwork portfolio cards.

#### 4b.3 Browser fill Portfolio

Follow `specs/008-upwork-profile-create/contracts/portfolio-from-github.md` (skills cap, draft save, thumbnail).

**Upwork limit:** max **5 skills** per portfolio card. If 009 artifact has more, trim to the most representative set (large project → 1–2 skills per sub-area, cap at 5). Example Castle Keepers: `TypeScript`, `Vue.js`, `Node.js`, `NestJS`, `UI/UX Design`.

1. Editor URL only: `https://www.upwork.com/freelancers/~<id>` (not `viewMode=1`)
2. Read `artifacts/project-portfolio-extract/<slug>.yaml`; skills from artifact `skills` only (not 009 `stack`); trim to ≤5 in `tmp/upwork-portfolio-draft.json`
3. **Add portfolio** → `title`, role, `description`, ≤5 `skills` (slow type → wait ~2s → `ArrowDown` → click `[role=option]`); web link via sub-dialog + native input events if **Add** stays disabled
4. **Save as draft** — mandatory; success = card under **Drafts** or dialog title «Edit portfolio project»; never navigate away with unsaved modal
5. Tell user to open the draft and **upload thumbnail image** (Publish blocked without it)
6. Repeat per approved artifact; do not Publish unless user explicitly asks

### 5. Write report

```bash
PYTHONPATH=src python3 -m upwork_profile_create.cli write-report \
  --fill-plan artifacts/upwork-profile-create/<slug>.yaml \
  --sections tmp/upwork-fill-sections.json
```

Include `portfolio` status when that step ran (`saved` / `skipped` / `pending_user_save`).

### 6. Final message

> Upwork profile filled (draft).
>
> Fill-plan: `artifacts/upwork-profile-create/<slug>.yaml`
> Report: `artifacts/upwork-profile-create/<slug>-report.yaml`
>
> Review each section in the browser and save manually (unless you asked the agent to save).

## Out of Scope

- Auto-publish profile (and auto-Save unless user explicitly requests it)
- Job-specific proposal tailoring (use `/upwork-proposal`)
- Collecting profile data (use `/upwork-profile`)
- Scraping GitHub without `/project-portfolio-extract` (use feature 009)
- Inventing portfolio projects or screenshots

## References

- Spec: `specs/008-upwork-profile-create/spec.md`
- Fill plan: `specs/008-upwork-profile-create/contracts/fill-plan-format.md`
- Browser flow: `specs/008-upwork-profile-create/contracts/browser-flow.md`
- Portfolio from GitHub: `specs/008-upwork-profile-create/contracts/portfolio-from-github.md`
- Project extract (009): `/project-portfolio-extract` → `specs/009-project-portfolio-extract/`
- Quickstart: `specs/008-upwork-profile-create/quickstart.md`
