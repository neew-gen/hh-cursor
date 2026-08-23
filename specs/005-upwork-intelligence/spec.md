# Feature Specification: Upwork Intelligence

**Feature Branch**: `005-upwork-intelligence`

**Created**: 2026-08-23

**Status**: Draft

**Input**: User description: "Собрать актуальные публичные сигналы Upwork о том, как клиенты оценивают proposals, что писать в cover letter и как строить freelancer profile, включая синергию с Uma AI; записать результат в переиспользуемый Markdown-артефакт."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Build Current Upwork Proposal Intelligence Brief (Priority: P1)

Как пользователь, я запускаю фичу и получаю актуальный структурированный отчет о том,
как клиенты сейчас просматривают proposals на Upwork, чтобы быстро понять механику
отбора без ручного чтения help-статей и ресурсов.

**Why this priority**: Это минимально ценный результат, без которого фича не решает
основную задачу пользователя.

**Independent Test**: Запустить фичу на чистом репозитории и убедиться, что она создает
`artifacts/upwork-intelligence.md` с секциями о текущем client review процессе,
источниках, доверии и ограничениях.

**Acceptance Scenarios**:

1. **Given** доступна хотя бы часть живых внешних источников Upwork, **When** пользователь
   запускает фичу, **Then** система создает итоговый `Markdown`-отчет с блоком о том,
   как клиенты сейчас оценивают proposals.
2. **Given** часть источников недоступна или вернула ошибку, **When** пользователь
   запускает фичу, **Then** отчет все равно создается и явно показывает пробелы,
   ограничения и недоступные источники.

---

### User Story 2 - Get Actionable Proposal and Profile Guidance (Priority: P2)

Как пользователь, я хочу получить конкретные рекомендации о том, что писать в proposals
и как оформлять Upwork profile, чтобы на основе собранных сигналов улучшить отклики и
конверсию в интервью.

**Why this priority**: После понимания client review следующий шаг — применить выводы к
cover letter и profile.

**Independent Test**: Запустить фичу и убедиться, что итоговый отчет содержит отдельные
разделы `WhatToWriteInProposals` и `HowToBuildProfile` с атомарными рекомендациями и
ссылками на источники.

**Acceptance Scenarios**:

1. **Given** система собрала сигналы из источников разного типа, **When** формируется
   итоговый отчет, **Then** рекомендации по proposals отделены от рекомендаций по profile.
2. **Given** среди источников есть советы про Uma AI, **When** формируется отчет,
   **Then** рекомендации по AI-assisted drafting описаны как draft-first workflow, а не
   как замена персонализации.

---

### User Story 3 - Reuse the Result in Cursor (Priority: P3)

Как пользователь, я хочу получить результат в стабильном формате, который можно сразу
использовать в следующих шагах Cursor для Upwork proposal/profile automation, без ручной
переработки отчета.

**Why this priority**: Это повышает ценность фичи в агентном workflow, но зависит от
того, что базовый отчет уже собран и полезен сам по себе.

**Independent Test**: Прочитать итоговый `Markdown`-файл и убедиться, что он имеет
предсказуемую структуру секций, пометки доверия, список источников и блок ограничений,
достаточные для повторного использования в следующем агентном шаге.

**Acceptance Scenarios**:

1. **Given** фича завершила сбор и синтез данных, **When** пользователь открывает
   `artifacts/upwork-intelligence.md`, **Then** файл содержит стабильные секции
   `Summary`, `HowClientsReviewProposalsNow`, `WhatToWriteInProposals`,
   `HowToBuildProfile`, `SourceQualityAndConflicts`, `Sources`,
   `FreshnessAndLimitations`.
2. **Given** пользователь хочет использовать результат в следующем промпте Cursor,
   **When** он передает содержимое итогового отчета, **Then** рекомендации остаются
   атомарными и снабжены confidence labels и source references.

---

### Edge Cases

- Все три источника недоступны — отчет создается с fallback-рекомендациями и явными
  ограничениями.
- Upwork возвращает HTTP 403 на прямой fetch — агент извлекает текст через Browser Tab,
  кэширует в `tmp/upwork-intelligence-sources/` и запускает `cli run --sources-dir`.
- Upwork Help возвращает paywall/login shell вместо текста — источник помечается как
  `unavailable` или `empty`, run не падает.
- Источники противоречат друг другу по длине cover letter или роли AI — конфликт
  фиксируется в `SourceQualityAndConflicts`.
- Uma/video interview workflow изменился после публикации help-статьи — ограничение
  freshness явно указано в `FreshnessAndLimitations`.
- Пользователь ограничивает `--max-sources` — отчет строится по доступному подмножеству
  registry без crash.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST collect live public content from a curated Upwork source registry;
  for Upwork domains, Browser Tab cache is the primary path when HTTP returns 403.
- **FR-002**: System MUST classify each source by trust tier and source class.
- **FR-003**: System MUST synthesize deterministic recommendations for proposal review,
  proposal writing, and profile building.
- **FR-004**: System MUST include Uma/AI synergy guidance when matching source text is
  available.
- **FR-005**: System MUST write a Markdown artifact to `artifacts/upwork-intelligence.md`
  by default.
- **FR-006**: System MUST continue artifact generation when individual sources fail.
- **FR-007**: System MUST expose a CLI with `list-sources`, `ingest-text`, and `run` with
  `--output`, `--max-sources`, `--timeout`, and `--sources-dir`.
- **FR-008**: System MUST NOT store credentials, cookies, or private session data in the
  repository.

### Key Entities

- **SourceDescriptor**: Curated Upwork URL with id, title, trust tier, topics.
- **SourceFetchResult**: Fetch status, cleaned text, and error metadata for one source.
- **RecommendationItem**: Atomic guidance with confidence, rationale, and source ids.
- **UpworkIntelligenceReport**: Structured synthesis result rendered to Markdown.
- **PipelineRun**: Run metadata including source success/failure counts.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: A user can generate `artifacts/upwork-intelligence.md` after Browser Tab
  cache ingest and one `run` command, without storing credentials in the repo.
- **SC-002**: The artifact contains all required sections from the report contract.
- **SC-003**: At least one recommendation in a successful run includes a confidence label
  and source reference.
- **SC-004**: A run with one or more failed sources still produces a complete artifact
  that documents degraded coverage.

## Assumptions

- Пользователь имеет интернет-доступ, Python 3.11+ и Browser Tab в Cursor.
- Upwork help/resources блокируют server-side HTTP (403); browser cache — основной путь.
- Фичи 007/008 (proposal/profile automation) будут читать артефакт опционально позже.
- Uma availability и usage limits могут меняться быстрее, чем editorial resources.
