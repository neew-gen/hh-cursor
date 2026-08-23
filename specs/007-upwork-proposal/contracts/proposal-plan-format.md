# Contract: Proposal Plan Format

**Artifact path**: `artifacts/upwork-proposal/<job-slug>.yaml`

**Job slug**: from job URL ID (`job-0123456789abcdef`) or slugified `client-title`.

## Top-Level Fields

| Field | Type | Required |
|-------|------|----------|
| `composed_at` | ISO-8601 string | yes |
| `job` | JobSnapshot object | yes |
| `source_profile` | string path | yes |
| `target_role` | string | yes |
| `profile_match_hint` | string | yes |
| `cover_letter` | ProposalCoverLetter object | yes |
| `screening_answers` | ScreeningAnswer[] | no |
| `contract_terms` | ContractTerms object \| null | no |
| `rewrite_applied` | boolean | yes |
| `intelligence_path` | string \| null | no |
| `intelligence_freshness` | string \| null | no |
| `intelligence_citations` | string[] | no |
| `limitations` | string[] | yes |

## JobSnapshot

```yaml
job:
  url: "https://www.upwork.com/jobs/~0123456789abcdef"
  title: "Senior Frontend Developer"
  client: "TechStartup Inc"
  description: |
    Build a React dashboard with TypeScript...
  budget_type: hourly
  key_skills:
    - React
    - TypeScript
  screening_questions:
    - "Describe your experience with React dashboards."
  extracted_at: "2026-08-23T10:00:00+00:00"
```

## ProposalCoverLetter

```yaml
cover_letter:
  text: |
    Hi there — I was drawn to your dashboard project...
  language: en
  char_count: 850
```

## ScreeningAnswer

```yaml
screening_answers:
  - question: "Describe your experience with React dashboards."
    answer: "Built multiple dashboards with Vue and TypeScript..."
```

## ContractTerms (optional)

```yaml
contract_terms:
  bid_type: hourly
  hourly_rate: "$60"
  fixed_price: null
  duration: "1 to 3 months"
  weekly_hours: "30"
  milestones: []
  connects_required: 6
```

## Completeness Rules

Proposal plan is **complete** when:

1. `job.url` and `job.title` are non-empty.
2. `cover_letter.text` is non-empty, 300–5000 chars, `char_count` matches length.
3. `source_profile` points to existing profile YAML.
4. `target_role` matches profile `target_role`.
5. All `job.screening_questions` have matching non-empty answers when questions present.

## Excluded Fields

Do **not** include: cookies, tokens, applicant PII beyond profile facts.
