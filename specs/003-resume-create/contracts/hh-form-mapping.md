# Contract: hh.ru Form Mapping

Maps fill-plan fields to hh.ru constructor blocks. Browser skill uses this table.

| fill_plan field | hh block | step | selector | fallback |
|-----------------|----------|------|----------|----------|
| `target_role` | Профессия | 1 | `[data-qa="resume-profession-input"]` | label «Профессия» |
| `specializations` | Специализации | 1 | `[data-qa="resume-specialization"]` | «Специализация» |
| `education` | Образование | 2 | `[data-qa="resume-education-add"]` | «Добавить образование» |
| `no_formal_education` | Нет образования | 2 | checkbox «Нет образования» | text match |
| `skills.hard` | Ключевые навыки | 3 | `[data-qa="skills-input"]` | «Ключевые навыки» |
| `work_experience` | Опыт работы | 4 | `[data-qa="resume-experience-add"]` | «Добавить место работы» |
| `work_preferences` | Условия | 5 | salary/format fields | optional |
| `about_me` | Обо мне | 6 | `[data-qa="resume-about-block"] textarea` | «Обо мне» |
| `languages` | Языки | 7 | language block | optional |

## Work Experience Sub-fields

| Sub-field | Form control |
|-----------|--------------|
| `company` | Company name input |
| `position` | Position input |
| `start_date` | Month/year start |
| `end_date` | Month/year end or «по настоящее время» |
| `description` | Duties textarea |
| `is_current` | «Работаю сейчас» checkbox |

## Skill Level Mapping

| fill-plan level | hh.ru label |
|-----------------|-------------|
| `basic` | Базовый |
| `medium` | Средний |
| `advanced` | Продвинутый |

## Date Normalization

Input may be `Июнь 2025`, `2025-06`, or `06.2025`. Mapper outputs `MM.YYYY` for form pickers.
