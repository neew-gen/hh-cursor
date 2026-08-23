# Contract: Rewrite Rules

Agent applies these when rewriting `overview`, `profile_title`,
`work_experience[].description`, and `skills`.

## Intelligence Input

Read from `artifacts/upwork-intelligence.md`:

- `## WhatToWrite` — content recommendations
- `## HowToBuildProfile` — structure recommendations
- Prefer bullets marked `[high]` confidence

If intelligence missing, use defaults below.

## Default Rules (no intelligence)

1. Use bullet points for experience descriptions.
2. Lead with measurable achievements where facts exist in profile.
3. Keep hard skills visible in overview and experience text.
4. Professional English tone; concise, client-facing.
5. Do not invent companies, dates, skills, or metrics.

## Constraints (always)

| Rule | Detail |
|------|--------|
| Facts only from profile | Companies, dates, positions, skill names MUST match profile |
| No new skills | Do not add skills absent from profile `skills` or experience stack lines |
| No fake metrics | Only quantify if profile already implies scale |
| Preserve links | Keep URLs from profile `overview` or `portfolio_links` verbatim |
| Language | English unless profile is explicitly Russian |

## overview Rewrite

- 2–4 short paragraphs max
- First paragraph: role focus aligned with `profile_title`
- Include portfolio links if present
- Apply `WhatToWrite` high-confidence bullets

## profile_title Rewrite

- Short, searchable professional title (≤ 70 chars ideal)
- Include primary skill/role from profile
- No company names unless in source title

## work_experience[].description Rewrite

- Bullet list format (`- ` prefix)
- Responsibilities + achievements per role
- Keep «Stack:» line if present in source description
- One entry per profile `work_experience` item — same company count
- **Hard limit: ≤ 500 characters** (Upwork employment description field).
  Never hard-truncate mid-sentence. If over limit: rewrite — drop low-value
  details, shorten Stack/Achievements, tighten wording — until ≤ 500 with
  complete sentences.

## skills Rewrite

- Same skill names as profile (case may vary)
- Order by relevance to `profile_title`
- Do not add or remove tags

## portfolio_items Compose (from GitHub)

- Only for projects the user explicitly approved (see `portfolio-from-github.md`)
- Title and description from README / code facts — English, client-facing
- Skills ⊆ profile `skills` that appear in the repo (plus `UI/UX Design` when user owned product design)
- **Upwork UI: max 5 skills per card** — trim in fill-plan / `tmp/upwork-portfolio-draft.json` before browser fill
- Large multi-part project: pick representative skills (e.g. Castle Keepers → TypeScript, Vue.js, Node.js, NestJS, UI/UX Design); omit infra tags already in description
- Do not invent metrics, clients, or features absent from the repo

## Metadata for compose

Pass to CLI:

```json
{
  "rewrite_applied": {
    "overview": true,
    "profile_title": true,
    "work_experience_descriptions": true,
    "skills_tags": true
  },
  "intelligence_citations": ["upwork-help-profile-overview", "..."]
}
```
