# Contract: Job Extract Format

Browser extract saved to `tmp/upwork-job-extract.json` for CLI `compose`.

## JSON Schema

```json
{
  "url": "https://www.upwork.com/jobs/~0123456789abcdef",
  "title": "Senior Frontend Developer",
  "client": "TechStartup Inc",
  "description": "Build a React dashboard with TypeScript and REST API integration.",
  "budget_type": "hourly",
  "key_skills": ["React", "TypeScript", "JavaScript"],
  "screening_questions": [
    "Describe your experience with React dashboards.",
    "What is your hourly rate?"
  ],
  "extracted_at": "2026-08-23T10:00:00+00:00"
}
```

## Required Fields

| Field | Type | Notes |
|-------|------|-------|
| `url` | string | Must match user-provided job URL |
| `title` | string | From job page heading |
| `client` | string | Client name if visible; may be empty |
| `description` | string | Job description text |
| `budget_type` | string | `hourly`, `fixed`, or empty |
| `key_skills` | string[] | May be empty if not listed |
| `screening_questions` | string[] | May be empty if only on apply form |
| `extracted_at` | ISO string | Set at extract time |

## Browser Extract Hints

On job page look for:
- Title: `h1` or job title heading
- Client: client name link or «About the client» section
- Skills: skill tags or «Skills and Expertise»
- Description: main job description block
- Budget: «Hourly» / «Fixed-price» badge
- Screening questions: may appear on apply form — extract when visible

If login wall blocks content → **STOP**, do not write partial extract.
