# Contract: Profile Artifact Format

**Artifact path**: `artifacts/resume-profile/<target-role-slug>.yaml`

Slug = transliterated `target_role` (Latin, lowercase, hyphens), e.g. `Frontend Developer (Vue)` → `frontend-developer-vue.yaml`.

## Top-Level Fields

| Field | Type | Required | hh.ru block |
|-------|------|----------|-------------|
| `collected_at` | ISO-8601 string | yes | metadata |
| `input_mode` | enum | yes | metadata |
| `resume_link` | string \| null | no | metadata |
| `target_role` | string | yes | Профессия |
| `specializations` | string[] | no | Специализации |
| `work_experience_status` | `none` \| `has_experience` | yes | Опыт работы |
| `work_experience` | WorkExperienceEntry[] | conditional | Опыт работы |
| `skills.hard` | SkillEntry[] | yes (min 1) | Ключевые навыки |
| `skills.soft` | SkillEntry[] | no | — |
| `education` | EducationEntry[] | conditional | Образование |
| `no_formal_education` | boolean | no | Образование |
| `about_me` | string \| null | no | Обо мне |
| `work_preferences` | object | no | Условия |
| `languages` | LanguageEntry[] | no | Языки |
| `additional_education` | string[] | no | Доп. образование |
| `portfolio_links` | string[] | no | Портфолио |
| `personal_links` | string[] | no | Личная страница |
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

## SkillEntry

```yaml
name: string
level: basic | medium | advanced
provenance: ...
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

1. `target_role` is non-empty.
2. `skills.hard` has at least one entry.
3. Either `work_experience_status: none` with empty `work_experience`, OR
   `work_experience_status: has_experience` with at least one valid entry.
4. Either `education` has at least one entry, OR `no_formal_education: true`.

`about_me` is optional for artifact completeness; gap question is asked when empty after extract.

## Gap When Empty

| Field | Gap question if empty after extract |
|-------|-------------------------------------|
| `about_me` | yes (optional — write allowed without answer) |

## Excluded Fields

Do **not** include: `key_phrases`, `tools`, ATS hints, resume-intelligence references.
