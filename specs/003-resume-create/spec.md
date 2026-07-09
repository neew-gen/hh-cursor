# Feature Specification: Resume Create for hh.ru

**Feature Branch**: `003-resume-create`

**Created**: 2026-07-09

**Status**: Draft

**Input**: User description: "Создание резюме на hh.ru из intelligence + profile"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Compose Fill Plan (Priority: P1)

Как пользователь, я выбираю сохранённый profile YAML, агент переписывает `about_me` и
описания опыта по рекомендациям resume-intelligence и сохраняет fill-plan, чтобы перед
заполнением hh.ru я мог проверить тексты.

**Why this priority**: Минимально ценный результат без Browser Tab — готовый артефакт
с улучшенными текстами и проверкой фактов.

**Independent Test**: CLI `compose` + `validate` на существующем profile YAML и
`artifacts/resume-intelligence.md` создаёт `artifacts/resume-create/<slug>.yaml` без
потери фактов (компании, даты, навыки).

**Acceptance Scenarios**:

1. **Given** profile YAML и intelligence MD доступны, **When** пользователь запускает
   compose, **Then** создаётся fill-plan с переписанными `about_me` и
   `work_experience[].description`.
2. **Given** fill-plan содержит компанию, отсутствующую в profile, **When** запускается
   validate, **Then** валидация не проходит и возвращает ошибки фактической целостности.

---

### User Story 2 - Create New Resume on hh.ru (Priority: P2)

Как пользователь, я выбираю «создать новое», агент открывает конструктор hh.ru в
Browser Tab и заполняет поля из fill-plan.

**Why this priority**: Основная ценность фичи — готовое резюме на hh.ru.

**Independent Test**: После skill-run форма содержит должность, навыки, опыт,
образование; агент остановился до публикации.

**Acceptance Scenarios**:

1. **Given** fill-plan валиден и режим `create_new`, **When** агент заполняет форму,
   **Then** обязательные блоки hh MVP заполнены из fill-plan.
2. **Given** форма заполнена, **When** агент завершает шаг, **Then** резюме не
   опубликовано автоматически — пользователь проверяет вручную.

---

### User Story 3 - Edit Existing Resume (Priority: P2)

Как пользователь, я выбираю «редактировать», агент открывает `resume_link` из профиля
и обновляет текстовые и структурные блоки из fill-plan.

**Why this priority**: Многие пользователи уже имеют резюме на hh.ru.

**Independent Test**: При наличии `resume_link` агент навигирует на страницу
редактирования, не создаёт дубликат.

**Acceptance Scenarios**:

1. **Given** profile содержит `resume_link`, **When** пользователь выбирает
   `edit_existing`, **Then** агент открывает URL редактирования, а не конструктор нового.
2. **Given** login/captcha на hh.ru, **When** агент обнаруживает блокер,
   **Then** workflow останавливается с запросом ручной аутентификации.

---

### User Story 4 - Blockers and Report (Priority: P3)

Как пользователь, я получаю краткий fill-report с перечнем заполненных секций и
пропусков после browser-fill.

**Why this priority**: Повышает прозрачность и завершает workflow.

**Independent Test**: После fill CLI `write-report` создаёт отчёт с секциями и статусами.

**Acceptance Scenarios**:

1. **Given** browser-fill завершён частично, **When** пишется отчёт,
   **Then** перечислены заполненные и пропущенные секции.
2. **Given** intelligence MD отсутствует, **When** пользователь продолжает,
   **Then** skill предупреждает и применяет дефолтные hh-правила переписывания.

---

### Edge Cases

- В `artifacts/resume-profile/` нет профилей — skill сообщает, что нужен шаг 002.
- `resume-intelligence.md` отсутствует — предложить запуск 001 или продолжить с дефолтами.
- Несколько profile YAML — AskQuestion выбора профиля.
- Нет `resume_link` — режим edit недоступен, только create.
- Login/captcha на hh.ru — пауза, ручная аутентификация.
- Даты в profile в русском формате — нормализация перед fill.
- Агент добавил факт, отсутствующий в profile — validate отклоняет fill-plan.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST read `artifacts/resume-profile/<slug>.yaml` as the sole source of facts.
- **FR-002**: System MUST read `artifacts/resume-intelligence.md` for text rewrite rules when available.
- **FR-003**: System MUST rewrite `about_me` and `work_experience[].description`; other fields MUST come from profile without invented facts.
- **FR-004**: System MUST ask fill mode: `create_new` | `edit_existing` when `resume_link` exists.
- **FR-005**: System MUST write fill-plan to `artifacts/resume-create/<slug>.yaml`.
- **FR-006**: System MUST fill hh.ru resume form via Browser Tab.
- **FR-007**: System MUST pause on login or captcha; MUST NOT store session secrets in repo artifacts.
- **FR-008**: System MUST NOT publish resume without explicit user action.
- **FR-009**: System MUST validate fill-plan factual integrity against source profile.
- **FR-010**: Users MUST be able to run workflow via documented Cursor skill `/resume-create`.
- **FR-011**: System MUST write fill-report after browser-fill attempt.
- **FR-012**: System MUST preserve intelligence source references in fill-plan metadata.

### Key Entities

- **FillPlan**: готовый к заполнению профиль с метаданными compose (режим, источники, rewrite flags).
- **IntelligenceBrief**: распарсенные секции `WhatToWrite` и `HowToBuildResume` из intelligence MD.
- **FormFieldMapping**: соответствие полей fill-plan шагам конструктора hh.ru.
- **FillReport**: итог browser-fill: заполненные секции, пропуски, blockers.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: После compose создаётся один файл `artifacts/resume-create/<slug>.yaml`.
- **SC-002**: Validate отклоняет fill-plan с компаниями или навыками, отсутствующими в profile.
- **SC-003**: При `create_new` агент заполняет MVP-блоки hh до остановки перед публикацией.
- **SC-004**: При `edit_existing` агент открывает `resume_link`, не создавая новое резюме.
- **SC-005**: Fill-report перечисляет статус каждой секции формы.

## Assumptions

- Шаг 001 (`resume-intelligence`) и шаг 002 (`resume-profile`) уже выполнены или их артефакты доступны локально.
- Публикация резюме — ручное действие пользователя после проверки.
- Переписывание текстов выполняет агент Cursor; Python обеспечивает структуру и валидацию.
- Адаптация под конкретную вакансию вне scope MVP.
