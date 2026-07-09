# Quickstart: Resume Profile Collection

## Prerequisites

- Python 3.11+
- Cursor with Browser Tab enabled
- Skill: `.cursor/skills/resume-profile/SKILL.md`

## Agent Workflow

1. Run skill `/resume-profile` (or ask agent to collect resume profile data).
2. Agent initializes a brand-new `tmp/profile-draft.json` for every run.
3. Answer Q1 by either pasting the hh.ru resume link immediately in the same reply, or, if the form captured only the intent to provide a link, sending the URL in the very next chat message without any repeated Q1 step; skipping the step is also allowed.
4. If link provided: agent opens hh.ru in Browser Tab, clicks `Скачать`, chooses
   `Простой текст · txt`, follows the `resume_converter/...type=txt` URL, parses the
   returned HTML document, then merges extracted fields into the draft.
5. Answer gap questions until none remain.
6. Verify a new artifact file exists in `artifacts/resume-profile/`.

## Recommended Start Command

```bash
PYTHONPATH=src python3 -m resume_profile.cli init-draft \
  --skills-mode new \
  --output tmp/profile-draft.json
```

## CLI (manual / agent-assisted)

List gaps in a draft JSON profile:

```bash
PYTHONPATH=src python3 -m resume_profile.cli gaps --input tmp/profile-draft.json
```

Write final artifact:

```bash
PYTHONPATH=src python3 -m resume_profile.cli write \
  --input tmp/profile-draft.json \
  --output artifacts/resume-profile/<slug>.yaml
```

Or omit `--output` to derive path from `target_role`. If that slug already exists, the write step
will create `(<n>)` suffixed filename instead of overwriting the previous artifact.

Parse downloaded resume HTML into draft:

```bash
PYTHONPATH=src python3 -m resume_profile.cli extract-text \
  --input tmp/resume-download.html \
  --output tmp/profile-draft.json \
  --resume-link "https://hh.ru/resume/..."
```

If download HTML is unavailable, the same command may be used with a page text snapshot as
fallback input.

Check completeness (JSON draft):

```bash
PYTHONPATH=src python3 -m resume_profile.cli validate --input tmp/profile-draft.json
```

## Tests

```bash
PYTHONPATH=src python3 -m unittest discover -s tests/unit -p 'test_*.py'
```

## Expected Output

`artifacts/resume-profile/<target-role-slug>.yaml` with required hh MVP fields and no `key_phrases` / `tools`.
