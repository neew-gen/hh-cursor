# hh-cursor

Project for automating work with **hh.ru** (HeadHunter) and **Upwork** via the Cursor agent.

## Setup

### Step 1. Install Cursor

Download and install [Cursor](https://cursor.com) — without it the agent and Browser Tab are unavailable.

### Step 2. Configure Browser Tab

1. Open **Cursor Settings** (`Cmd + ,` on macOS or `Ctrl + ,` on Windows/Linux).
2. Go to **Tools & MCP**.
3. Find **Browser Automation**.
4. Enable it and select **Browser Tab** mode.

### Step 3. Python (optional, for CLI)

Skills run via agent chat by default. For manual CLI debugging or tests:

- Python 3.11 or newer
- Set `PYTHONPATH=src` before `python3 -m ...` commands

## Local artifacts and privacy

Personal data (profiles, fill plans, proposals) is written under `artifacts/` and **gitignored** — do not commit those YAML files. Git shallow clones and drafts live in gitignored `tmp/`.

## Tests

```bash
PYTHONPATH=src python3 -m unittest discover -s tests/unit -p 'test_*.py'
```

## Skills

Skills run in order. Each next step builds on artifacts from the previous ones. To start, type the command in the agent chat.

### 001. `/resume-intelligence` (optional)

**Not required** — you do not need to run it on every cycle. Once is enough, or whenever you want to refresh recommendations.

Fetches current signals from the web about how HR and ATS process resumes, what to write, and how to format them. Output: `artifacts/resume-intelligence.md`. Used by `/resume-create` and `/job-apply` when the file exists.

### 002. `/resume-profile`

Collects user data for filling a resume on hh.ru. You can pass a link to your HeadHunter resume — the agent extracts data via Browser Tab. Or skip the link and answer step-by-step questions: the agent asks only for what is missing for required hh.ru form fields.

Output: `artifacts/resume-profile/<slug>.yaml` (slug from the target role, e.g. `frontend-developer.yaml`).

### 003. `/resume-create`

Creates or updates a resume on hh.ru from `/resume-profile` data. If `artifacts/resume-intelligence.md` exists, rewrites “About me” and experience descriptions using recommendations — without inventing facts. Then opens HeadHunter in Browser Tab and fills the form.

If the profile had a link to an existing resume, you can choose edit; otherwise a new one is created. The agent stops before publishing: you do the final save on hh.ru yourself.

Output: `artifacts/resume-create/<slug>.yaml` (fill-plan with texts and fill steps).

### 004. `/job-apply`

Applies to an hh.ru vacancy. Needs a vacancy URL and a profile from `/resume-profile`. The agent extracts requirements, writes a tailored cover letter (using `resume-intelligence` if present), and opens HeadHunter in Browser Tab: clicks “Откликнуться”, selects the resume, and pastes the letter.

Resume choice is remembered for later applications. The agent stops before send — you click “Отправить” yourself.

Output: `artifacts/job-apply/<vacancy-slug>.yaml` (application-plan with letter and vacancy snapshot).

## Upwork skills

A separate chain for Upwork. Artifacts do not overlap with hh.ru. Run in order.

### 005. `/upwork-intelligence` (optional)

Collects current guidance for Upwork profiles and proposals. **Upwork blocks direct HTTP (403)** — the agent opens help/resources in **Browser Tab**, caches text, and synthesizes a report. Output: `artifacts/upwork-intelligence.md`. Used by `/upwork-profile-create` and `/upwork-proposal`.

### 006. `/upwork-profile`

Collects data for an Upwork profile: optional `upwork.com/freelancers/...` link and a gap questionnaire for required fields (title, overview, skills, experience). Output: `artifacts/upwork-profile/<slug>.yaml`.

### 008. `/upwork-profile-create`

Creates or updates an Upwork profile from `/upwork-profile` using `upwork-intelligence`. Rewrites overview and experience without inventing facts, fills the form in Browser Tab. Stops before final Save.

Output: `artifacts/upwork-profile-create/<slug>.yaml`.

### 007. `/upwork-proposal`

Applies (proposal) to an Upwork job. Needs a job post URL and a profile from `/upwork-profile`. The agent extracts requirements, writes an English cover letter, answers screening questions, and fills the proposal form in Browser Tab. Stops before Send — Connects are charged only after your manual click.

Output: `artifacts/upwork-proposal/<job-slug>.yaml`.

## Generic skills

Platform-agnostic utilities — not tied to hh.ru or Upwork browser flows.

### 009. `/project-portfolio-extract`

Extracts **portfolio-ready text** from a GitHub URL, ZIP archive, or local project folder: `title`, `description`, `project_url`, `skills`. Shallow clone into gitignored `tmp/` is an internal step only.

Used by `/upwork-profile-create` for Portfolio fill (run 009 first, then 008 browser step). Output: `artifacts/project-portfolio-extract/<slug>.yaml`.

## Troubleshooting

### SSL errors

If fetch fails with `SSL: CERTIFICATE_VERIFY_FAILED`, on macOS with a Python.org build installing certificates often helps:

```bash
open "/Applications/Python 3.8/Install Certificates.command"
```

### Browser Automation and MCP

The built-in MCP `cursor-ide-browser` is not added to `.cursor/mcp.json` — it is enabled only via **Browser Automation** in Cursor settings (see Step 2 above).

---

## Русский

Проект для автоматизации работы с **hh.ru** и **Upwork** через агента Cursor.

### Настройка

#### Шаг 1. Установите Cursor

Скачайте и установите [Cursor](https://cursor.com) — без него агент и Browser Tab недоступны.

#### Шаг 2. Настройте Browser Tab

1. Откройте **Cursor Settings** (`Cmd + ,` на macOS или `Ctrl + ,` на Windows/Linux).
2. Перейдите в раздел **Tools & MCP**.
3. Найдите пункт **Browser Automation**.
4. Включите его и выберите режим **Browser Tab**.

#### Шаг 3. Python (опционально, для CLI)

Навыки по умолчанию запускаются из чата агента. Для ручной отладки CLI или тестов:

- Python 3.11 или новее
- Перед `python3 -m ...` задайте `PYTHONPATH=src`

### Локальные артефакты и приватность

Личные данные (профили, fill-plan, proposals) пишутся в `artifacts/` и **в .gitignore** — не коммитьте эти YAML. Shallow clone и черновики — в gitignored `tmp/`.

### Тесты

```bash
PYTHONPATH=src python3 -m unittest discover -s tests/unit -p 'test_*.py'
```

### Навыки

Навыки выполняются по порядку. Каждый следующий шаг опирается на артефакты предыдущих. Для запуска введите команду в чат с агентом.

#### 001. `/resume-intelligence` (опционально)

**Не обязателен** — запускать не нужно при каждом цикле. Достаточно один раз или когда хотите обновить рекомендации.

Собирает из интернета актуальные сигналы о том, как HR и ATS сейчас обрабатывают резюме, что в них лучше писать и как их оформлять. Результат — `artifacts/resume-intelligence.md`. Его используют `/resume-create` и `/job-apply`, если файл уже есть.

#### 002. `/resume-profile`

Собирает данные о пользователе для заполнения резюме на hh.ru. Можно передать ссылку на своё резюме на HeadHunter — агент извлечёт данные через Browser Tab. Или пропустить ссылку и ответить на вопросы по шагам: агент спросит только то, чего не хватает для обязательных полей формы hh.ru.

Результат — `artifacts/resume-profile/<slug>.yaml` (slug из целевой должности, например `frontend-developer.yaml`).

#### 003. `/resume-create`

Создаёт или обновляет резюме на hh.ru на основе данных из `/resume-profile`. При наличии `artifacts/resume-intelligence.md` переписывает «О себе» и описания опыта по рекомендациям — без выдумывания фактов. Затем открывает HeadHunter в Browser Tab и заполняет форму.

Если в профиле была ссылка на существующее резюме — можно выбрать редактирование; иначе создаётся новое. Агент останавливается до публикации: финальное сохранение на hh.ru делаете вы.

Результат — `artifacts/resume-create/<slug>.yaml` (fill-plan с текстами и планом заполнения).

#### 004. `/job-apply`

Откликается на вакансию hh.ru. Нужна ссылка на вакансию и профиль из `/resume-profile`. Агент извлекает требования вакансии, пишет сопроводительное письмо под вакансию (с учётом `resume-intelligence`, если есть) и открывает HeadHunter в Browser Tab: нажимает «Откликнуться», выбирает резюме и вставляет письмо.

Выбор резюме запоминается для следующих откликов. Агент останавливается до отправки — финальный клик «Отправить» делаете вы.

Результат — `artifacts/job-apply/<vacancy-slug>.yaml` (application-plan с письмом и снимком вакансии).

### Upwork-навыки

Отдельная цепочка для Upwork. Артефакты не пересекаются с hh.ru. Выполняйте по порядку.

#### 005. `/upwork-intelligence` (опционально)

Собирает актуальные рекомендации по заполнению профиля и написанию proposals на Upwork. **Upwork блокирует прямой HTTP (403)** — агент открывает help/resources во **Browser Tab**, кэширует текст и синтезирует отчёт. Результат — `artifacts/upwork-intelligence.md`. Используют `/upwork-profile-create` и `/upwork-proposal`.

#### 006. `/upwork-profile`

Собирает данные для профиля Upwork: опциональная ссылка на `upwork.com/freelancers/...` и gap-опросник по обязательным полям (title, overview, skills, опыт). Результат — `artifacts/upwork-profile/<slug>.yaml`.

#### 008. `/upwork-profile-create`

Создаёт или обновляет профиль на Upwork из `/upwork-profile` с учётом `upwork-intelligence`. Переписывает overview и описания опыта без выдумывания фактов, заполняет форму в Browser Tab. Останавливается до финального Save.

Результат — `artifacts/upwork-profile-create/<slug>.yaml`.

#### 007. `/upwork-proposal`

Отклик (proposal) на вакансию Upwork. Нужна ссылка на job post и профиль из `/upwork-profile`. Агент извлекает требования, пишет cover letter на английском, отвечает на screening questions и заполняет форму proposal в Browser Tab. Останавливается до Send — Connects списываются только после вашего ручного клика.

Результат — `artifacts/upwork-proposal/<job-slug>.yaml`.

### Общие навыки

Не привязаны к hh.ru или Upwork.

#### 009. `/project-portfolio-extract`

Достаёт **готовый текст для portfolio** из GitHub URL, ZIP или локальной папки: `title`, `description`, `project_url`, `skills`. Shallow clone в gitignored `tmp/` — внутренний шаг.

Используется в `/upwork-profile-create` для Portfolio (сначала 009, затем browser fill в 008). Результат — `artifacts/project-portfolio-extract/<slug>.yaml`.

### Устранение проблем

#### SSL ошибки

Если при fetch появляется ошибка вида `SSL: CERTIFICATE_VERIFY_FAILED`, для Python.org
сборки на macOS часто помогает установка сертификатов командой:

```bash
open "/Applications/Python 3.8/Install Certificates.command"
```

#### Browser Automation и MCP

Встроенный MCP `cursor-ide-browser` не добавляется в `.cursor/mcp.json` — он включается только через **Browser Automation** в настройках Cursor (см. шаг 2 выше).
