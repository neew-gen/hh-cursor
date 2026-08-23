# Data Model: Upwork Profile

## WorkExperienceEntry (freelancer_core)

**Fields**
- `company`: employer or client name
- `position`: role title
- `start_date`: `YYYY-MM`
- `end_date`: `YYYY-MM` or null when current
- `is_current`: boolean
- `description`: responsibilities and achievements text
- `company_description`: optional
- `provenance`: `from_resume_link` | `from_user_answer` | `inferred`

## EducationEntry (freelancer_core)

**Fields**
- `institution`: school name
- `degree`: degree level label
- `specialty`: field of study
- `graduation_year`: integer year
- `provenance`

## UpworkSourceStats

**Fields**
- `profile_link_used`: boolean
- `fields_from_link`: integer count
- `fields_from_user`: integer count

## UpworkProfile

**Fields**
- `collected_at`: ISO timestamp
- `input_mode`: `questionnaire_with_link` | `questionnaire_only`
- `profile_link`: optional Upwork profile URL
- `profile_title`: required string
- `overview`: required string
- `hourly_rate`: required string (USD)
- `skills`: list of string tags
- `work_experience_status`: `none` | `has_experience`
- `work_experience`: list of WorkExperienceEntry
- `education`: list of EducationEntry
- `portfolio_links`: list of URLs
- `limitations`: list of strings
- `sources`: UpworkSourceStats

## GapField

**Fields**
- `field_id`: schema identifier
- `question`: user-facing gap question text (English)
- `required`: boolean

## Relationships

- One `UpworkProfile` has many `WorkExperienceEntry`, `EducationEntry`.
- `GapField` records are computed from incomplete `UpworkProfile` against MVP rules.
