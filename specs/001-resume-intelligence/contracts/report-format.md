# Contract: Report Format

## Purpose

Define the stable structure of `artifacts/resume-intelligence.md`.

## Output Path

- Default path: `artifacts/resume-intelligence.md`

## Required Sections

1. `# Resume Intelligence`
2. `## Summary`
3. `## HowHRAndATSProcessResumesNow`
4. `## WhatToWrite`
5. `## HowToBuildResume`
6. `## SourceQualityAndConflicts`
7. `## Sources`
8. `## FreshnessAndLimitations`

## Required Content Rules

- Each recommendation MUST be rendered as an atomic bullet or short paragraph.
- Recommendations MUST include source references.
- Recommendations MUST include confidence labels.
- Conflicts and heuristics MUST be clearly separated from higher-confidence findings.
- The report MUST include run freshness information.
- The report MUST include missing or unavailable source coverage when relevant.

## Source Reference Format

- Use stable inline references such as ``[`source-id`]`` or title plus URL rendering.
- The `Sources` section MUST map each source identifier to title, URL, class, and trust
  tier.

## Confidence Format

- Allowed values: `high`, `medium`, `low`
- Confidence labels MUST appear directly in findings or recommendations, not only in the
  source inventory.
