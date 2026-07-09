# Feature Specification: Job Apply for hh.ru

**Feature Branch**: `004-job-apply`

**Created**: 2026-07-09

**Status**: Draft

**Input**: User description: "Отклик на вакансию hh.ru с адаптированным сопроводительным письмом"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Compose Application Plan (Priority: P1)

Как пользователь, я даю ссылку на вакансию и выбираю сохранённый profile YAML, агент
извлекает требования вакансии, пишет сопроводительное письмо и сохраняет application-plan,
чтобы я мог проверить текст до отклика на hh.ru.

**Why this priority**: Минимально ценный результат без полного browser-submit — готовое
письмо с проверкой фактов.

**Independent Test**: fixture `tests/fixtures/vacancy-extract.json` + profile YAML → CLI
`compose` + `validate` создаёт `artifacts/job-apply/<vacancy-slug>.yaml` без Browser Tab.

**Acceptance Scenarios**:

1. **Given** URL вакансии, profile YAML и vacancy extract, **When** агент compose,
   **Then** application-plan содержит `cover_letter.text`, снимок вакансии и метаданные.
2. **Given** cover letter содержит компанию-работодателя, отсутствующую в profile,
   **When** validate, **Then** валидация не проходит.

---

### User Story 2 - Browser Apply Flow (Priority: P2)

Как пользователь, я запускаю отклик с готовым application-plan, агент открывает вакансию,
нажимает «Откликнуться», выбирает резюме по `target_role` и вставляет сопроводительное.

**Why this priority**: Основная ценность — готовая форма отклика на hh.ru.

**Independent Test**: После skill-run форма отклика заполнена; кнопка «Отправить» не нажата.

**Acceptance Scenarios**:

1. **Given** валидный application-plan и сохранённый выбор в `tmp/resume-selection.json`,
   **When** агент заполняет форму отклика,
   **Then** выбрано резюме из preference, и вставлен текст письма.
2. **Given** preference отсутствует и на hh.ru несколько резюме,
   **When** агент доходит до picker,
   **Then** агент спрашивает пользователя и сохраняет выбор в `tmp/resume-selection.json`.
3. **Given** форма заполнена, **When** агент завершает шаг,
   **Then** отклик не отправлен автоматически — пользователь проверяет вручную.

---

### User Story 2b - Persistent Resume Choice (Priority: P2)

Как пользователь, я один раз выбираю резюме для откликов, и агент использует его во всех
следующих `/job-apply`, пока я явно не попрошу сбросить выбор и выбрать другое.

**Why this priority**: Исключает ошибочный автовыбор «похожего» резюме при серии откликов.

**Independent Test**: после выбора «Frontend Developer» и записи `tmp/resume-selection.json`
второй отклик выбирает то же резюме без повторного вопроса; после `clear-resume-selection`
агент снова спрашивает при нескольких резюме.

**Acceptance Scenarios**:

1. **Given** `tmp/resume-selection.json` с `resume_title: Frontend Developer`,
   **When** новый `/job-apply`,
   **Then** в picker выбрано именно это резюме, не другое с похожим названием.
2. **Given** preference отсутствует, на hh.ru 2+ резюме,
   **When** агент открывает форму отклика,
   **Then** `AskQuestion` с перечнем резюме до заполнения письма.
3. **Given** пользователь пишет «сбрось резюме» / «выбери другое резюме»,
   **When** агент обрабатывает запрос,
   **Then** `tmp/resume-selection.json` удалён и при следующем отклике выбор запрашивается заново.

---

### User Story 3 - Application Report (Priority: P3)

Как пользователь, я получаю application-report с перечнем выполненных шагов и blockers.

**Why this priority**: Прозрачность workflow и фиксация остановок.

**Independent Test**: После browser-fill создаётся `-report.yaml` с секциями и blockers.

**Acceptance Scenarios**:

1. **Given** browser-fill завершён, **When** write-report,
   **Then** отчёт содержит `vacancy_opened`, `resume_selected`, `cover_letter_filled`.
2. **Given** login/captcha, **When** агент обнаруживает блокер,
   **Then** workflow останавливается с записью в blockers.

---

### Edge Cases

- Вакансия уже закрыта или пользователь уже откликался — blocker, не перезаписывать.
- Нет опубликованного резюме на hh.ru, совпадающего с `target_role` — blocker, предложить `/resume-create`.
- Пустой profile artifacts — стоп до запуска `/resume-profile`.
- Vacancy URL не с hh.ru — отклонить на входе.
- Несколько резюме на hh.ru, preference не задан — не угадывать; спросить пользователя.
- Сохранённое резюме недоступно в picker (удалено/скрыто) — blocker, предложить сбросить preference.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST accept vacancy URL from user (hh.ru domain).
- **FR-002**: System MUST let user pick profile YAML when multiple profiles exist.
- **FR-003**: System MUST extract vacancy title, company, requirements, key skills via Browser Tab.
- **FR-004**: System MUST generate cover letter from profile facts and vacancy context only.
- **FR-005**: System MUST validate cover letter factual integrity against source profile.
- **FR-006**: System MUST save application-plan to `artifacts/job-apply/<vacancy-slug>.yaml`.
- **FR-007**: System MUST open vacancy, click respond, select resume per saved preference or user choice, fill cover letter.
- **FR-007a**: System MUST persist user-selected hh.ru resume in `tmp/resume-selection.json` until explicit reset.
- **FR-007b**: System MUST reuse saved resume for all subsequent applies without re-asking.
- **FR-007c**: System MUST NOT auto-pick among multiple hh.ru resumes by vacancy relevance or `resume_match_hint`.
- **FR-007d**: System MUST clear preference only on explicit user request to change resume.
- **FR-008**: System MUST NOT auto-submit the application response.
- **FR-009**: System MUST pause on login, captcha, or permission prompts.
- **FR-010**: System MUST write application-report after browser step.

### Key Entities

- **VacancySnapshot**: URL, title, company, requirements, key_skills, extracted_at.
- **ApplicationPlan**: vacancy + profile reference + cover_letter + metadata.
- **ApplicationReport**: section statuses, blockers, submitted=false.
- **ResumeSelectionPreference**: `resume_title`, `resume_id`, `selected_at`, `source` — `tmp/resume-selection.json`.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Пользователь получает application-plan с cover letter за один skill-run (P1).
- **SC-002**: Validate отклоняет письмо с выдуманным работодателем из profile.
- **SC-003**: После browser-fill форма отклика содержит текст письма; submit не выполнен.
- **SC-004**: При blocker (login, no resume match) workflow останавливается с понятным сообщением.
- **SC-005**: Серия откликов использует одно и то же резюме из `tmp/resume-selection.json` без повторного вопроса.

## Assumptions

- Пользователь авторизован на hh.ru или готов войти вручную при паузе.
- Резюме для отклика уже опубликовано на hh.ru (через `/resume-create` или вручную).
- Адаптация самого резюме под вакансию вне scope — только сопроводительное письмо.
- `resume-intelligence.md` опционален; при отсутствии применяются default rules.
