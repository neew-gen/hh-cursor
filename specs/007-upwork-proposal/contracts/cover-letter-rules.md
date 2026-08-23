# Contract: Cover Letter Rules (EN Proposal)

Agent applies these when writing `cover_letter_text` in `tmp/proposal-draft.json`.

## Intelligence Input

Read from `artifacts/upwork-intelligence.md`:

- `## WhatToWrite` — content recommendations
- Prefer bullets marked `[high]` confidence

If intelligence missing, use defaults below.

## Structure (mandatory)

1. **Hook** (1–2 sentences): specific interest in the client's project — problem, stack, or outcome; no generic «I am applying for your job».
2. **Relevant experience** (2–3 bullets or short paragraphs): achievements from profile `work_experience` aligned with job requirements.
3. **Fit** (1 paragraph): map profile `skills.hard` to job `key_skills` / description.
4. **Call-to-action** (1 sentence): readiness to discuss scope, timeline, or next step; confident tone.

## Length

- Target: 600–2000 characters
- Maximum: 5000 characters (Upwork limit)
- Minimum: 300 characters

## Constraints (always)

| Rule | Detail |
|------|--------|
| Facts only from profile | Companies, positions, dates, skills MUST exist in profile YAML |
| No new employers | Do not claim work at companies not in `work_experience` |
| No new skills | Skills mentioned must be in `skills.hard` or experience descriptions |
| No fake metrics | Only quantify if profile already implies scale |
| Job keywords | Use job requirements/skills vocabulary naturally |
| Language | English (`en`) by default for Upwork |
| Tone | Professional, specific; no «Dear Sir/Madam», no generic templates |
| No application opener | Do not open with «I am applying for your job posting» |

### Forbidden openings (examples)

- «I am applying for your job posting on Upwork»
- «I saw your job and I am interested»
- «I would like to apply for the position of …»

Instead — hook: specific project detail, stack match, or client goal.

**Example opening:** «Hi — your dashboard rebuild aligns with the TypeScript interfaces I shipped at Acme Corp…»

## Client Interest Criteria

Proposal should make client want to respond:

- Opens with why **this** project matches **your** proven experience
- Shows 2–3 concrete proof points from real profile experience
- Demonstrates understanding of job requirements
- Ends with confident, short CTA

## Draft JSON for compose

```json
{
  "cover_letter_text": "...",
  "language": "en",
  "rewrite_applied": true,
  "intelligence_citations": ["upwork-proposal-guide"],
  "screening_answers": [
    {
      "question": "Describe your experience with React dashboards.",
      "answer": "..."
    }
  ],
  "contract_terms": {
    "bid_type": "hourly",
    "hourly_rate": "$60",
    "duration": "1 to 3 months",
    "connects_required": 6
  }
}
```

## Metadata for compose

`intelligence_citations` — source ids from intelligence used for style guidance.
