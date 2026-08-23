# Research: Project Portfolio Extract

## Decision: Acquire vs extract vs compose

**Decision**: Three-layer pipeline — acquire (clone/unzip/path), extract (facts JSON), compose (portfolio fields).

**Rationale**: Clone is implementation detail; portfolio text is user-facing value. Agent composes `description`; CLI handles deterministic parsing.

## Decision: Temp paths

**Decision**: `tmp/github-clones/{owner}-{repo}/` and `tmp/project-unpacks/{slug}/`.

**Rationale**: `tmp/` already gitignored in hh-cursor.

## Decision: Stale threshold

**Decision**: ~2 years since last commit → flag as stale; require user approval.

**Rationale**: Aligns with user request; avoids outdated portfolio entries.

## Decision: Skill consent wording

**Decision**: User-facing message explains clone/ZIP read before any acquire.

**Rationale**: Transparent access to external/local code.

## Alternatives considered

- GitHub API: rejected for MVP (auth, rate limits).
- Browser-only README scrape: rejected; local clone gives fuller manifests.
- LLM inside CLI: rejected; agent in skill composes description for review.
