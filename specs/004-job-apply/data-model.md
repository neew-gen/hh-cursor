# Data Model: Job Apply

## VacancySnapshot

**Fields**
- `url`: string — vacancy page URL
- `title`: string — job title
- `company`: string — employer name
- `requirements`: list of strings — key requirement bullets
- `key_skills`: list of strings — skills from vacancy
- `extracted_at`: ISO timestamp

## CoverLetter

**Fields**
- `text`: string — full cover letter body
- `language`: `ru` | `en`
- `char_count`: integer

## ApplicationPlan

**Fields**
- `composed_at`: ISO timestamp
- `vacancy`: VacancySnapshot
- `source_profile`: path to profile YAML
- `target_role`: string from profile
- `resume_match_hint`: string — same as target_role for hh.ru resume picker
- `cover_letter`: CoverLetter
- `rewrite_applied`: boolean
- `intelligence_path`: string or null
- `intelligence_freshness`: string or null
- `intelligence_citations`: list of source ids
- `limitations`: list of strings

## ApplicationReport

**Fields**
- `reported_at`: ISO timestamp
- `application_plan_path`: source plan path
- `submitted`: always false in MVP
- `sections`: list of SectionStatus
- `blockers`: list of strings

## SectionStatus

**Fields**
- `section_id`: `vacancy_opened` | `resume_selected` | `cover_letter_filled`
- `status`: `filled` | `skipped` | `failed` | `partial`
- `notes`: optional string

## ResumeSelectionPreference

**Storage**: `tmp/resume-selection.json` (local, gitignored)

**Fields**
- `resume_title`: string — display name on hh.ru resume picker
- `resume_id`: string — hh.ru resume hash from picker input value
- `selected_at`: ISO timestamp
- `source`: `user` | `single_available`

**Lifecycle**
- Created when user picks a resume (or auto when only one resume exists).
- Read before every browser apply; overrides `resume_match_hint` from ApplicationPlan.
- Deleted only on explicit user reset request.
