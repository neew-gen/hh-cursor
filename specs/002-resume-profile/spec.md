# Feature Specification: Resume Profile Collection

**Feature Branch**: `002-resume-profile`

**Created**: 2026-07-08

**Status**: Draft

**Input**: User description: "Сбор данных для заполнения резюме на hh.ru: опциональная ссылка на резюме hh.ru, gap-опросник по полям формы hh, один YAML-артефакт `artifacts/resume-profile/<target-role-slug>.yaml`. Без resume-intelligence и без генерации резюме."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Questionnaire Without Link (Priority: P1)

Как пользователь, я прохожу опросник, пропускаю ссылку на резюме hh.ru и отвечаю на
вопросы только по обязательным полям формы hh.ru, чтобы получить файл с данными для
следующего шага заполнения резюме.

**Why this priority**: Минимальный путь без Browser Tab и без существующего резюме на hh.

**Independent Test**: Пройти опросник без ссылки и убедиться, что создан
`artifacts/resume-profile/<target-role-slug>.yaml` с `input_mode: questionnaire_only` и заполненными
required-полями hh MVP.

**Acceptance Scenarios**:

1. **Given** пользователь пропускает Q1 (ссылку на резюме), **When** он отвечает на
   gap-вопросы по должности, опыту, навыкам и образованию, **Then** система создаёт
   `artifacts/resume-profile/<target-role-slug>.yaml` с provenance `from_user_answer` для собранных полей.
2. **Given** пользователь указывает «нет опыта работы», **When** опросник завершён,
   **Then** артефакт содержит `work_experience_status: none` и пустой `work_experience`.

---

### User Story 2 - Prefill From Resume Link (Priority: P2)

Как пользователь, я даю ссылку на своё резюме hh.ru, система извлекает данные через
Browser Tab и задаёт вопросы только по незаполненным обязательным полям.

**Why this priority**: Сокращает ручной ввод, если резюме уже есть на hh.

**Independent Test**: Дать валидную ссылку (после ручного login при необходимости) и
убедиться, что часть полей имеет `from_resume_link`, а gap-вопросы покрывают только пробелы.

**Acceptance Scenarios**:

1. **Given** пользователь вводит ссылку на резюме hh.ru и страница доступна,
   **When** агент открывает страницу, нажимает `Скачать`, выбирает `Простой текст · txt`
   и обрабатывает полученный `resume_converter/...type=txt` документ как HTML,
   **Then** артефакт предзаполняется должностью, опытом, навыками и образованием
   где они присутствуют в скачанном документе.
2. **Given** извлечение частичное, **When** определяются пробелы, **Then** пользователю
   задаются gap-вопросы только по пустым required-полям hh MVP.

---

### User Story 3 - Artifact Ready For hh Form Fill (Priority: P3)

Как пользователь, я получаю артефакт, поля которого соответствуют блокам формы hh.ru,
чтобы на следующем шаге (фича 003) агент мог заполнить резюме без дополнительных вопросов.

**Why this priority**: Завершает ценность сбора данных — готовый вход для fill workflow.

**Independent Test**: Проверить, что YAML содержит все required MVP-поля hh и не содержит
полей, отсутствующих в форме hh (например, отдельных key_phrases).

**Acceptance Scenarios**:

1. **Given** сбор завершён успешно, **When** пользователь открывает
   `artifacts/resume-profile/<target-role-slug>.yaml`, **Then** файл содержит `target_role`,
   `work_experience` или `work_experience_status: none`, `skills.hard`, `education` или
   `no_formal_education: true`, а также метаданные `collected_at`, `input_mode`,
   `limitations`.
2. **Given** required-поле не заполнено, **When** пользователь пытается завершить сбор,
   **Then** система не записывает финальный артефакт и переспрашивает по этому полю.

---

### Edge Cases

