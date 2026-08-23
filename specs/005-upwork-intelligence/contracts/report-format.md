# Contract: Report Format

## Purpose

Define the stable structure of `artifacts/upwork-intelligence.md`.

## Output Path

- Default path: `artifacts/upwork-intelligence.md`

## Required Sections

1. `# Upwork Intelligence`
2. `## Summary`
3. `## HowClientsReviewProposalsNow`
4. `## WhatToWriteInProposals`
5. `## HowToBuildProfile`
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
- Uma/AI guidance MUST be presented as editable draft workflow when mentioned.

## Source Reference Format

- Use stable inline references such as ``[`source-id`]`` or title plus URL rendering.
- The `Sources` section MUST map each source identifier to title, URL, class, and trust
  tier.

## Confidence Format

- Allowed values: `high`, `medium`, `low`
- Confidence labels MUST appear directly in findings or recommendations, not only in the
  source inventory.
