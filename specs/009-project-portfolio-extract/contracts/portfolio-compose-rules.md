# Contract: Portfolio Compose Rules

Agent applies when writing `description` (and refining `title` / `skills`) from `ProjectFacts`.

## Language

- English, client-facing, professional
- 2–4 sentences or short bullet block (platform-dependent)

## Facts only

| Rule | Detail |
|------|--------|
| No invented metrics | Do not add user counts, revenue, team size unless in README |
| No fake clients | Do not name companies unless in repo |
| Skills | Subset of evidence from deps/stack; map to common portfolio tags (Vue.js, TypeScript). Artifact may list many skills; **Upwork fill (008) uses max 5 per card** — trim at compose or in `/upwork-profile-create` |
| Title | Short; prefer README H1 or package name; ≤ 70 chars |

## Description structure

1. What the project is (from summary/readme)
2. Your implied role if pet project ("Built...", "Open-source library...")
3. Stack highlight (1 line)
4. Optional outcome only if stated in README (tests, docs, demo)

## CLI vs agent

- CLI `compose-portfolio` may produce skeleton `description` from summary + stack
- Agent MUST review and polish before `write-artifact`
- User may preview before save

## Stale projects

Do not compose artifact unless user explicitly approved stale flag.
