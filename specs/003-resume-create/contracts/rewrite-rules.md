# Contract: Rewrite Rules

Agent applies these when rewriting `about_me` and `work_experience[].description`.

## Intelligence Input

Read from `artifacts/resume-intelligence.md`:

- `## WhatToWrite` — content recommendations
- `## HowToBuildResume` — structure recommendations
- Prefer bullets marked `[high]` confidence

If intelligence missing, use defaults below.

## Default Rules (no intelligence)

1. Use bullet points for experience descriptions.
2. Lead with measurable achievements where facts exist in profile.
3. Keep hard skills visible in experience text when already mentioned.
4. Professional Russian tone; no fluff.
5. Do not invent companies, dates, skills, or metrics.

## Constraints (always)

| Rule | Detail |
|------|--------|
| Facts only from profile | Companies, dates, positions, skill names MUST match profile |
| No new skills | Do not add skills absent from `skills.hard` or experience stack lines |
| No fake metrics | Only quantify if profile already implies scale |
| Preserve links | Keep URLs from profile `about_me` verbatim |
| Language | Russian unless profile is explicitly English |

## about_me Rewrite

- 2–4 short paragraphs max
- First paragraph: role focus aligned with `target_role`
- Include pet projects / links if present in profile
- Apply `WhatToWrite` high-confidence bullets

## work_experience[].description Rewrite

- Bullet list format (`- ` prefix)
- Responsibilities + achievements per role
- Keep «Стек:» line if present in source description
- Keep «Достижения:» line if present
- One entry per profile `work_experience` item — same company count

## Metadata for compose

Pass to CLI:

```json
{
  "rewrite_applied": {
    "about_me": true,
    "work_experience_descriptions": true
  },
  "intelligence_citations": ["hh-knowledge-create-resume", "..."]
}
```
