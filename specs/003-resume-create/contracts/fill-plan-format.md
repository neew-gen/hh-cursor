# Contract: Fill Plan Format

**Artifact path**: `artifacts/resume-create/<target-role-slug>.yaml`

Slug matches profile slug from `artifacts/resume-profile/<slug>.yaml`.

## Compose Metadata (top-level, before or after profile fields)

| Field | Type | Required |
|-------|------|----------|
| `composed_at` | ISO-8601 string | yes |
| `source_profile` | string path | yes |
| `intelligence_path` | string \| null | no |
| `intelligence_freshness` | string \| null | no |
| `fill_mode` | `create_new` \| `edit_existing` | yes |
| `target_url` | string | yes |
| `rewrite_applied` | object | yes |
| `intelligence_citations` | string[] | no |

### rewrite_applied

```yaml
rewrite_applied:
  about_me: true
  work_experience_descriptions: true
```

## Profile Fields

Same schema as `specs/002-resume-profile/contracts/profile-format.md`.

Rewritten fields:
- `about_me` — agent-optimized text
- `work_experience[].description` — agent-optimized bullets

Structural fields MUST match source profile facts:
- `target_role`, companies, positions, dates, skill names, education institutions

## Completeness Rules

Fill-plan is **valid** when:

1. All profile completeness rules from feature 002 pass.
2. `composed_at`, `source_profile`, `fill_mode`, `target_url` are set.
3. Factual integrity validator passes against `source_profile`.

## Excluded

- Vacancy-specific tailoring fields
- Session cookies or auth tokens
