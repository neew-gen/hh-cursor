# Contract: Application Plan Format

**Artifact path**: `artifacts/job-apply/<vacancy-slug>.yaml`

**Vacancy slug**: from vacancy URL ID (`vacancy-12345678`) or slugified `company-title`.

## Top-Level Fields

| Field | Type | Required |
|-------|------|----------|
| `composed_at` | ISO-8601 string | yes |
| `vacancy` | VacancySnapshot object | yes |
| `source_profile` | string path | yes |
| `target_role` | string | yes |
| `resume_match_hint` | string | yes |
| `cover_letter` | CoverLetter object | yes |
| `rewrite_applied` | boolean | yes |
| `intelligence_path` | string \| null | no |
| `intelligence_freshness` | string \| null | no |
| `intelligence_citations` | string[] | no |
| `limitations` | string[] | yes |

## VacancySnapshot

```yaml
vacancy:
  url: "https://hh.ru/vacancy/12345678"
  title: "Frontend-разработчик"
  company: "Пример Компания"
  requirements:
    - "Опыт с Vue 3"
    - "TypeScript"
  key_skills:
    - "Vue"
    - "TypeScript"
  extracted_at: "2026-07-09T12:00:00+00:00"
```

## CoverLetter

```yaml
cover_letter:
  text: |
    Текст сопроводительного письма...
  language: ru
  char_count: 1500
```

## Completeness Rules

Application plan is **complete** when:

1. `vacancy.url` and `vacancy.title` are non-empty.
2. `cover_letter.text` is non-empty and `char_count` matches text length.
3. `source_profile` points to existing profile YAML.
4. `target_role` matches profile `target_role`.

## Excluded Fields

Do **not** include: cookies, tokens, applicant PII beyond profile facts.
