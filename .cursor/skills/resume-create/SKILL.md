---
name: "resume-create"
description: "Create or edit hh.ru resume from resume-intelligence guidance and resume-profile YAML; compose fill-plan and fill form via Browser Tab."
compatibility: "Requires Browser Tab for hh.ru; Python package resume_create; artifacts from features 001 and 002"
metadata:
  author: "hh-cursor"
---

## User Input

```text
$ARGUMENTS
```

Create or update an hh.ru resume using:
- `artifacts/resume-intelligence.md` (how to write — feature 001)
- `artifacts/resume-profile/<slug>.yaml` (facts — feature 002)

Output: `artifacts/resume-create/<slug>.yaml` fill-plan + browser fill.

## Agent communication (mandatory)

The user sees questions and final summary, not a dev log.

**Forbidden in user-facing messages:**
- Announcing CLI/bootstrap steps, validation internals, browser/CDP mechanics
- Preambles before questions («сейчас загружу профиль»)

**Allowed:**
- `AskQuestion` prompts (profile choice, fill mode)
- Blockers (login/captcha, missing artifacts)
- Optional short preview of rewritten `about_me` before browser fill
- Final message with artifact paths and manual publish reminder

**Turn shape:** run tools internally → one `AskQuestion` or blocker or final summary.

## Workflow

### 0. Check prerequisites

```bash
PYTHONPATH=src python3 -m resume_create.cli list-profiles
```

- If empty: tell user to run `/resume-profile` first. **Stop.**
- If one profile: use it silently.
- If multiple: `AskQuestion` to pick profile (show `target_role` from list).

Check intelligence:

```bash
PYTHONPATH=src python3 -m resume_create.cli load-inputs --profile <profile-yaml>
```

- If `intelligence_available: false`: warn that rewrite uses default rules; offer continue or run feature 001 first.

### 1. Q1 — Fill mode

`AskQuestion` only when profile has `resume_link`:

- Prompt: «Создать новое резюме или отредактировать существующее на hh.ru?»
- Options:
  - `create_new` — «Создать новое резюме»
  - `edit_existing` — «Редактировать существующее» (default when `resume_link` present)

If no `resume_link`: use `create_new` without asking.

### 2. Rewrite texts

Read `artifacts/resume-intelligence.md` sections `WhatToWrite` and `HowToBuildResume`.
Follow `specs/003-resume-create/contracts/rewrite-rules.md`.

Rewrite **only**:
- `about_me`
- each `work_experience[].description`

**Constraints:**
- Same companies, positions, dates, skill names as profile
- Do not invent metrics, skills, or employers
- Preserve URLs from original `about_me`

Build draft JSON at `tmp/fill-draft.json`:

```json
{
  "about_me": "...",
  "work_experience": [{"description": "..."}, ...],
  "rewrite_applied": {
    "about_me": true,
    "work_experience_descriptions": true
  },
  "intelligence_citations": ["hh-knowledge-create-resume"]
}
```

`work_experience` array length MUST equal profile entry count.

### 3. Compose and validate fill-plan

```bash
PYTHONPATH=src python3 -m resume_create.cli compose \
  --profile <profile-yaml> \
  --draft tmp/fill-draft.json \
  --fill-mode create_new
```

Use `--fill-mode edit_existing` when user chose edit.

If compose fails validation: fix draft (no new facts) and retry.

Resolve path:

```bash
PYTHONPATH=src python3 -m resume_create.cli artifact-path --target-role "<target_role>"
```

### 4. Browser fill

Follow `specs/003-resume-create/contracts/browser-flow.md` and `hh-form-mapping.md`.

```bash
PYTHONPATH=src python3 -m resume_create.cli form-mappings
```

**Create new:**
1. `browser_navigate` → `https://hh.ru/applicant/resumes`
2. Login/captcha → **stop**, user authenticates
3. Click «Создать резюме»
4. Fill sections in step order from fill-plan
5. Optional: save draft — **do not publish**

**Edit existing:**
1. `browser_navigate` → `target_url` from fill-plan
2. Login/captcha → **stop**
3. Click «Редактировать»
4. Update sections from fill-plan

Use `browser_lock` before multi-step fill; `browser_unlock` when done.

Map skill levels: basic → Базовый, medium → Средний, advanced → Продвинутый.

### 5. Write report

Save section statuses to `tmp/fill-sections.json`:

```json
[
  {"section_id": "target_role", "status": "filled", "notes": ""},
  {"section_id": "skills.hard", "status": "filled", "notes": ""}
]
```

```bash
PYTHONPATH=src python3 -m resume_create.cli write-report \
  --fill-plan artifacts/resume-create/<slug>.yaml \
  --sections tmp/fill-sections.json
```

### 6. Final message

> Резюме заполнено на hh.ru (черновик).
>
> Fill-plan: `artifacts/resume-create/<slug>.yaml`
> Отчёт: `artifacts/resume-create/<slug>-report.yaml`
>
> Проверьте форму в браузере и опубликуйте вручную.

## Out of Scope

- Auto-publish resume
- Vacancy-specific tailoring
- Re-running resume-intelligence inside this skill
- Collecting profile data (use `/resume-profile`)

## References

- Spec: `specs/003-resume-create/spec.md`
- Fill plan: `specs/003-resume-create/contracts/fill-plan-format.md`
- Browser flow: `specs/003-resume-create/contracts/browser-flow.md`
- Rewrite rules: `specs/003-resume-create/contracts/rewrite-rules.md`
- Quickstart: `specs/003-resume-create/quickstart.md`
