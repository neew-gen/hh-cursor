# Research: hh.ru Resume Field Mapping

**Feature**: 002-resume-profile | **Date**: 2026-07-08

## Sources

- [Как создать резюме на hh.ru (article/1628)](https://feedback.hh.ru/knowledge-base/article/1628)
- [Как отредактировать резюме (article/1896)](https://feedback.hh.ru/knowledge-base/article/1896)

## hh.ru Constructor Steps → Artifact Fields

| hh.ru step / block | Artifact field(s) | MVP required |
|--------------------|-------------------|--------------|
| Профессия | `target_role`, `specializations[]` | yes (role) |
| Образование | `education[]`, `no_formal_education` | yes |
| Ключевые навыки + уровень | `skills.hard[]` | yes |
| Опыт работы | `work_experience[]`, `work_experience_status` | yes |
| Условия (зарплата, формат) | `work_preferences` | no |
| Обо мне | `about_me` | no |
| Языки | `languages[]` | no |
| Доп. образование | `additional_education[]` | no |

## Download HTML Extract Heuristics

Observed hh.ru behavior for resume download:

- Clicking `Скачать` and selecting `Простой текст · txt` leads to a
  `resume_converter/...type=txt` URL.
- Despite the `txt` name, the response is a full HTML document with stable resume markup.
- Extraction should prefer this download HTML in the same authenticated browser session,
  because it preserves block structure better than a flattened page snapshot.

Deterministic parsing in `extractor.py` uses these blocks:

- **Role**: `.resume__position`
- **Specializations**: `.resume-profession-role`
- **Experience entries**: `.resume-experience`
- **Experience company**: `.resume-experience__company`
- **Experience position**: `.resume-experience__position`
- **Date / degree hints**: `.bloko-form-hint`
- **Education entry**: `.resume-education`
- **Education institution**: `.resume-education__name`
- **Skills / about-me content**: `.resume-skils__item`

## Page Text Fallback Heuristics

Deterministic regex/line parsing in `extractor.py`:

- **Role**: lines near «Желаемая должность», resume title heading.
- **Skills**: block after «Ключевые навыки» / «Навыки» — comma or bullet list.
- **Experience**: blocks with company + date range pattern `MMM YYYY — MMM YYYY` or «по настоящее время».
- **Education**: block after «Образование».

Extract is best-effort; gap detection fills missing required fields via questionnaire.

## Decisions

- **D1**: Artifact format YAML (stdlib writer, no PyYAML dependency).
- **D2**: Gap questions derived from `schema.py`, not hardcoded list.
- **D3**: Feature 001 excluded from runtime.
- **D4**: Agent skill drives UX; Python CLI validates/writes artifact.
- **D5**: Preferred extract source is download HTML from `resume_converter/...type=txt`;
  page-text parsing is fallback only when download HTML is unavailable.

## Alternatives Rejected

- Reading resume-intelligence for question hints — out of scope per user.
- urllib fetch of private resume — violates browser-first for hh.ru.
