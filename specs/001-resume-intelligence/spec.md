# Feature Specification: Resume Intelligence

**Feature Branch**: `001-resume-intelligence`

**Created**: 2026-07-07

**Status**: Draft

**Input**: User description: "Нужно с помощью SDD и Spec Kit добавить функционал получения информации о том, как в текущий момент HR обрабатывают резюме, что лучше там писать и как лучше создавать резюме; проанализировать, являются ли перечисленные источники единственными; отразить это в механизме и описать использование в README."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Build Current Resume Intelligence Brief (Priority: P1)

Как пользователь, я запускаю фичу и получаю актуальный структурированный отчет о том,
как HR и ATS сейчас обрабатывают резюме, чтобы быстро понять текущую механику screening
без ручного изучения десятков источников.

**Why this priority**: Это минимально ценный результат, без которого фича не решает
основную задачу пользователя.

**Independent Test**: Запустить фичу на чистом репозитории и убедиться, что она создает
`artifacts/resume-intelligence.md` с секциями о текущем screening-процессе,
источниках, доверии и ограничениях.

**Acceptance Scenarios**:

1. **Given** доступна хотя бы часть живых внешних источников, **When** пользователь
   запускает фичу, **Then** система создает итоговый `Markdown`-отчет с блоком о том,
   как сейчас HR и ATS обрабатывают резюме.
2. **Given** часть источников недоступна или вернула ошибку, **When** пользователь
   запускает фичу, **Then** отчет все равно создается и явно показывает пробелы,
   ограничения и недоступные источники.

---

### User Story 2 - Get Actionable Resume Guidance (Priority: P2)

Как пользователь, я хочу получить конкретные рекомендации о том, что писать в резюме и
как его оформлять, чтобы на основе собранных сигналов улучшить собственное резюме.

**Why this priority**: После понимания общего процесса screening следующий шаг для
пользователя - применить выводы на практике.

**Independent Test**: Запустить фичу и убедиться, что итоговый отчет содержит отдельные
разделы `WhatToWrite` и `HowToBuildResume` с атомарными рекомендациями и ссылками на
источники.

**Acceptance Scenarios**:

1. **Given** система собрала сигналы из источников разного типа, **When** формируется
   итоговый отчет, **Then** рекомендации по содержанию резюме отделены от рекомендаций по
   структуре и оформлению.
2. **Given** среди источников есть противоречивые советы, **When** формируется отчет,
   **Then** спорные рекомендации помечаются как конфликтные или эвристические, а не
   выдаются как подтвержденный факт.

---

### User Story 3 - Reuse the Result in Cursor (Priority: P3)

Как пользователь, я хочу получить результат в стабильном формате, который можно сразу
использовать в следующих шагах Cursor, чтобы строить дальнейшие промпты, ревизии резюме
и автоматизации без ручной переработки отчета.

**Why this priority**: Это повышает ценность фичи в агентном workflow, но зависит от
того, что базовый отчет уже собран и полезен сам по себе.

**Independent Test**: Прочитать итоговый `Markdown`-файл и убедиться, что он имеет
предсказуемую структуру секций, пометки доверия, список источников и блок ограничений,
достаточные для повторного использования в следующем агентном шаге.

**Acceptance Scenarios**:

1. **Given** фича завершила сбор и синтез данных, **When** пользователь открывает
   `artifacts/resume-intelligence.md`, **Then** файл содержит стабильные секции
   `Summary`, `HowHRAndATSProcessResumesNow`, `WhatToWrite`, `HowToBuildResume`,
   `SourceQualityAndConflicts`, `Sources`, `FreshnessAndLimitations`.
2. **Given** пользователь хочет использовать результат в следующем промпте Cursor,
   **When** он передает содержимое итогового отчета, **Then** рекомендации остаются
   читаемыми, трассируемыми к источникам и пригодными для следующего шага без ручной
   нормализации структуры.

---

### Edge Cases

- Что происходит, если официальные источники `hh` недоступны, а вторичные источники
  доступны?
