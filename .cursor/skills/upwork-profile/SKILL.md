---
name: "upwork-profile"
description: "Collect Upwork freelancer profile data via optional profile link and gap questionnaire; write artifacts/upwork-profile/<profile-title-slug>.yaml. Does not use upwork-intelligence."
compatibility: "Requires Browser Tab for Upwork link extract; Python package upwork_profile"
metadata:
  author: "hh-cursor"
---

## User Input

```text
$ARGUMENTS
```

Collect user profile data for filling an Upwork profile on the next step (feature 008).
**Do not read** `artifacts/upwork-intelligence.md` or feature 005 artifacts.

Artifacts directory: `artifacts/upwork-profile/` (gitignored). Filename slug = transliterated `profile_title`, e.g. `Frontend Developer` → `frontend-developer.yaml`.

## Agent communication (mandatory)

The user sees a questionnaire, not a dev log. **Never narrate internal work in chat.**

**Forbidden in user-facing messages:**
- Announcing bootstrap, init-draft, CLI, artifact checks, gap detection, validation, browser/CDP steps
- Preambles before a question («сейчас задам вопрос»)

**Allowed user-facing text:**
- `AskQuestion` prompts only (Q1, gap questions) — **no extra chat text in the same turn**
- Blockers (login/captcha on Upwork, invalid profile URL)
- Final confirmation with artifact path after `write`

**Turn shape:** run tools internally → one `AskQuestion` (or blocker / final path).

## Workflow

### 0. Initialize new draft

```bash
PYTHONPATH=src python3 -m upwork_profile.cli init-draft \
  --output tmp/upwork-profile-draft.json
```

After draft initialization, show Q1 in the same turn with **no** intervening chat text.

### 1. Q1 — Profile link (optional)

Ask Q1 **only via `AskQuestion`**.

- Title: `Upwork profile`
- Prompt: `Paste a link to your Upwork freelancer profile (upwork.com/freelancers/...).`
- Options:
  - `provide_link` — `Enter my Upwork profile link`
  - `skip_link` — `Skip and answer questions instead`

If URL provided:

1. Validate with `PYTHONPATH=src python3 -c "from upwork_profile.extractor import is_valid_upwork_profile_link; print(is_valid_upwork_profile_link('URL'))"`
2. Browser Tab: `browser_navigate` to URL
3. If login/captcha → **stop**, ask user to authenticate
4. Extract page text via `browser_snapshot` or CDP; save to `tmp/upwork-profile-page.txt`
5. Run extract CLI:
   ```bash
   PYTHONPATH=src python3 -m upwork_profile.cli extract-text \
     --input tmp/upwork-profile-page.txt \
     --output tmp/upwork-profile-draft.json \
     --profile-link "URL"
   ```

If Skip: keep draft from step 0; continue to gap questions.

### 2. Gap questionnaire loop

Repeat until `validate` reports `"complete": true`:

```bash
PYTHONPATH=src python3 -m upwork_profile.cli gaps --input tmp/upwork-profile-draft.json
PYTHONPATH=src python3 -m upwork_profile.cli validate --input tmp/upwork-profile-draft.json
```

For each gap, ask **one question** at a time via `AskQuestion`. Store answers in English in the artifact (user may answer in Russian in chat — translate facts only, do not invent).

| field_id | JSON path |
|----------|-----------|
| profile_title | `profile_title` |
| overview | `overview` |
| hourly_rate | `hourly_rate` |
| skills | append to `skills[]` |
| work_experience_status | `work_experience_status` |
| work_experience | append to `work_experience[]` |
| education | append to `education[]` |
| portfolio_links | append to `portfolio_links[]` |

### 3. Validate and write artifact

```bash
PYTHONPATH=src python3 -m upwork_profile.cli artifact-path --profile-title "Frontend Developer"
PYTHONPATH=src python3 -m upwork_profile.cli validate --input tmp/upwork-profile-draft.json
PYTHONPATH=src python3 -m upwork_profile.cli write --input tmp/upwork-profile-draft.json
```

If slug exists, write `<slug> (2).yaml`, etc.

Final message example:

> Upwork profile data is ready.
>
> Saved to `artifacts/upwork-profile/<slug>.yaml`.
>
> Profile title: **<profile_title>**. Use this file with `/upwork-profile-create` or `/upwork-proposal`.

## Out of Scope

- upwork-intelligence / proposal advice
- Job post URL collection
- Publishing profile on Upwork (feature 008)

## References

- Spec: `specs/006-upwork-profile/spec.md`
- Profile format: `specs/006-upwork-profile/contracts/profile-format.md`
- Questionnaire: `specs/006-upwork-profile/contracts/questionnaire-flow.md`
- Quickstart: `specs/006-upwork-profile/quickstart.md`