- В `artifacts/resume-profile/` нет ни одного сохранённого профиля — вопрос про новый/дополняемый набор навыков не задаётся, сбор начинается как brand-new profile.
- Пользователь пропускает Q1 — сбор только через gap-опросник.
- Пользователь выбрал ввод ссылки в Q1, но сама ссылка не попала в ответ формы — агент принимает URL следующим обычным сообщением без повторного Q1.
- После выбора `Ввести ссылку на ваше резюме` агент не показывает вторую форму; допустим только обычный текстовый prompt с просьбой вставить ссылку следующим сообщением.
- Ссылка битая или не hh.ru — сообщение об ошибке, предложение skip или новой ссылки.
- Login/captcha на hh.ru — пауза, пользователь логинится вручную, агент продолжает.
- hh.ru download по кнопке `Простой текст · txt` возвращает HTML-документ, а не plain text — парсер обязан обрабатывать его как download HTML.
- Частичное извлечение по ссылке — gap-вопросы по пустым required-полям.
- «Нет опыта работы» — допустимо с явным флагом `work_experience_status: none`.
- Пустой ответ на required gap-вопрос — артефакт не создаётся, переспрос.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST ask Q1 for an optional hh.ru resume link; user MUST be able to paste the link in the same reply to Q1, and skip MUST be allowed.
- **FR-002**: System MUST extract resume fields from hh.ru via Browser Tab when a valid
  link is provided.
- **FR-002a**: When extracting from hh.ru, the system MUST use the resume page download flow
  (`Скачать` -> `Простой текст · txt`) and follow the resulting `resume_converter/...type=txt`
  URL in the same authenticated browser session.
- **FR-002b**: The `type=txt` response from hh.ru MUST be treated as an HTML download document,
  not as plain text, when it contains the resume download markup.
- **FR-002c**: The HTML download parser MUST deterministically extract fields from stable resume
  blocks including role, specializations, work experience, education, skills, languages,
  and about-me when those blocks are present.
- **FR-003**: System MUST ask gap questions only for empty required hh.ru form fields,
  using wording aligned with hh.ru blocks.
- **FR-004**: System MUST NOT read or depend on feature 001 (`resume-intelligence`).
- **FR-005**: System MUST NOT generate or publish resume text on hh.ru (feature 003 scope).
- **FR-006**: System MUST write exactly one final artifact file to `artifacts/resume-profile/<target-role-slug>.yaml`.
- **FR-007**: System MUST record provenance per field: `from_resume_link`, `from_user_answer`,
  or `inferred`.
- **FR-008**: System MUST mirror hh.ru resume form blocks in artifact schema (no separate
  key_phrases or tools fields).
- **FR-009**: System MUST require MVP fields: `target_role`, `work_experience` or explicit
  no-experience status, `skills.hard`, `education` or `no_formal_education`.
- **FR-010**: System MUST pause and report when login or captcha blocks hh.ru access.
- **FR-011**: System MUST NOT store secrets, cookies, or credentials in repository artifacts.
- **FR-012**: Users MUST be able to run collection via documented Cursor skill workflow.
- **FR-013**: System MUST skip the skills-mode question and initialize a new draft automatically when no saved resume-profile artifacts exist.
- **FR-014**: If the user chooses the Q1 option to provide a link but the URL is not captured inside that same `AskQuestion` response, the system MUST accept the hh.ru resume link in the very next plain chat message without re-asking Q1 or showing any extra intermediary questionnaire step.
- **FR-015**: After the user chooses the Q1 option to provide a link, the system MUST use plain chat text for any immediate follow-up prompt requesting the URL and MUST NOT render a second `AskQuestion` for that handoff.

### Key Entities

- **ResumeProfile**: итоговый профиль пользователя, поля 1:1 с формой hh.ru.
- **WorkExperienceEntry**: одно место работы (компания, должность, период, описание).
- **SkillEntry**: навык с уровнем (basic/medium/advanced).
- **EducationEntry**: учебное заведение, специальность, год, степень.
- **GapField**: описание незаполненного required-поля и текст gap-вопроса.
- **CollectionRun**: один проход сбора (input_mode, timestamps, source counts).

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: После успешного сбора создаётся ровно один финальный файл `artifacts/resume-profile/<target-role-slug>.yaml`.
- **SC-002**: Артефакт содержит все required MVP-поля hh или явный флаг отсутствия опыта/
  образования.
- **SC-003**: При skip Q1 все собранные поля имеют provenance `from_user_answer`.
- **SC-004**: При успешном extract по ссылке хотя бы одно поле имеет
  `from_resume_link`.
- **SC-005**: В артефакте нет полей, отсутствующих в форме hh.ru (key_phrases, tools).

## Assumptions

- Следующий шаг (фича 003) заполнит форму hh.ru в Browser Tab, используя этот артефакт.
- Фича 001 остаётся в репозитории, но не участвует в runtime фичи 002.
- Контакты и зарплата optional в MVP; секреты не пишутся в артефакт.
- Извлечение с hh.ru browser-first; при наличии download HTML используется детерминированный
  парсинг HTML-блоков, fallback — детерминированный парсинг текста страницы, без LLM.
