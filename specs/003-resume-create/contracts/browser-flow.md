# Contract: Browser Flow

## Create New (`fill_mode: create_new`)

1. `browser_navigate` → `https://hh.ru/applicant/resumes`
2. If login/captcha → **STOP**, ask user to authenticate
3. Click «Создать резюме» (`[data-qa="resume-create-button"]` or text match)
4. Fill sections in order per `hh-form-mapping.md`
5. Optional: click «Сохранить» draft — do **not** click «Опубликовать»
6. Report filled sections via `write-report`

## Edit Existing (`fill_mode: edit_existing`)

1. `browser_navigate` → `target_url` (from profile `resume_link`)
2. If login/captcha → **STOP**
3. Click «Редактировать» on resume page
4. Update sections from fill-plan (prioritize rewritten text blocks)
5. Stop before publish
6. Report filled sections

## Stop Conditions (mandatory)

| Condition | Action |
|-----------|--------|
| Login wall | Pause; user logs in; resume from same URL |
| Captcha | Pause; user solves; resume |
| Missing profile artifact | Do not open browser; ask user to run `/resume-profile` |
| Invalid fill-plan | Fix compose/validate before browser |
| Publish confirmation | **Never auto-confirm** in MVP |

## Lock Workflow

```
browser_navigate → browser_lock → fill sections → browser_unlock
```

If tab already exists: `browser_lock` first.

## Final User Message

After fill, agent sends:

> Резюме заполнено на hh.ru (черновик).
>
> Fill-plan: `artifacts/resume-create/<slug>.yaml`
> Отчёт: `artifacts/resume-create/<slug>-report.yaml`
>
> Проверьте форму в браузере и опубликуйте вручную.
