# Quickstart: Resume Create

## Prerequisites

1. `artifacts/resume-intelligence.md` from feature 001 (optional but recommended)
2. `artifacts/resume-profile/<slug>.yaml` from feature 002
3. Browser Tab enabled in Cursor

## CLI

```bash
# List available profiles
PYTHONPATH=src python3 -m resume_create.cli list-profiles

# Load inputs (profile + intelligence summary)
PYTHONPATH=src python3 -m resume_create.cli load-inputs \
  --profile artifacts/resume-profile/frontend-developer-vue.yaml

# After agent rewrites texts into tmp/fill-draft.json:
PYTHONPATH=src python3 -m resume_create.cli compose \
  --profile artifacts/resume-profile/frontend-developer-vue.yaml \
  --draft tmp/fill-draft.json \
  --fill-mode create_new

# Validate factual integrity
PYTHONPATH=src python3 -m resume_create.cli validate \
  --input artifacts/resume-create/frontend-developer-vue.yaml \
  --profile artifacts/resume-profile/frontend-developer-vue.yaml

# Write fill report after browser session
PYTHONPATH=src python3 -m resume_create.cli write-report \
  --fill-plan artifacts/resume-create/frontend-developer-vue.yaml \
  --sections tmp/fill-sections.json
```

## Cursor Skill

```
/resume-create
```

Flow: select profile → choose create/edit → rewrite texts → validate → fill hh.ru form → report.

## Artifacts

| Path | Description |
|------|-------------|
| `artifacts/resume-create/<slug>.yaml` | Fill-plan ready for hh form |
| `artifacts/resume-create/<slug>-report.yaml` | Browser fill status report |

## Stop Points

- Login/captcha on hh.ru — authenticate manually, then continue
- Do not auto-publish — review form and publish yourself
