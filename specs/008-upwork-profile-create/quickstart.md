# Quickstart: Upwork Profile Create

## Prerequisites

1. `artifacts/upwork-intelligence.md` from feature 005 (optional but recommended)
2. `artifacts/upwork-profile/<slug>.yaml` from feature 006
3. Browser Tab enabled in Cursor

## CLI

```bash
# List available profiles
PYTHONPATH=src python3 -m upwork_profile_create.cli list-profiles

# Load inputs (profile + intelligence summary)
PYTHONPATH=src python3 -m upwork_profile_create.cli load-inputs \
  --profile artifacts/upwork-profile/senior-python-developer.yaml

# After agent rewrites texts into tmp/fill-draft.json:
PYTHONPATH=src python3 -m upwork_profile_create.cli compose \
  --profile artifacts/upwork-profile/senior-python-developer.yaml \
  --draft tmp/fill-draft.json \
  --fill-mode edit_existing

# Validate factual integrity
PYTHONPATH=src python3 -m upwork_profile_create.cli validate \
  --input artifacts/upwork-profile-create/senior-python-developer.yaml \
  --profile artifacts/upwork-profile/senior-python-developer.yaml

# Write fill report after browser session
PYTHONPATH=src python3 -m upwork_profile_create.cli write-report \
  --fill-plan artifacts/upwork-profile-create/senior-python-developer.yaml \
  --sections tmp/fill-sections.json
```

## Artifacts

| Path | Description |
|------|-------------|
| `artifacts/upwork-profile-create/<slug>.yaml` | Fill-plan ready for Upwork form |
| `artifacts/upwork-profile-create/<slug>-report.yaml` | Browser fill status report |

## Stop Points

- Login/captcha on Upwork — authenticate manually, then continue
- Do not auto-publish — review form and publish yourself
