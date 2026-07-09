# Contract: Vacancy Extract Format

Browser extract saved to `tmp/vacancy-extract.json` for CLI `compose`.

## JSON Schema

```json
{
  "url": "https://hh.ru/vacancy/12345678",
  "title": "Frontend-разработчик",
  "company": "Пример Компания",
  "requirements": [
    "Опыт коммерческой разработки от 3 лет",
    "Знание Vue 3, TypeScript"
  ],
  "key_skills": ["Vue", "TypeScript", "JavaScript"],
  "extracted_at": "2026-07-09T12:00:00+00:00"
}
```

## Required Fields

| Field | Type | Notes |
|-------|------|-------|
| `url` | string | Must match user-provided vacancy URL |
| `title` | string | From vacancy page heading |
| `company` | string | Employer name |
| `requirements` | string[] | Min 1 bullet if visible on page |
| `key_skills` | string[] | May be empty if not listed |
| `extracted_at` | ISO string | Set at extract time |

## Browser Extract Hints

On vacancy page look for:
- Title: `[data-qa="vacancy-title"]` or `h1`
- Company: `[data-qa="vacancy-company-name"]` or company link text
- Skills: `[data-qa="skills-element"]` or skill chips
- Requirements: vacancy description section bullets or paragraphs

If login wall blocks content → **STOP**, do not write partial extract.
