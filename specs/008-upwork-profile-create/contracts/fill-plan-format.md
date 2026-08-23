# Contract: Fill Plan Format

**Artifact path**: `artifacts/upwork-profile-create/<profile-title-slug>.yaml`

Slug matches profile slug from `artifacts/upwork-profile/<slug>.yaml`.

## Compose Metadata (top-level, before profile fields)

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
  overview: true
  profile_title: true
  work_experience_descriptions: true
  skills_tags: true
```

## Profile Fields

Same schema as feature 006 upwork-profile artifact.

Rewritten fields:
- `overview` — agent-optimized bio
- `profile_title` — agent-optimized professional title
- `work_experience[].description` — agent-optimized bullets
- `skills` — agent-optimized tag list (same skill names, may reorder)

Structural fields MUST match source profile facts:
- companies, positions, dates, skill names, `hourly_rate`

### Optional: portfolio_items

Filled after US5 GitHub consent (see `portfolio-from-github.md`):

```yaml
portfolio_items:
  - title: "vue-use-api-call"
    description: "..."
    project_url: "https://github.com/example/vue-use-api-call"
    skills: ["Vue.js", "TypeScript"]
    source: github
    approved_by_user: true
```

Not required for compose/validate MVP; agent may keep draft in `tmp/upwork-portfolio-draft.json`.

## Completeness Rules

Fill-plan is **valid** when:

1. `profile_title` is non-empty.
2. `composed_at`, `source_profile`, `fill_mode`, `target_url` are set.
3. Factual integrity validator passes against `source_profile`.

## Excluded

- Proposal-specific tailoring fields
- Session cookies or auth tokens
