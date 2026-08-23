# Contract: Upwork Form Mapping

Maps fill-plan fields to Upwork profile settings UI.

## Field Mappings

| field_id | upwork_block | step | selector | fallback |
|----------|--------------|------|----------|----------|
| `profile_title` | Title | 1 | `[data-test="profile-title-input"]` | Title |
| `hourly_rate` | Hourly rate | 2 | `[data-test="hourly-rate-input"]` | Hourly rate |
| `overview` | Overview | 3 | `[data-test="overview-textarea"]` | Overview |
| `skills` | Skills | 4 | `[data-test="skills-input"]` | Skills |
| `work_experience` | Employment History | 5 | `[data-test="employment-add"]` | Add employment |
| `portfolio` | Portfolio | 6 | `[data-test="portfolio-add"]` | Add portfolio |

## Fill Order

1. **profile_title** — single-line input
2. **hourly_rate** — USD rate from profile `hourly_rate` (factual; do not rewrite). Open Edit hourly rate, set value, then apply Save policy
3. **overview** — multiline textarea (5000 char limit on Upwork; agent should stay concise)
4. **skills** — typeahead tags from `skills` list
5. **work_experience** — for each entry: add employment, fill company/position/dates from profile, paste rewritten `description` (**≤ 500 characters**; rewrite to fit — never mid-cut)
6. **portfolio** — only after GitHub consent + project selection (`portfolio-from-github.md`). For each approved item: Add portfolio → title, description, URL, skills → Save policy. Ask before replacing existing cards.

## Date Format

Normalize to `MM.YYYY` via `mapper.format_date_for_form`.

## CLI

```bash
PYTHONPATH=src python3 -m upwork_profile_create.cli form-mappings
```

## Notes

- Selectors are best-effort; Upwork may change DOM. Use label fallback and snapshot inspection.
- Employment structural fields (company, title, dates) and `hourly_rate` are factual — copy from fill-plan without rewrite.
- After each section/modal fill, follow the Save policy in `browser-flow.md` / skill (wait for user Save by default).
