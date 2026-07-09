# Contract: Cover Letter Rules

Agent applies these when writing `cover_letter_text` in `tmp/cover-letter-draft.json`.

## Intelligence Input

Read from `artifacts/resume-intelligence.md`:

- `## WhatToWrite` — content recommendations
- Prefer bullets marked `[high]` confidence

If intelligence missing, use defaults below.

## Structure (mandatory)

0. **Greeting** (первая строка): «Добрый день,» или «Добрый вечер,» — по **локальному времени пользователя** на момент написания письма:
   - до 18:00 → «Добрый день,»
   - с 18:00 → «Добрый вечер,»
   - «Доброе утро» не использовать (только день / вечер)
1. **Hook** (1–2 предложения после приветствия): конкретный интерес к роли/компании — через мотив, продукт или задачу, без формального «отклика».
2. **Relevant experience** (2–3 bullets or short paragraphs): achievements from profile `work_experience` aligned with vacancy requirements.
3. **Fit** (1 paragraph): map profile `skills.hard` to vacancy `key_skills` / requirements.
4. **Call-to-action** (1 sentence): readiness to discuss; no begging tone.

## Length

- Target: 1200–2500 characters
- Maximum: 5000 characters (hh.ru typical limit)
- Minimum: 400 characters

## Constraints (always)

| Rule | Detail |
|------|--------|
| Facts only from profile | Companies, positions, dates, skills MUST exist in profile YAML |
| No new employers | Do not claim work at companies not in `work_experience` |
| No new skills | Skills mentioned must be in `skills.hard` or experience descriptions |
| No fake metrics | Only quantify if profile already implies scale |
| Vacancy keywords | Use vacancy requirements/skills vocabulary naturally |
| Language | Russian unless profile/vacancy explicitly English |
| Tone | Professional, specific; no «Уважаемые господа», no generic templates |
| Time-based greeting | Письмо **начинается** с «Добрый день,» или «Добрый вечер,» (см. Structure §0); без имени рекрутера |
| No application opener | После приветствия **не** писать «Откликаюсь на вакансию …», «Откликаюсь на позицию …» и аналоги с названием вакансии |

### Forbidden openings (examples)

Не использовать сразу после приветствия:

- «Откликаюсь на вакансию Frontend-разработчик в …»
- «Откликаюсь на позицию … в компании …»
- «Пишу по поводу вакансии …»

Вместо этого — зацепка: продукт, домен, стек, задача или ценность компании.

**Пример начала:** «Добрый день, меня заинтересовал ваш финтех-продукт …»

## HR Interest Criteria

Letter should make recruiter want to respond:

- Opens with time-appropriate greeting, then why **this** role at **this** company — без шаблона «откликаюсь на вакансию …»
- Shows 2–3 concrete proof points from real profile experience
- Demonstrates understanding of vacancy requirements
- Ends with confident, short CTA

## Draft JSON for compose

```json
{
  "cover_letter_text": "...",
  "language": "ru",
  "rewrite_applied": true,
  "intelligence_citations": ["hh-tailoring-resume"]
}
```

## Metadata for compose

`intelligence_citations` — source ids from intelligence used for style guidance.
