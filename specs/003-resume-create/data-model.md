# Data Model: Resume Create

## FillPlan

Extends profile fields with compose metadata.

**Fields**
- All fields from `ResumeProfile` (see `specs/002-resume-profile/data-model.md`)
- `composed_at`: ISO timestamp
- `source_profile`: path to profile YAML used
- `intelligence_path`: path to intelligence MD (or null)
- `intelligence_freshness`: extracted run date from intelligence (or null)
- `fill_mode`: `create_new` | `edit_existing`
- `target_url`: hh.ru URL for create list or edit resume
- `rewrite_applied`: `{ about_me: bool, work_experience_descriptions: bool }`
- `intelligence_citations`: list of source ids used for rewrite

## IntelligenceBrief

**Fields**
- `generated_at`: string or null
- `what_to_write`: list of recommendation strings (high confidence)
- `how_to_build_resume`: list of recommendation strings (high confidence)
- `limitations`: list of limitation strings

## FormFieldMapping

**Fields**
- `field_id`: fill-plan field path
- `hh_block`: human label
- `hh_step`: integer step order in constructor
- `selector`: primary data-qa selector
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
- `section_id`: e.g. `target_role`, `skills.hard`
- `status`: `filled` | `skipped` | `failed` | `partial`
- `notes`: optional string
