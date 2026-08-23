# Research: Upwork Proposal

## Upwork Proposal UI

- Job page has «Apply Now» or «Submit a Proposal»; layout varies by job type (hourly vs fixed).
- Proposal form includes cover letter textarea, screening questions, bid terms (rate/price, duration).
- Send button — must not be clicked in MVP.
- Connects cost shown before or during apply flow — checkpoint required.

## Profile Selection

- Upwork freelancer profile is single per account; `profile_match_hint` mirrors `target_role` from YAML.
- Specialty/title on Upwork should align with profile `target_role` (feature 006/008).

## Job Extract

- Public job pages may show partial content without login; full description often requires auth.
- On login wall during extract → pause per constitution.
- Screening questions may appear only on apply form — extract when visible or note in limitations.

## Proposal Validation Heuristics

- Extract employer names from profile `work_experience[].company`
- Flag proposal if it mentions company names not in profile (unless same as job client)
- Skills mentioned should be subset of profile skills (allow job terms as targets, not claims)
- EN proposal length: 300–5000 characters

## Selectors to Monitor

| Element | Primary selector | Fallback |
|---------|------------------|----------|
| Apply button | `aria-label` Apply / Submit a Proposal | button text |
| Cover letter | textarea in proposal form | largest textarea |
| Screening Q | label + following input/textarea | question blocks |
| Hourly rate | rate input field | bid section inputs |
| Connects | connects badge near apply | text «Connects» |
