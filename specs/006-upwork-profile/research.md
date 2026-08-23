# Research: Upwork Profile Field Mapping

**Feature**: 006-upwork-profile | **Date**: 2026-08-23

## Sources

- [Upwork Help: Profile overview](https://support.upwork.com/hc/en-us/articles/211063358-Profile-overview)
- [Upwork Help: Skills](https://support.upwork.com/hc/en-us/articles/211063508-Skills)

## Upwork Profile Sections → Artifact Fields

| Upwork section | Artifact field(s) | MVP required |
|----------------|-------------------|--------------|
| Profile title | `profile_title` | yes |
| Overview | `overview` | yes |
| Hourly rate | `hourly_rate` | yes |
| Skills | `skills[]` | yes |
| Work history | `work_experience[]`, `work_experience_status` | yes |
| Education | `education[]` | no (gap asked when empty) |
| Portfolio | `portfolio_links[]` | no |

## Page Text Extract Heuristics

Deterministic regex/line parsing in `extractor.py`:

- **Title**: first heading lines or «Profile title» marker.
- **Overview**: block after «Overview» / «About me» / «Summary».
- **Rate**: `$NN` or «Hourly rate» marker.
- **Skills**: comma/bullet list after «Skills» / «Expertise».
- **Experience**: blocks with company + position + description after «Experience».
- **Education**: block after «Education» with institution and year.
- **Portfolio**: URLs in page text.

Extract is best-effort; gap detection fills missing required fields via questionnaire.

## Link Validation

Valid profile links match:

```
https://www.upwork.com/freelancers/<slug>
https://upwork.com/freelancers/<slug>
```

## Decisions

- **D1**: Artifact format YAML (stdlib writer, no PyYAML dependency).
- **D2**: Gap questions in English (`schema.GAP_QUESTIONS`).
- **D3**: Feature 005 excluded from runtime.
- **D4**: `skills` as plain string tags, not SkillEntry objects.
- **D5**: Shared `WorkExperienceEntry` / `EducationEntry` in `freelancer_core`.
- **D6**: `resume_profile` not refactored to use `freelancer_core` in this feature.
