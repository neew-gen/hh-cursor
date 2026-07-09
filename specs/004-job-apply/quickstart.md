# Quickstart: Job Apply for hh.ru

## Prerequisites

1. At least one profile: `artifacts/resume-profile/<slug>.yaml` (run `/resume-profile`)
2. Published resume on hh.ru matching `target_role` (run `/resume-create` or publish manually)
3. Optional: `artifacts/resume-intelligence.md` (feature 001)

## Agent Workflow

1. Run `/job-apply` with vacancy URL or answer the URL question
2. Pick profile if multiple exist
3. Agent extracts vacancy, writes cover letter, composes application-plan
4. Agent fills hh.ru response form — stops before submit
5. Review artifacts and submit manually in browser

## CLI Commands

```bash
PYTHONPATH=src python3 -m job_apply.cli list-profiles

PYTHONPATH=src python3 -m job_apply.cli load-inputs \
  --profile artifacts/resume-profile/frontend-developer.yaml \
  --vacancy tmp/vacancy-extract.json

PYTHONPATH=src python3 -m job_apply.cli compose \
  --profile artifacts/resume-profile/frontend-developer.yaml \
  --vacancy tests/fixtures/vacancy-extract.json \
  --draft tmp/cover-letter-draft.json

PYTHONPATH=src python3 -m job_apply.cli validate \
  --input artifacts/job-apply/vacancy-12345678.yaml \
  --profile artifacts/resume-profile/frontend-developer.yaml

PYTHONPATH=src python3 -m job_apply.cli artifact-path \
  --vacancy-url "https://hh.ru/vacancy/12345678" \
  --company "ТехКомпания" \
  --title "Frontend-разработчик"

PYTHONPATH=src python3 -m job_apply.cli write-report \
  --application-plan artifacts/job-apply/vacancy-12345678.yaml \
  --sections tmp/application-sections.json
```

## Artifacts

| Path | Description |
|------|-------------|
| `artifacts/job-apply/<vacancy-slug>.yaml` | Application plan with cover letter |
| `artifacts/job-apply/<vacancy-slug>-report.yaml` | Browser apply report |
| `tmp/vacancy-extract.json` | Vacancy data from browser |
| `tmp/cover-letter-draft.json` | Agent-written cover letter draft |

## P1 Checkpoint (no browser)

```bash
PYTHONPATH=src python3 -m unittest tests.unit.test_job_apply_composer
```

Uses `tests/fixtures/vacancy-extract.json` and local profile YAML.
