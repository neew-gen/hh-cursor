# Quickstart: Upwork Profile Collection

## Prerequisites

- Python 3.11+
- Cursor with Browser Tab enabled

## Agent Workflow

1. Initialize a new draft for every collection run.
2. Answer Q1: optional Upwork profile link or skip.
3. If link provided: open profile in Browser Tab, capture page text, run extract-text merge.
4. Answer gap questions until none remain.
5. Verify artifact exists in `artifacts/upwork-profile/`.

## Recommended Start Command

```bash
PYTHONPATH=src python3 -m upwork_profile.cli init-draft \
  --output tmp/upwork-profile-draft.json
```

## CLI

List gaps in draft JSON:

```bash
PYTHONPATH=src python3 -m upwork_profile.cli gaps --input tmp/upwork-profile-draft.json
```

Write final artifact:

```bash
PYTHONPATH=src python3 -m upwork_profile.cli write \
  --input tmp/upwork-profile-draft.json \
  --output artifacts/upwork-profile/<slug>.yaml
```

Or omit `--output` to derive path from `profile_title`.

Extract from page text snapshot:

```bash
PYTHONPATH=src python3 -m upwork_profile.cli extract-text \
  --input tmp/upwork-page-text.txt \
  --output tmp/upwork-profile-draft.json \
  --profile-link "https://www.upwork.com/freelancers/~01abc..."
```

Validate completeness:

```bash
PYTHONPATH=src python3 -m upwork_profile.cli validate --input tmp/upwork-profile-draft.json
```

Resolve artifact path:

```bash
PYTHONPATH=src python3 -m upwork_profile.cli artifact-path \
  --profile-title "Full Stack Developer"
```

## Tests

```bash
PYTHONPATH=src python3 -m unittest discover -s tests/unit -p 'test_upwork_profile_*.py'
```

## Expected Output

`artifacts/upwork-profile/<profile-title-slug>.yaml` with required MVP Upwork fields.
