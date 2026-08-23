# Feature Specification: Upwork Profile Create

**Feature Branch**: `008-upwork-profile-create`

**Created**: 2026-08-22

**Status**: Draft

**Input**: User description: "Создание профиля на Upwork из intelligence + upwork-profile"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Compose Fill Plan (Priority: P1)

Как пользователь, я выбираю сохранённый upwork-profile YAML, агент переписывает `overview`,
`profile_title`, описания опыта и теги навыков по рекомендациям upwork-intelligence и
сохраняет fill-plan, чтобы перед заполнением Upwork я мог проверить тексты.

**Why this priority**: Минимально ценный результат без Browser Tab — готовый артефакт
с улучшенными текстами и проверкой фактов.

**Independent Test**: CLI `compose` + `validate` на существующем profile YAML и
`artifacts/upwork-intelligence.md` создаёт `artifacts/upwork-profile-create/<slug>.yaml` без
потери фактов (компании, даты, навыки).

**Acceptance Scenarios**:

1. **Given** profile YAML и intelligence MD доступны, **When** пользователь запускает
   compose, **Then** создаётся fill-plan с переписанными `overview`, `profile_title`,
   `work_experience[].description` и `skills`.
2. **Given** fill-plan содержит компанию, отсутствующую в profile, **When** запускается
   validate, **Then** валидация не проходит и возвращает ошибки фактической целостности.

---

### User Story 2 - Create or Edit Upwork Profile (Priority: P2)

Как пользователь, я выбираю «создать новое» или «редактировать», агент открывает профиль
Upwork в Browser Tab и заполняет поля из fill-plan.

**Why this priority**: Основная ценность фичи — готовый профиль на Upwork.

**Independent Test**: После skill-run форма содержит title, overview, skills, employment
history; агент остановился до публикации.

**Acceptance Scenarios**:

1. **Given** fill-plan валиден и режим `create_new`, **When** агент заполняет форму,
   **Then** обязательные блоки Upwork MVP заполнены из fill-plan.
2. **Given** форма заполнена, **When** агент завершает шаг, **Then** профиль не
   опубликован автоматически — пользователь проверяет вручную.

---

### User Story 3 - Edit Existing Profile (Priority: P2)

Как пользователь, я выбираю «редактировать», агент открывает `profile_link` из профиля
и обновляет текстовые блоки из fill-plan.

**Why this priority**: Многие пользователи уже имеют профиль на Upwork.

**Independent Test**: При наличии `profile_link` агент навигирует на страницу
редактирования, не создаёт дубликат.

**Acceptance Scenarios**:

1. **Given** profile содержит `profile_link`, **When** пользователь выбирает
   `edit_existing`, **Then** агент открывает URL редактирования, а не onboarding нового.
2. **Given** login/captcha на Upwork, **When** агент обнаруживает блокер,
   **Then** workflow останавливается с запросом ручной аутентификации.

---

### User Story 4 - Blockers and Report (Priority: P3)

Как пользователь, я получаю краткий fill-report с перечнем заполненных секций и
пропусков после browser-fill.

**Why this priority**: Повышает прозрачность и завершает workflow.

**Independent Test**: CLI `write-report` создаёт `artifacts/upwork-profile-create/<slug>-report.yaml`.

**Acceptance Scenarios**:

1. **Given** browser-fill завершён, **When** агент пишет report, **Then** файл содержит
   статусы секций `overview`, `profile_title`, `skills`, `work_experience`.

---

### User Story 5 - Portfolio from GitHub (Priority: P2)

Как пользователь, я даю ссылки на проекты (GitHub), агент предупреждает, что откроет
репозитории / клонирует код, я подтверждаю **какие** проекты парсить (устаревшие —
пропускаем или только с моего согласия), агент составляет тексты portfolio items и
заполняет секцию Portfolio на Upwork.

**Why this priority**: Portfolio — видимый блок профиля; ссылки из overview Upwork
блокирует, поэтому нужен отдельный шаг с анализом репозиториев.

**Independent Test**: После согласия и выбора проектов агент пишет draft portfolio
items с фактами из README/кода и останавливается до Save в модалке Portfolio.

**Acceptance Scenarios**:

1. **Given** пользователь ещё не дал ссылки, **When** агент доходит до Portfolio,
   **Then** агент предупреждает о доступе к GitHub/clone и просит ссылки — без парсинга.
2. **Given** несколько ссылок, часть старше ~2 лет без активности, **When** агент
   предлагает список, **Then** пользователь выбирает проекты; невыбранные не попадают
   в fill и на Upwork.
3. **Given** выбранный публичный репозиторий, **When** агент анализирует его,
   **Then** title/description/skills опираются только на факты репо и profile skills.

### Edge Cases

- Отсутствует `artifacts/upwork-intelligence.md` — compose работает с default rewrite rules.
- Отсутствует profile artifact — CLI возвращает ошибку; browser не открывается.
- Draft JSON с неверным числом `work_experience` — compose падает с ValueError.
- Skills в draft содержат новые теги — validate не проходит.
- Login wall / captcha на Upwork — агент останавливается, пользователь продолжает вручную.
- Приватный репозиторий без доступа — агент просит локальный путь или пропускает проект.
- Пользователь отказывается от GitHub-доступа — Portfolio step пропускается.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST compose fill-plan из upwork-profile YAML и agent draft JSON.
- **FR-002**: System MUST validate factual integrity fill-plan против source profile.
- **FR-003**: System MUST load upwork-intelligence MD sections WhatToWrite, HowToBuildProfile.
- **FR-004**: System MUST support fill modes `create_new` и `edit_existing`.
- **FR-005**: System MUST preserve intelligence citations в fill-plan metadata.
- **FR-006**: System MUST NOT auto-publish профиль на Upwork.
- **FR-007**: System MUST write fill-report после browser-fill.
- **FR-008**: System MUST получить согласие пользователя перед доступом к GitHub / clone / локальному репо для Portfolio.
- **FR-009**: System MUST спросить, какие проекты парсить; устаревшие (многолетняя неактивность) не размещать без явного выбора пользователя.
- **FR-010**: System MUST составлять portfolio items только из фактов выбранных репозиториев и profile `skills`.

### Key Entities

- **UpworkProfile**: факты пользователя (title, overview, experience, skills).
- **FillPlan**: profile + compose metadata + rewritten texts.
- **IntelligenceBrief**: parsed upwork-intelligence recommendations.
- **FillReport**: browser-fill status per section.
- **PortfolioItem**: title, description, project_url, skills — из одобренного GitHub-проекта.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: `compose` + `validate` проходит на sample profile без ошибок фактов.
- **SC-002**: Fill-plan содержит все 4 rewrite-поля: overview, profile_title, experience, skills.
- **SC-003**: Browser-fill останавливается до финального submit/publish.
- **SC-004**: 100% structural facts (companies, dates, skill names) совпадают с source profile.

## Assumptions

- Feature 006 (`upwork-profile`) предоставляет profile YAML в `artifacts/upwork-profile/`.
- Feature 005 (`upwork-intelligence`) предоставляет MD в `artifacts/upwork-intelligence.md`.
- Пользователь аутентифицирован на Upwork в Browser Tab при необходимости.
- Язык профиля — English, если не указано иное в profile.
