# Research: hh.ru Resume Constructor

**Feature**: 003-resume-create | **Date**: 2026-07-09

## Sources

- [Как создать резюме на hh.ru (article/1628)](https://feedback.hh.ru/knowledge-base/article/1628)
- [Как отредактировать резюме (article/1896)](https://feedback.hh.ru/knowledge-base/article/1896)
- Feature 002 research: `specs/002-resume-profile/research.md`

## Constructor Steps (create flow)

| Step | hh.ru block | Fill-plan fields |
|------|-------------|------------------|
| 1 | Профессия | `target_role`, `specializations` |
| 2 | Образование | `education`, `no_formal_education` |
| 3 | Ключевые навыки | `skills.hard` |
| 4 | Опыт работы | `work_experience`, `work_experience_status` |
| 5 | Условия | `work_preferences` (optional) |
| 6 | Обо мне | `about_me` |
| 7 | Языки | `languages` (optional) |

## Entry URLs

| Mode | URL pattern |
|------|-------------|
| List resumes | `https://hh.ru/applicant/resumes` |
| Create new | From list → «Создать резюме» button |
| Edit existing | `resume_link` from profile (e.g. `https://*.hh.ru/resume/<hash>`) → «Редактировать» |

## Observed UI Selectors (best-effort)

Selectors may change; skill uses snapshot fallback by visible labels.

| Block | Primary selector | Fallback |
|-------|------------------|----------|
| Create button | `[data-qa="resume-create-button"]` | text «Создать резюме» |
| Profession input | `[data-qa="resume-profession-input"]` | label «Профессия» |
| Specializations | `[data-qa="resume-specialization"]` | «Специализация» |
| Skills input | `[data-qa="skills-input"]` | «Ключевые навыки» |
| About me | `[data-qa="resume-about-block"] textarea` | «Обо мне» |
| Experience add | `[data-qa="resume-experience-add"]` | «Добавить место работы» |
| Education add | `[data-qa="resume-education-add"]` | «Добавить образование» |
| Save draft | `[data-qa="resume-save"]` | «Сохранить» |
| Publish | `[data-qa="resume-publish"]` | «Опубликовать» — **do not click in MVP** |

## Date Normalization

Profile artifacts may contain Russian month names (`Июнь 2025`). Mapper normalizes to
`MM.YYYY` for hh form month/year pickers where possible.

## Decisions

- **D1**: Fill-plan YAML reuses profile field schema plus compose metadata.
- **D2**: Text rewrite in agent; Python validates facts only.
- **D3**: Stop before publish — user confirms manually.
- **D4**: Intelligence optional — default rewrite rules in `contracts/rewrite-rules.md`.

## Alternatives Rejected

- urllib/API for form submit — violates browser-first constitution.
- Auto-publish — too risky without user review.
