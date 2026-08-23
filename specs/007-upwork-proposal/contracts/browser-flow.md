# Contract: Browser Flow — Upwork Proposal

## Extract Job

1. `browser_navigate` → job URL from user
2. If login/captcha → **STOP**, ask user to authenticate
3. Extract title, client, description, budget_type, skills, screening questions per `job-extract-format.md`
4. Write `tmp/upwork-job-extract.json`
5. `browser_unlock` if locked

## Submit Proposal (fill only)

1. `browser_navigate` → job URL (or continue on same tab)
2. If login/captcha → **STOP**
3. If page shows job closed or already applied → **STOP** with blocker
4. Click «Apply Now» / «Submit a Proposal» — try:
   - button with text «Apply Now» or «Submit a Proposal»
   - `[data-test="apply-button"]` if present
5. **Connects checkpoint** (before filling or after opening form):
   - Read Connects required for this job (badge or apply modal text)
   - Report to user: «This proposal requires N Connects»
   - If Connects insufficient → **STOP** with blocker
   - Do not proceed to Send without user awareness of Connects cost
6. In proposal form:
   - Fill cover letter textarea with `cover_letter.text` from proposal-plan
   - Fill each screening question with matching `screening_answers`
   - If `contract_terms` present: fill hourly rate, fixed price, duration, weekly hours as applicable
7. **Do not** click Send / Submit Proposal button
8. Report sections via `write-report`

## Stop Conditions (mandatory)

| Condition | Action |
|-----------|--------|
| Login wall | Pause; user logs in; resume |
| Captcha | Pause; user solves; resume |
| Job closed | Blocker; do not apply |
| Already applied | Blocker; do not overwrite |
| Insufficient Connects | Blocker; report required vs available |
| Screening Q mismatch | Blocker; re-extract or update plan |
| Missing profile | Do not open browser; run `/upwork-profile` |
| Invalid proposal-plan | Fix compose/validate before browser |
| Send confirmation | **Never auto-submit** in MVP |

## Lock Workflow

```
browser_navigate → browser_lock → extract or fill → browser_unlock
```

If tab already exists: `browser_lock` first.

## Final User Message

After fill, agent sends:

> Proposal form filled on Upwork (not submitted).
>
> Proposal plan: `artifacts/upwork-proposal/<job-slug>.yaml`
> Report: `artifacts/upwork-proposal/<job-slug>-report.yaml`
> Connects required: N
>
> Review the proposal in the browser and submit manually when ready.
