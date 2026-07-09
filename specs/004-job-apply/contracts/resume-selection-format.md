# Contract: Resume Selection Preference

Персистентный выбор резюме для browser apply. Файл в `tmp/` — локальная сессионная настройка пользователя, не коммитится.

## Path

`tmp/resume-selection.json`

## JSON Schema

```json
{
  "resume_title": "Frontend Developer",
  "resume_id": "abc123def4567890abcdef1234567890abcdef",
  "selected_at": "2026-07-09T16:30:00+00:00",
  "source": "user"
}
```

## Required Fields

| Field | Type | Notes |
|-------|------|-------|
| `resume_title` | string | Точное или отображаемое имя резюме на hh.ru (как в picker) |
| `resume_id` | string | ID резюме с hh.ru (`input[value]` в picker), если доступен |
| `selected_at` | ISO string | Момент сохранения |
| `source` | string | `user` — выбор пользователя; `single_available` — единственное резюме |

## Selection Rules (agent)

1. **Перед browser apply** прочитать `tmp/resume-selection.json`, если файл существует.
2. **Если preference есть** — выбрать в picker **только** это резюме (match по `resume_id`, иначе fuzzy по `resume_title`). **Не** подменять другим резюме из `resume_match_hint` / релевантности вакансии.
3. **Если preference нет** и в picker **несколько** резюме — `AskQuestion` (список названий). Не выбирать самостоятельно.
4. **Если preference нет** и резюме **одно** — использовать его; записать preference с `source: single_available`.
5. **После явного выбора пользователя** — записать/обновить `tmp/resume-selection.json`.
6. **Сброс** — только по явной просьбе пользователя («сбрось резюме», «выбери другое резюме», «смени резюме»): удалить файл или `cli clear-resume-selection`; затем снова п.3–4.

## CLI (optional helper)

```bash
PYTHONPATH=src python3 -m job_apply.cli show-resume-selection
PYTHONPATH=src python3 -m job_apply.cli clear-resume-selection
```

## Report Notes

В `application-sections.json` → `resume_selected.notes` указывать `resume_title` из preference.
