---
name: "upwork-proposal"
description: "Apply to Upwork job with tailored proposal from upwork-profile YAML; compose proposal-plan and fill proposal form via Browser Tab."
compatibility: "Requires Browser Tab for upwork.com; Python package upwork_proposal; artifacts from feature 006"
metadata:
  author: "hh-cursor"
---

## User Input

```text
$ARGUMENTS
```

Apply to an Upwork job using:
- Job post URL from user
- `artifacts/upwork-profile/<slug>.yaml` (facts — feature 006)
- `artifacts/upwork-intelligence.md` (style — feature 005, optional)

Output: `artifacts/upwork-proposal/<job-slug>.yaml` proposal-plan + browser apply.

## Agent communication (mandatory)

The user sees questions and final summary, not a dev log.

**Forbidden in user-facing messages:**
- Announcing CLI/bootstrap steps, validation internals, browser/CDP mechanics
- Preambles before questions («сейчас загружу профиль»)

**Allowed:**
- `AskQuestion` prompts (job URL, profile choice, Connects confirmation)
- Blockers (login/captcha, missing artifacts, Uma video interview required)
- Short preview of proposal cover letter (first 2–3 sentences)
- Final message with artifact paths and manual Send reminder

## Workflow

### 0. Job URL

If `$ARGUMENTS` contains upwork.com job URL — use it. Otherwise `AskQuestion`:

- Prompt: «Paste the Upwork job post URL»
- Validate URL contains `upwork.com` and `/jobs/` or `/nx/jobs/`

### 1. Check prerequisites

```bash
PYTHONPATH=src python3 -m upwork_proposal.cli list-profiles
```

- If empty: tell user to run `/upwork-profile` first. **Stop.**
- If one profile: use it silently.
- If multiple: `AskQuestion` to pick profile (show `profile_title`).

```bash
PYTHONPATH=src python3 -m upwork_proposal.cli load-inputs --profile <profile-yaml>
```

- If `intelligence_available: false`: warn that proposal uses default rules; continue.

### 2. Extract job post

Follow `specs/007-upwork-proposal/contracts/job-extract-format.md`.

1. `browser_navigate` → job URL
2. Login/captcha → **stop**, user authenticates
3. Extract title, client, description, budget_type, skills, screening_questions
4. Write `tmp/upwork-job-extract.json`
5. If page requires Uma video interview instead of cover letter → **stop** with blocker

### 3. Write proposal draft

Read `specs/007-upwork-proposal/contracts/cover-letter-rules.md`.
Read profile YAML and `artifacts/upwork-intelligence.md` if available.

Write `tmp/upwork-proposal-draft.json`:

```json
{
  "cover_letter_text": "...",
  "language": "en",
  "screening_answers": [
    {"question": "...", "answer": "..."}
  ],
  "rewrite_applied": true,
  "intelligence_citations": ["upwork-help-proposals"]
}
```

**Quality goal:** lead with client's problem (not generic intro), 2–3 achievements from profile, job keywords, clear CTA. English by default.

Show user a short preview before browser apply.

### 4. Compose and validate

```bash
PYTHONPATH=src python3 -m upwork_proposal.cli compose \
  --profile <profile-yaml> \
  --job tmp/upwork-job-extract.json \
  --draft tmp/upwork-proposal-draft.json
```

```bash
PYTHONPATH=src python3 -m upwork_proposal.cli validate \
  --input artifacts/upwork-proposal/<job-slug>.yaml \
  --profile <profile-yaml>
```

```bash
PYTHONPATH=src python3 -m upwork_proposal.cli artifact-path \
  --job-url "<url>" --client "<client>" --title "<title>"
```

### 5. Browser apply

Follow `specs/007-upwork-proposal/contracts/browser-flow.md`.

1. `browser_navigate` → job URL
2. Login/captcha → **stop**
3. If already applied → **stop** with blocker
4. Click «Apply now»
5. Fill contract terms if prompted (use profile `hourly_rate` as default — confirm with user)
6. Paste `cover_letter.text` into proposal textarea
7. Fill screening question answers from proposal-plan
8. **Do not** click «Send» — user confirms Connects cost and submits manually

### 6. Write report

```bash
PYTHONPATH=src python3 -m upwork_proposal.cli write-report \
  --proposal-plan artifacts/upwork-proposal/<job-slug>.yaml \
  --sections tmp/upwork-proposal-sections.json
```

### 7. Final message

> Proposal form filled on Upwork (not submitted).
>
> Proposal plan: `artifacts/upwork-proposal/<job-slug>.yaml`
> Report: `artifacts/upwork-proposal/<job-slug>-report.yaml`
>
> Review the proposal and Connects cost in the browser, then click Send manually.

## Out of Scope

- Auto-submit proposal (Connects deduction)
- Profile editing for job fit (use `/upwork-profile-create`)
- Collecting profile data (use `/upwork-profile`)

## References

- Spec: `specs/007-upwork-proposal/spec.md`
- Proposal plan: `specs/007-upwork-proposal/contracts/proposal-plan-format.md`
- Browser flow: `specs/007-upwork-proposal/contracts/browser-flow.md`
- Cover letter rules: `specs/007-upwork-proposal/contracts/cover-letter-rules.md`
- Quickstart: `specs/007-upwork-proposal/quickstart.md`
