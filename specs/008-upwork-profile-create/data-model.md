# Data Model: Upwork Profile Create

## UpworkProfile

Source artifact from feature 006.

**Fields**
- `collected_at`: ISO timestamp
- `input_mode`: `questionnaire_with_link` | `questionnaire_only`
- `profile_link`: Upwork profile URL or null
- `profile_title`: professional title
- `overview`: bio text or null
- `hourly_rate`: USD rate string (from profile; factual, not rewritten)
- `work_experience`: list of `WorkExperienceEntry`
- `skills`: list of skill tag strings
- `portfolio_links`: string list
- `limitations`: string list
- `sources`: `{ profile_link_used, fields_from_link, fields_from_user }`

## WorkExperienceEntry

**Fields**
- `company`, `position`, `start_date`, `end_date`, `is_current`, `description`, `provenance`

## FillPlan

Extends profile fields with compose metadata.

**Fields**
- All fields from `UpworkProfile`
- `composed_at`: ISO timestamp
- `source_profile`: path to profile YAML used
- `intelligence_path`: path to intelligence MD (or null)
- `intelligence_freshness`: extracted run date from intelligence (or null)
- `fill_mode`: `create_new` | `edit_existing`
- `target_url`: Upwork URL for profile settings or edit link
- `rewrite_applied`: `{ overview, profile_title, work_experience_descriptions, skills_tags }`
- `intelligence_citations`: list of source ids used for rewrite

## IntelligenceBrief

**Fields**
- `generated_at`: string or null
- `what_to_write`: list of recommendation strings (high confidence)
- `how_to_build_profile`: list of recommendation strings (high confidence)
- `limitations`: list of limitation strings
- `source_ids`: list of citation ids

## FormFieldMapping

**Fields**
- `field_id`: fill-plan field path
- `upwork_block`: human label
- `upwork_step`: integer step order
- `selector`: primary data-test selector
- `selector_fallback`: label-based fallback

## FillReport

**Fields**
- `reported_at`: ISO timestamp
- `fill_plan_path`: source fill-plan
- `fill_mode`: create_new | edit_existing
- `sections`: list of `SectionStatus`
- `blockers`: list of strings (login, captcha, etc.)
- `published`: always false in MVP

## SectionStatus

**Fields**
- `section_id`: e.g. `overview`, `profile_title`, `hourly_rate`, `skills`, `work_experience`
- `status`: `filled` | `skipped` | `failed` | `partial`
- `notes`: optional string
