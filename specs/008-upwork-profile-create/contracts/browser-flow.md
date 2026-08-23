# Contract: Browser Flow

## Create New (`fill_mode: create_new`)

1. `browser_navigate` → `https://www.upwork.com/freelancer/settings/profile`
2. If login/captcha → **STOP**, ask user to authenticate
3. Fill sections in order per `upwork-form-mapping.md` (including `hourly_rate`)
4. **Portfolio** — only after consent + project pick per `portfolio-from-github.md`
5. Apply **Save policy** after each section (default: wait for user)
6. Report filled sections via `write-report`

## Edit Existing (`fill_mode: edit_existing`)

1. `browser_navigate` → `target_url` (from profile `profile_link`)
2. If login/captcha → **STOP**
3. Navigate to profile edit sections
4. Update sections from fill-plan (prioritize rewritten text blocks; set `hourly_rate` from profile)
5. **Portfolio** — consent + project pick (`portfolio-from-github.md`); ask keep/update/replace for existing cards
6. Apply **Save policy** after each section
7. Report filled sections

## Save policy (mandatory)

| Mode | When | Agent action |
|------|------|--------------|
| **Default** | Profile sections (overview, skills, employment, …) | Do **not** click Save / Publish / Submit. Stop after filling; wait until the user saves and says continue |
| **Portfolio draft** | Each Upwork portfolio item modal | Agent **must** click **Save as draft** after fill; verify card under **Drafts**; then ask user to upload thumbnail (see `portfolio-from-github.md`) |
| **User opted out** | User explicitly says not to wait and to save (e.g. «сохраняй сам», «не жди», «save yourself») | Agent may click Save for that filled section |
| **Publish** | Never by default | Do not publish profile or portfolio unless the user explicitly asks |

## Stop Conditions (mandatory)

| Condition | Action |
|-----------|--------|
| Login wall | Pause; user logs in; resume from same URL |
| Captcha | Pause; user solves; resume |
| Missing profile artifact | Do not open browser; ask user to run upwork-profile skill |
| Invalid fill-plan | Fix compose/validate before browser |
| Section filled (default) | Pause for user Save; resume on continue |
| Publish confirmation | **Never auto-confirm** unless user explicitly requested publish |
| No GitHub consent / no project pick | Skip Portfolio; do not invent items |
| Stale project without user pick | Do not add to Portfolio |

## Lock Workflow

```
browser_navigate → browser_lock → fill section → browser_unlock → wait for user Save → repeat
```

If tab already exists: `browser_lock` first.

## Final User Message

After fill, agent sends:

> Профиль заполнен на Upwork (черновик).
>
> Fill-plan: `artifacts/upwork-profile-create/<slug>.yaml`
> Отчёт: `artifacts/upwork-profile-create/<slug>-report.yaml`
>
> Проверьте форму в браузере и сохраните вручную (если не просили сохранять автоматически).