- Как система ведет себя, если vendor-источник описывает возможности ATS маркетингово,
  но без подтверждения из более сильных источников?
- Как система обрабатывает ситуацию, когда источник доступен, но на странице нет
  полезного текста для извлечения?
- Что происходит, если все живые источники временно недоступны?
- Как система помечает советы, которые актуальны для части рынка, но не подтверждаются
  для `hh`-сценариев напрямую?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST retrieve live information from a curated set of external sources
  relevant to resume screening, resume writing, and ATS or recruiter behavior.
- **FR-002**: System MUST classify each source by source type and trust tier.
- **FR-003**: System MUST analyze whether the initial source list is sufficient and MUST
  include additional source classes when they materially improve coverage of the topic.
- **FR-004**: System MUST synthesize findings into a single `Markdown` artifact at
  `artifacts/resume-intelligence.md`.
- **FR-005**: System MUST separate the final artifact into stable sections for current
  screening behavior, content recommendations, resume construction guidance, source
  conflicts, source inventory, and limitations.
- **FR-006**: System MUST attach or preserve source references for derived guidance so the
  user can trace recommendations back to evidence.
- **FR-007**: System MUST distinguish between evidence-backed findings, lower-confidence
  heuristics, and unresolved conflicts across sources.
- **FR-008**: System MUST continue producing an artifact when some sources are unavailable,
  while explicitly reporting missing coverage and degraded confidence.
- **FR-009**: System MUST record run freshness so the user can judge whether the guidance
  reflects the current market context.
- **FR-010**: Users MUST be able to run the feature through a documented local workflow
  described in `README.md`.
- **FR-011**: System MUST keep final user-facing artifacts under `artifacts/`.
- **FR-012**: System MUST avoid storing secrets, session tokens, or private credentials in
  repository files or generated artifacts.

### Key Entities *(include if feature involves data)*

- **SourceDescriptor**: описывает источник, его тип, trust tier, URL, topical focus и
  expected contribution to the final report.
- **SourceFetchResult**: хранит результат чтения источника, статус, доступность,
  freshness data и извлеченный текст.
- **EvidenceClaim**: представляет конкретное утверждение или сигнал, найденный в
  источнике, с категорией и ссылкой на первоисточник.
- **RecommendationItem**: представляет рекомендацию по содержанию или построению резюме
  с обоснованием, trust label и supporting sources.
- **ResumeIntelligenceReport**: итоговый структурированный отчет, который объединяет
  сводку, guidance blocks, conflicts, source inventory и limitations.
- **PipelineRun**: отражает один запуск фичи, включая время выполнения, охват источников
  и итоговый artifact path.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: После одного запуска фича создает один итоговый файл
  `artifacts/resume-intelligence.md`.
- **SC-002**: Итоговый файл содержит все обязательные секции и как минимум один
  заполненный вывод в каждом из блоков `HowHRAndATSProcessResumesNow`, `WhatToWrite`,
  `HowToBuildResume`, если доступен хотя бы один релевантный источник.
- **SC-003**: Пользователь может определить уровень доверия для каждой ключевой
  рекомендации без обращения к исходному коду фичи.
- **SC-004**: При частичной недоступности источников итоговый файл все равно создается и
  явно перечисляет недоступные или слабые зоны покрытия.
- **SC-005**: Пользователь может использовать итоговый `Markdown`-отчет как вход в
  следующий шаг Cursor без ручного переформатирования структуры секций.

## Assumptions

- Первая версия фичи ориентируется на общие практики `hh`-релевантного рынка и не
  обещает точное моделирование внутренней логики конкретного работодателя.
- Внешние источники могут меняться, поэтому итоговый отчет отражает актуальность на
  момент запуска, а не постоянную истину.
- Для MVP допустимо использовать curated source registry вместо полностью автономного
  discovery всех возможных источников.
- Фича не выполняет автоматическую правку пользовательского резюме в первой версии; она
  формирует intelligence artifact, пригодный для следующих шагов.
