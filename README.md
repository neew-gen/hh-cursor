# hh-cursor

Проект для автоматизации работы с hh.ru через агента Cursor.

## Как включить Browser Tab

1. Откройте **Cursor Settings** (`Cmd + ,` на macOS или `Ctrl + ,` на Windows/Linux).
2. Перейдите в раздел **Tools & MCP**.
3. Найдите пункт **Browser Automation**.
4. Включите его и выберите режим **Browser Tab**.

## Что делать при SSL ошибках

Если при fetch появляется ошибка вида `SSL: CERTIFICATE_VERIFY_FAILED`, для Python.org
сборки на macOS часто помогает установка сертификатов командой:

```bash
open "/Applications/Python 3.8/Install Certificates.command"
```

### Дополнительно

- Встроенный MCP `cursor-ide-browser` не добавляется в `.cursor/mcp.json` — он включается только через **Browser Automation**.

## Workflow: три шага

| Шаг | Skill | Артефакт |
|-----|-------|----------|
| 1 | resume-intelligence (CLI) | `artifacts/resume-intelligence.md` |
| 2 | `/resume-profile` | `artifacts/resume-profile/<slug>.yaml` |
| 3 | `/resume-create` | `artifacts/resume-create/<slug>.yaml` |

Подробнее: `specs/003-resume-create/quickstart.md`.
