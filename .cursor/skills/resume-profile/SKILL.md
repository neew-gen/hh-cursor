---
name: "resume-profile"
description: "Collect hh.ru resume form data via optional resume link and gap questionnaire; write artifacts/resume-profile/<target-role-slug>.yaml. Does not use resume-intelligence."
compatibility: "Requires Browser Tab for hh.ru link extract; Python package resume_profile"
metadata:
  author: "hh-cursor"
---

## User Input

```text
$ARGUMENTS
```

Collect user profile data for filling an hh.ru resume on the next step (feature 003).
**Do not read** `artifacts/resume-intelligence.md` or feature 001 artifacts.

Artifacts directory: `artifacts/resume-profile/` (gitignored). Filename slug = transliterated `target_role`, e.g. `Frontend Developer (Vue)` → `frontend-developer-vue.yaml`.

## Agent communication (mandatory)

The user sees a questionnaire, not a dev log. **Never narrate internal work in chat.**

**Forbidden in user-facing messages** (including the first reply after `/resume-profile`):
- Announcing bootstrap, init-draft, CLI, artifact checks, gap detection, validation, browser/CDP steps
- Reporting outcomes of step 0 («артефактов нет», «сразу показываю Q1», «инициализирую черновик»)
- Preambles before a question («сейчас задам вопрос», «перейдём к следующему шагу»)
- Describing what you *will* do instead of doing it silently and showing the next prompt

**Allowed user-facing text:**
- `AskQuestion` prompts only (Q0, Q1, gap questions) — **no extra chat text in the same turn**
- Blockers that need user action (login/captcha on hh.ru, invalid resume URL)
- Final confirmation with artifact path after `write`

**Turn shape:** run tools internally → one `AskQuestion` (or blocker / final path). Empty chat body is fine when the question carries the whole turn.

**First turn after `/resume-profile`:** no greeting, no explanation — only Q0 (if saved profiles exist) or Q1 (if not).

## Workflow

### 0. Initialize new draft

Always start feature 002 as a **brand-new collection run**.
Do **not** inspect existing artifacts to decide whether to update, supplement, append, or reuse them.
Do **not** ask any Q0-like question.

Start command:

```bash
PYTHONPATH=src python3 -m resume_profile.cli init-draft \
  --skills-mode new \
  --output tmp/profile-draft.json
```

Operational notes:

- Treat background shell completions as internal status, not as a reason to repeat the same user-facing prompt.
- If a shell command hangs or backgrounds with no output, inspect once, use the documented fallback, and continue the workflow instead of narrating each retry.
- After draft initialization, show Q1 in the same turn with **no** intervening chat text.
- Never expose step-0 mechanics to the user; only expose the resulting `AskQuestion`.

### 1. Q1 — Resume link (optional)

Ask Q1 **only via `AskQuestion`**. No accompanying chat text — see **Agent communication**.

- Title: `Профиль резюме`
- Prompt: `Введите сюда ссылку на ваше резюме на HeadHunter (hh.ru).`
- Options:
  - `provide_link` — `Ввести ссылку на ваше резюме`
  - `skip_link` — `Пропустить этот шаг и перейти к вопросам`
- The user must be able to choose the link option and paste the URL via `Other` in the same form flow.
- Do **not** ask «Будете ли вы вводить ссылку?» before this prompt.
- Do **not** require a separate follow-up message just to paste the link.
- If `provide_link` is selected but the URL value is not captured by `AskQuestion`, send a plain chat prompt like `Вставьте ссылку на резюме hh.ru и отправьте сообщение.` and wait for the next user message. Do **not** show another `AskQuestion`.

If URL provided:

1. Validate with `PYTHONPATH=src python3 -c "from resume_profile.extractor import is_valid_hh_resume_link; print(is_valid_hh_resume_link('URL'))"`
2. Browser Tab: `browser_navigate` to URL
3. If login/captcha → **stop**, ask user to authenticate, then continue
4. Download full resume via the page button (not `main.innerText`):
   - Click `[data-qa="resume-download-button"]`
   - Choose **Простой текст · txt** (or fetch the `type=txt` href from the opened menu)
   - Fetch the download URL in the same browser session and save to `tmp/resume-download.html`
   - hh.ru serves a full HTML document here (despite `.txt` in the URL)
