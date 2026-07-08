# Quickstart: Resume Profile Collection

## Prerequisites

- Python 3.11+
- Cursor with Browser Tab enabled
- Skill: `.cursor/skills/resume-profile/SKILL.md`

## Agent Workflow

1. Run skill `/resume-profile` (or ask agent to collect resume profile data).
2. Agent should prefer `bootstrap`, which checks for saved artifacts and immediately creates `tmp/profile-draft.json` when none exist.
3. If `bootstrap` reports saved artifacts, answer the skills-mode question and optionally choose a profile to supplement.
4. Answer Q1 by either pasting the hh.ru resume link immediately in the same reply, or, if the form captured only the intent to provide a link, sending the URL in the very next chat message without any repeated Q1 step; skipping the step is also allowed.
5. If link provided: agent opens hh.ru in Browser Tab, clicks `Скачать`, chooses
   `Простой текст · txt`, follows the `resume_converter/...type=txt` URL, parses the
   returned HTML document, then merges extracted fields into the draft.
6. Answer gap questions until none remain.
7. Verify `artifacts/resume-profile/<target-role-slug>.yaml` exists.

## Recommended Start Command

```bash
PYTHONPATH=src python3 -m resume_profile.cli bootstrap \
  --output tmp/profile-draft.json
```

If `bootstrap` is unavailable, fall back to `has-artifacts` followed by `init-draft`.

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

Or omit `--output` to derive path from `target_role`.

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
