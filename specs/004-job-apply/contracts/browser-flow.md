# Contract: Browser Flow — Job Apply

## Extract Vacancy

1. `browser_navigate` → vacancy URL from user
2. If login/captcha → **STOP**, ask user to authenticate
3. Extract title, company, requirements, skills per `vacancy-extract-format.md`
4. Write `tmp/vacancy-extract.json`
5. `browser_unlock` if locked

## Apply to Vacancy

1. `browser_navigate` → vacancy URL (or continue on same tab)
2. If login/captcha → **STOP**
3. If page shows «Вы откликнулись» / already applied → **STOP** with blocker
4. Click «Откликнуться» — selectors (try in order):
   - `[data-qa="vacancy-response-link-top"]`
   - `[data-qa="vacancy-response-link-bottom"]`
   - button/link with text «Откликнуться»
5. In response modal:
   - Read `tmp/resume-selection.json` per `resume-selection-format.md`
   - **If preference exists**: select that resume (`resume_id` first, else `resume_title` fuzzy match). Do not substitute another resume.
   - **If no preference and multiple resumes in picker**: **STOP** → `AskQuestion` with resume titles → save preference → continue
   - **If no preference and single resume**: select it; save preference with `source: single_available`
   - If saved resume not in picker → **STOP** with blocker; suggest reset preference
   - Fill cover letter textarea:
     - `[data-qa="vacancy-response-popup-form-letter-input"]`
     - or `textarea` in response popup
   - Paste text from application-plan `cover_letter.text`
6. **Do not** click «Отправить отклик» / submit button
7. Report sections via `write-report`

## Stop Conditions (mandatory)

| Condition | Action |
|-----------|--------|
| Login wall | Pause; user logs in; resume |
| Captcha | Pause; user solves; resume |
| Vacancy closed | Blocker; do not apply |
| Already applied | Blocker; do not overwrite |
| No resume match | Blocker; suggest publish via `/resume-create` |
| Saved resume not in picker | Blocker; suggest reset `tmp/resume-selection.json` |
| Multiple resumes, no preference | Pause; `AskQuestion`; save preference |
| Missing profile | Do not open browser; run `/resume-profile` |
| Invalid application-plan | Fix compose/validate before browser |
| Submit confirmation | **Never auto-submit** in MVP |

## Lock Workflow

```
browser_navigate → browser_lock → extract or apply → browser_unlock
```

If tab already exists: `browser_lock` first.

## Final User Message

After fill, agent sends:

> Форма отклика заполнена на hh.ru (не отправлена).
>
> Application plan: `artifacts/job-apply/<vacancy-slug>.yaml`
> Отчёт: `artifacts/job-apply/<vacancy-slug>-report.yaml`
>
> Проверьте письмо и резюме в браузере и отправьте отклик вручную.
