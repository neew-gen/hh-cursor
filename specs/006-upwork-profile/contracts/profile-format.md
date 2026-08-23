# Contract: Upwork Profile Artifact Format

**Artifact path**: `artifacts/upwork-profile/<profile-title-slug>.yaml`

Slug = transliterated `profile_title` (Latin, lowercase, hyphens), e.g.
`Full Stack Developer (React)` → `full-stack-developer-react.yaml`.

## Top-Level Fields

| Field | Type | Required | Upwork section |
|-------|------|----------|----------------|
| `collected_at` | ISO-8601 string | yes | metadata |
| `input_mode` | enum | yes | metadata |
| `profile_link` | string \| null | no | metadata |
| `profile_title` | string | yes | Profile title |
| `overview` | string | yes | Overview |
| `hourly_rate` | string | yes | Hourly rate |
| `skills` | string[] | yes (min 1) | Skills |
| `work_experience_status` | `none` \| `has_experience` | yes | Work history |
| `work_experience` | WorkExperienceEntry[] | conditional | Work history |
| `education` | EducationEntry[] | no | Education |
| `portfolio_links` | string[] | no | Portfolio |
| `limitations` | string[] | yes | metadata |
| `sources` | object | yes | metadata |

## WorkExperienceEntry

```yaml
company: string
position: string
start_date: "YYYY-MM"
end_date: "YYYY-MM" | null
is_current: boolean
description: string
company_description: string | null
provenance: from_resume_link | from_user_answer | inferred
```

## EducationEntry

```yaml
institution: string
degree: string
specialty: string
graduation_year: integer
provenance: ...
```

## Completeness Rules (MVP)

Artifact is **complete** when:

1. `profile_title` is non-empty.
2. `overview` is non-empty.
3. `hourly_rate` is non-empty.
4. `skills` has at least one entry.
5. Either `work_experience_status: none` with empty `work_experience`, OR
   `work_experience_status: has_experience` with at least one valid entry.

`education` and `portfolio_links` are optional for completeness; gap questions asked when empty.

## Gap When Empty

| Field | Gap question if empty after extract |
|-------|-------------------------------------|
| `education` | yes (optional — write allowed without answer) |
| `portfolio_links` | yes (optional) |

## Excluded Fields

Do not include `key_phrases`, `tools`, or other fields absent from Upwork profile form.

## Sources Object

```yaml
sources:
  profile_link_used: boolean
  fields_from_link: integer
  fields_from_user: integer
```
