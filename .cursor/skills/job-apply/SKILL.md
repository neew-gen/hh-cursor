---
name: "job-apply"
description: "Apply to hh.ru vacancy with tailored cover letter from resume-profile YAML; compose application-plan and fill response form via Browser Tab."
compatibility: "Requires Browser Tab for hh.ru; Python package job_apply; artifacts from feature 002"
metadata:
  author: "hh-cursor"
---

## User Input

```text
$ARGUMENTS
```

Apply to an hh.ru vacancy using:
- Vacancy URL from user
- `artifacts/resume-profile/<slug>.yaml` (facts — feature 002)
- `artifacts/resume-intelligence.md` (style — feature 001, optional)

Output: `artifacts/job-apply/<vacancy-slug>.yaml` application-plan + browser apply.

## Agent communication (mandatory)

The user sees questions and final summary, not a dev log.

**Forbidden in user-facing messages:**
- Announcing CLI/bootstrap steps, validation internals, browser/CDP mechanics
- Preambles before questions («сейчас загружу профиль»)

**Allowed:**
- `AskQuestion` prompts (vacancy URL, profile choice)
- Blockers (login/captcha, missing artifacts, no resume match)
- Short preview of cover letter (first 2–3 sentences)
- Final message with artifact paths and manual submit reminder

**Turn shape:** run tools internally → one `AskQuestion` or blocker or final summary.

## Workflow

### 0. Vacancy URL

If `$ARGUMENTS` contains hh.ru vacancy URL — use it. Otherwise `AskQuestion`:

- Prompt: «Пришлите ссылку на вакансию hh.ru»
- Validate URL contains `hh.ru` and `/vacancy/`

### 1. Check prerequisites

```bash
PYTHONPATH=src python3 -m job_apply.cli list-profiles
```

- If empty: tell user to run `/resume-profile` first. **Stop.**
- If one profile: use it silently.
- If multiple: `AskQuestion` to pick profile (show `target_role` from list).

Check inputs:

```bash
PYTHONPATH=src python3 -m job_apply.cli load-inputs --profile <profile-yaml>
```

- If `intelligence_available: false`: warn that cover letter uses default rules; continue.

### 1b. Resume selection preference

Follow `specs/004-job-apply/contracts/resume-selection-format.md`.

- If user says «сбрось резюме» / «другое резюме» / «смени резюме» in `$ARGUMENTS` or chat → delete `tmp/resume-selection.json` (or `cli clear-resume-selection`).
- If `tmp/resume-selection.json` exists → use saved `resume_title` / `resume_id` for all applies; **never** swap to another resume by vacancy fit.
- If missing and hh.ru shows multiple resumes in picker → `AskQuestion` before fill; save choice to `tmp/resume-selection.json`.
- If missing and one resume → use it; save preference.

```bash
PYTHONPATH=src python3 -m job_apply.cli show-resume-selection
PYTHONPATH=src python3 -m job_apply.cli clear-resume-selection
```

### 2. Extract vacancy

Follow `specs/004-job-apply/contracts/vacancy-extract-format.md`.

1. `browser_navigate` → vacancy URL
2. Login/captcha → **stop**, user authenticates
3. Extract title, company, requirements, key_skills from page
4. Write `tmp/vacancy-extract.json` per contract format
5. `browser_unlock` when done

Use `browser_lock` before multi-step extract.

### 3. Write cover letter

Read `specs/004-job-apply/contracts/cover-letter-rules.md`.
Read profile YAML and `artifacts/resume-intelligence.md` if available.

Write `tmp/cover-letter-draft.json`:

```json
{
  "cover_letter_text": "...",
  "language": "ru",
  "rewrite_applied": true,
  "intelligence_citations": ["hh-tailoring-resume"]
}
```

**Quality goal:** letter must interest HR — specific hook, 2–3 achievements from profile, vacancy keywords, why this role/company. No generic templates.

Show user a short preview (first 2–3 sentences) before browser apply.

### 4. Compose and validate

```bash
PYTHONPATH=src python3 -m job_apply.cli compose \
  --profile <profile-yaml> \
  --vacancy tmp/vacancy-extract.json \
  --draft tmp/cover-letter-draft.json
```

```bash
PYTHONPATH=src python3 -m job_apply.cli validate \
  --input artifacts/job-apply/<vacancy-slug>.yaml \
  --profile <profile-yaml>
```

If validation fails: fix draft (no invented facts) and retry compose.

Resolve path:

```bash
PYTHONPATH=src python3 -m job_apply.cli artifact-path \
  --vacancy-url "<url>" --company "<company>" --title "<title>"
```

### 5. Browser apply

Follow `specs/004-job-apply/contracts/browser-flow.md`.

1. `browser_navigate` → vacancy URL (if not already open)
2. Login/captcha → **stop**
3. If already applied → **stop** with blocker
4. Click «Откликнуться» (`[data-qa="vacancy-response-link-top"]` or text match)
5. Select resume per `resume-selection-format.md` (saved preference or user `AskQuestion` — not `resume_match_hint` alone)
6. Paste `cover_letter.text` into cover letter textarea
7. **Do not** click «Отправить отклик»

Use `browser_lock` before multi-step apply; `browser_unlock` when done.

### 6. Write report

Save section statuses to `tmp/application-sections.json`:

```json
[
  {"section_id": "vacancy_opened", "status": "filled", "notes": ""},
  {"section_id": "resume_selected", "status": "filled", "notes": ""},
  {"section_id": "cover_letter_filled", "status": "filled", "notes": ""}
]
```

```bash
PYTHONPATH=src python3 -m job_apply.cli write-report \
  --application-plan artifacts/job-apply/<vacancy-slug>.yaml \
  --sections tmp/application-sections.json
```

### 7. Final message

> Форма отклика заполнена на hh.ru (не отправлена).
>
> Application plan: `artifacts/job-apply/<vacancy-slug>.yaml`
> Отчёт: `artifacts/job-apply/<vacancy-slug>-report.yaml`
>
> Проверьте письмо и резюме в браузере и отправьте отклик вручную.

## Out of Scope

- Auto-submit application response
- Resume tailoring for vacancy (use `/resume-create` for resume edits)
- Re-running resume-intelligence inside this skill
- Collecting profile data (use `/resume-profile`)

## References

- Spec: `specs/004-job-apply/spec.md`
- Application plan: `specs/004-job-apply/contracts/application-plan-format.md`
- Browser flow: `specs/004-job-apply/contracts/browser-flow.md`
- Resume selection: `specs/004-job-apply/contracts/resume-selection-format.md`
- Cover letter rules: `specs/004-job-apply/contracts/cover-letter-rules.md`
- Quickstart: `specs/004-job-apply/quickstart.md`
