# Quickstart: Upwork Proposal

## Prerequisites

1. At least one profile: `artifacts/upwork-profile/<slug>.yaml` (run `/upwork-profile`)
2. Upwork account with published freelancer profile
3. Optional: `artifacts/upwork-intelligence.md` (feature 005)

## Agent Workflow

1. Run `/upwork-proposal` with job URL or answer URL question
2. Pick profile if multiple exist
3. Agent extracts job, writes EN proposal, composes proposal-plan
4. Agent fills Upwork proposal form — stops before Send; Connects checkpoint
5. Review artifacts and submit manually in browser

## CLI Commands

```bash
PYTHONPATH=src python3 -m upwork_proposal.cli list-profiles

PYTHONPATH=src python3 -m upwork_proposal.cli load-inputs \
  --profile tests/fixtures/upwork-profile-sample.yaml \
  --job tests/fixtures/upwork-job-extract.json

PYTHONPATH=src python3 -m upwork_proposal.cli compose \
  --profile tests/fixtures/upwork-profile-sample.yaml \
  --job tests/fixtures/upwork-job-extract.json \
  --draft tmp/proposal-draft.json

PYTHONPATH=src python3 -m upwork_proposal.cli validate \
  --input artifacts/upwork-proposal/job-0123456789abcdef.yaml \
  --profile tests/fixtures/upwork-profile-sample.yaml

PYTHONPATH=src python3 -m upwork_proposal.cli artifact-path \
  --job-url "https://www.upwork.com/jobs/~0123456789abcdef" \
  --client "TechStartup Inc" \
  --title "Senior Frontend Developer"

PYTHONPATH=src python3 -m upwork_proposal.cli write-report \
  --proposal-plan artifacts/upwork-proposal/job-0123456789abcdef.yaml \
  --sections tmp/proposal-sections.json
```

## Artifacts

| Path | Description |
|------|-------------|
| `artifacts/upwork-proposal/<job-slug>.yaml` | Proposal plan with cover letter |
| `artifacts/upwork-proposal/<job-slug>-report.yaml` | Browser proposal report |
| `tmp/upwork-job-extract.json` | Job data from browser |
| `tmp/proposal-draft.json` | Agent-written proposal draft |

## P1 Checkpoint (no browser)

```bash
PYTHONPATH=src python3 -m unittest tests.unit.test_upwork_proposal_composer tests.unit.test_upwork_proposal_validator
```

Uses `tests/fixtures/upwork-job-extract.json` and `tests/fixtures/upwork-profile-sample.yaml`.