5. **Always** run extract CLI (never hand-build JSON from snapshot):
   ```bash
   PYTHONPATH=src python3 -m resume_profile.cli extract-text \
     --input tmp/resume-download.html \
     --output tmp/profile-draft.json \
     --resume-link "URL"
   ```
   Preserve `_meta` from prior `init-draft` when merging extract output into draft.

If Skip:

- Keep current `tmp/profile-draft.json` from step 0.
- Silently continue to the next gap; show only the next `AskQuestion`.

### 2. Gap questionnaire loop

Repeat until `validate` reports `"complete": true`:

```bash
PYTHONPATH=src python3 -m resume_profile.cli gaps --input tmp/profile-draft.json
PYTHONPATH=src python3 -m resume_profile.cli validate --input tmp/profile-draft.json
```

For each gap from `gaps` output, ask **one question** at a time — `AskQuestion` only, no chat commentary between questions.

**AskQuestion options** — use `ask_options` from CLI output **verbatim** (do not invent options):
- Options come **only** from the current `tmp/profile-draft.json` draft (partial field values) plus the fixed defer option.
- **Never** use other artifact files or prior sessions to build answer choices (except loading the chosen artifact in Q0 for supplement).
- Option `defer_to_chat` («Отвечу в следующем сообщении») is **always last**; wait for free-form text in chat when selected.
- For fixed-choice fields (`work_experience_status`, `no_formal_education`) use CLI options as-is (no defer).

**Voice / long text:** `AskQuestion` has no native voice input. For `about_me`:
- Accept **free-form reply in chat** (user can use macOS dictation in the chat field), OR
- `AskQuestion` with an «Other» option for pasted text.

Field merge hints:

| field_id | JSON path |
|----------|-----------|
| target_role | `target_role` |
| work_experience_status | `work_experience_status` (`none` / `has_experience`) |
| work_experience | append to `work_experience[]` |
| skills.hard | append to `skills.hard[]` with `level` and `provenance: from_user_answer` |
| education | append to `education[]` |
| no_formal_education | `no_formal_education: true` |
| about_me | `about_me` string, `provenance: from_user_answer` if user-filled |

Optional gap `about_me` may remain empty; required gaps must be filled before write.

### 3. Validate and write artifact

Resolve output path (or let CLI derive from `target_role`):

```bash
PYTHONPATH=src python3 -m resume_profile.cli artifact-path --target-role "Frontend Developer (Vue)"
PYTHONPATH=src python3 -m resume_profile.cli validate --input tmp/profile-draft.json
PYTHONPATH=src python3 -m resume_profile.cli write --input tmp/profile-draft.json
```

Default write path: `artifacts/resume-profile/<translit-target-role>.yaml` (только YAML, без JSON sidecar).
If the same slug already exists, write a **new** file with a numeric suffix in parentheses:
`<slug> (2).yaml`, `<slug> (3).yaml`, and so on.

После `write` отправь пользователю нормальное финальное сообщение, например:

> Профиль резюме готов.
>
> Данные сохранены в `artifacts/resume-profile/<slug>.yaml`.
>
> Должность: **<target_role>**. На следующем шаге этот файл можно использовать для заполнения формы на hh.ru.

Не ограничивайся одной строкой с путём к файлу. **Do not** fill hh.ru form in this skill (feature 003).

## Out of Scope

- resume-intelligence / ATS advice
- Vacancy URL collection
- Publishing or editing resume on hh.ru
- Separate key_phrases or tools fields

## References

- Spec: `specs/002-resume-profile/spec.md`
- Profile format: `specs/002-resume-profile/contracts/profile-format.md`
- Questionnaire: `specs/002-resume-profile/contracts/questionnaire-flow.md`
- Quickstart: `specs/002-resume-profile/quickstart.md`
