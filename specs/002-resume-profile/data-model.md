# Data Model: Resume Profile

## WorkExperienceEntry

**Fields**
- `company`: employer name
- `position`: job title
- `start_date`: `YYYY-MM`
- `end_date`: `YYYY-MM` or null when current
- `is_current`: boolean
- `description`: duties and achievements text
- `company_description`: optional
- `provenance`: `from_resume_link` | `from_user_answer` | `inferred`

## SkillEntry

**Fields**
- `name`: skill name
- `level`: `basic` | `medium` | `advanced`
- `provenance`

## EducationEntry

**Fields**
- `institution`: school name
- `degree`: degree level label
- `specialty`: field of study
- `graduation_year`: integer year
- `provenance`

## WorkPreferences

**Fields** (all optional)
- `salary`
- `employment_type`
- `work_format`
- `commute_time`
- `business_trips`

## LanguageEntry

**Fields**
- `name`
- `level`: CEFR label

## ResumeProfile

**Fields**
- `collected_at`: ISO timestamp
- `input_mode`: `questionnaire_with_link` | `questionnaire_only`
- `resume_link`: optional URL
- `target_role`: required string
- `specializations`: list of strings
- `work_experience_status`: `none` | `has_experience`
- `work_experience`: list of WorkExperienceEntry
- `skills`: `{ hard: SkillEntry[], soft: SkillEntry[] }`
- `education`: list of EducationEntry
- `no_formal_education`: boolean
- `about_me`: optional string
- `work_preferences`: optional WorkPreferences
- `languages`: list of LanguageEntry
- `additional_education`: list of strings
- `portfolio_links`: list of strings
- `personal_links`: list of strings
- `limitations`: list of strings
- `sources`: `{ resume_link_used, fields_from_link, fields_from_user }`

## GapField

**Fields**
- `field_id`: schema identifier
- `question`: user-facing gap question text
- `required`: boolean

## CollectionRun

**Fields**
- `started_at`, `finished_at`
- `artifact_path`
- `gaps_remaining`: count at finish

## Relationships

- One `ResumeProfile` has many `WorkExperienceEntry`, `SkillEntry`, `EducationEntry`.
- `GapField` records are computed from incomplete `ResumeProfile` against `schema.REQUIRED_FIELDS`.
