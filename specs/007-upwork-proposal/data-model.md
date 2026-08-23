# Data Model: Upwork Proposal

## JobSnapshot

**Fields**
- `url`: string — job page URL
- `title`: string — job title
- `client`: string — client name (if visible)
- `description`: string — job description text
- `budget_type`: string — `hourly` | `fixed` | empty
- `key_skills`: list of strings — skills from job posting
- `screening_questions`: list of strings — client screening questions
- `extracted_at`: ISO timestamp

## ProposalCoverLetter

**Fields**
- `text`: string — full proposal body
- `language`: default `en`
- `char_count`: integer

## ScreeningAnswer

**Fields**
- `question`: string — screening question text
- `answer`: string — factual answer from profile

## ContractTerms (optional)

**Fields**
- `bid_type`: `hourly` | `fixed` | null
- `hourly_rate`: string or null
- `fixed_price`: string or null
- `duration`: string or null
- `weekly_hours`: string or null
- `milestones`: list of strings
- `connects_required`: integer or null

## ProposalPlan

**Fields**
- `composed_at`: ISO timestamp
- `job`: JobSnapshot
- `source_profile`: path to profile YAML
- `target_role`: string from profile
- `profile_match_hint`: string — same as target_role
- `cover_letter`: ProposalCoverLetter
- `screening_answers`: list of ScreeningAnswer
- `contract_terms`: ContractTerms or null
- `rewrite_applied`: boolean
- `intelligence_path`: string or null
- `intelligence_freshness`: string or null
- `intelligence_citations`: list of source ids
- `limitations`: list of strings

## ProposalReport

**Fields**
- `reported_at`: ISO timestamp
- `proposal_plan_path`: source plan path
- `submitted`: always false in MVP
- `sections`: list of SectionStatus
- `blockers`: list of strings

## SectionStatus

**Fields**
- `section_id`: `job_opened` | `cover_letter_filled` | `screening_questions_filled` | `contract_terms_filled`
- `status`: `filled` | `skipped` | `failed` | `partial`
- `notes`: optional string
