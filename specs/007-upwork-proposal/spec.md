# Feature Specification: Upwork Proposal

**Feature Branch**: `007-upwork-proposal`

**Created**: 2026-08-23

**Status**: Draft

**Input**: User description: "Submit tailored Upwork proposal with cover letter and screening answers"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Compose Proposal Plan (Priority: P1)

Как пользователь, я даю ссылку на Upwork job и выбираю сохранённый upwork-profile YAML;
агент извлекает описание вакансии, пишет proposal (EN) и сохраняет proposal-plan,
чтобы я мог проверить текст до отправки на Upwork.

**Why this priority**: Минимально ценный результат без browser-submit — готовое proposal
с проверкой фактов.

**Independent Test**: fixture `tests/fixtures/upwork-job-extract.json` + profile YAML → CLI
`compose` + `validate` создаёт `artifacts/upwork-proposal/<job-slug>.yaml` без Browser Tab.

**Acceptance Scenarios**:

1. **Given** URL job, profile YAML и job extract, **When** агент compose,
   **Then** proposal-plan содержит `cover_letter.text`, снимок job и screening answers.
2. **Given** cover letter содержит работодателя, отсутствующего в profile,
   **When** validate, **Then** валидация не проходит.

---

### User Story 2 - Browser Proposal Flow (Priority: P2)

Как пользователь, я запускаю proposal с готовым proposal-plan; агент открывает job,
заполняет cover letter, screening questions и contract terms (если есть).

**Why this priority**: Основная ценность — готовая форма proposal на Upwork.

**Independent Test**: После skill-run форма заполнена; кнопка Send не нажата; Connects checkpoint.

**Acceptance Scenarios**:

1. **Given** валидный proposal-plan, **When** агент заполняет форму,
   **Then** вставлен текст proposal и ответы на screening questions.
2. **Given** job требует Connects, **When** агент доходит до checkpoint,
   **Then** агент сообщает число Connects и останавливается до Send.
3. **Given** форма заполнена, **When** агент завершает шаг,
   **Then** proposal не отправлен автоматически — пользователь проверяет вручную.

---

### User Story 3 - Proposal Report (Priority: P3)

Как пользователь, я получаю proposal-report с перечнем выполненных шагов и blockers.

**Why this priority**: Прозрачность workflow и фиксация остановок.

**Independent Test**: После browser-fill создаётся `-report.yaml` с секциями и blockers.

**Acceptance Scenarios**:

1. **Given** browser-fill завершён, **When** write-report,
   **Then** отчёт содержит `job_opened`, `cover_letter_filled`, `screening_questions_filled`.
2. **Given** login/captcha, **When** агент обнаруживает блокер,
   **Then** workflow останавливается с записью в blockers.

---

### Edge Cases

- Job уже закрыт или пользователь уже applied — blocker, не перезаписывать.
- Пустой upwork-profile artifacts — стоп до запуска `/upwork-profile`.
- Job URL не с upwork.com — отклонить на входе.
- Screening questions на странице отличаются от extract — blocker, re-extract.
- Connects недостаточно — blocker с числом required vs available.
- Cover letter короче 300 или длиннее 5000 символов — validate fails до browser.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST accept Upwork job URL from user (upwork.com domain).
- **FR-002**: System MUST let user pick profile YAML from `artifacts/upwork-profile/`.
- **FR-003**: System MUST extract job title, client, description, budget_type, key_skills, screening_questions via Browser Tab.
- **FR-004**: System MUST generate EN proposal from profile facts and job context only.
- **FR-005**: System MUST validate proposal factual integrity against source profile.
- **FR-006**: System MUST save proposal-plan to `artifacts/upwork-proposal/<job-slug>.yaml`.
- **FR-007**: System MUST fill proposal form: cover letter, screening answers, optional contract terms.
- **FR-008**: System MUST stop before Send; user submits manually.
- **FR-009**: System MUST checkpoint Connects cost before Send.
- **FR-010**: System MUST use `artifacts/upwork-intelligence.md` for style guidance when available.

### Key Entities

- **JobSnapshot**: extracted job posting data
- **ProposalCoverLetter**: EN proposal body (300–5000 chars)
- **ScreeningAnswer**: question/answer pair
- **ProposalPlan**: composed artifact for browser fill
- **ProposalReport**: browser workflow outcome

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: User can compose and validate proposal-plan without browser in under 2 minutes.
- **SC-002**: Validator catches invented employers/skills with zero false negatives on fixture set.
- **SC-003**: Browser flow fills form and stops before Send in 100% of successful runs.
- **SC-004**: Connects checkpoint reported before any Send attempt.

## Assumptions

- Upwork profile YAML follows same structure as resume-profile (feature 006).
- Proposals written in English by default for Upwork marketplace.
- User has Upwork account with sufficient Connects when applying.
