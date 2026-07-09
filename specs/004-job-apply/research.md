# Research: Job Apply

## hh.ru Response UI

- Vacancy page has «Откликнуться» at top and bottom; `data-qa` attributes vary by A/B tests.
- Response opens modal/drawer with resume picker and optional cover letter field.
- Cover letter is optional on some vacancies but skill always fills it when field exists.
- Submit button text: «Отправить отклик» or similar — must not be clicked in MVP.

## Resume Selection

- User's published resumes shown as cards with title (matches `target_role` from profile).
- Fuzzy match: normalize case, compare substring or token overlap.
- If multiple resumes match, pick closest string match to `resume_match_hint`.

## Vacancy Extract

- Public vacancy pages may show partial content without login; full description often requires auth.
- On login wall during extract → pause per constitution.

## Cover Letter Validation Heuristics

- Extract employer names from profile `work_experience[].company`
- Flag cover letter if it mentions company names not in profile (unless same as vacancy company)
- Skills mentioned should be subset of profile skills ∪ vacancy key_skills (allow vacancy terms as targets, not claims)

## Selectors to Monitor

| Element | Primary selector | Fallback |
|---------|------------------|----------|
| Respond button | `vacancy-response-link-top` | text «Откликнуться» |
| Letter input | `vacancy-response-popup-form-letter-input` | textarea in modal |
| Resume card | resume title text | radio in modal |
