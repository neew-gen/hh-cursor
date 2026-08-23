# Research: Upwork Intelligence

## Decision 1: Use a curated live Upwork source registry for MVP

**Decision**: The first version will fetch live content from three curated Upwork URLs rather
than attempting broad autonomous discovery.

**Rationale**: Upwork guidance is spread across Help Center and editorial resources. A
small curated registry keeps runs stable, testable, and traceable.

**Alternatives considered**:
- Open-ended web search on every run: rejected because results are unstable.
- Static offline corpus only: rejected because the user wants current public guidance.

## Decision 8: Browser Tab cache is the primary Upwork fetch path

**Decision**: Agent opens each registry URL in Browser Tab, extracts `innerText`, stores
normalized text in `tmp/upwork-intelligence-sources/<source-id>.txt` via `ingest-text`,
then runs `cli run --sources-dir`.

**Rationale**: Upwork Help and Resources return HTTP 403 to `urllib` fetch (verified
2026-08). Browser Tab matches constitution browser-first and succeeds on the same URLs.

**Alternatives considered**:
- HTTP-only CLI: rejected — consistently 403 in practice.
- User manual paste in chat: rejected — not reproducible; cache files are automatable.

## Decision 2: Primary sources are Upwork Help plus Upwork Resources

**Decision**: Registry sources are:
- `upwork-help-proposals` — Upwork Help: How to submit a proposal on Upwork
- `upwork-beginners-guide` — Upwork Resources beginner guide
- `upwork-profile-tips` — Upwork Resources profile tips article

**Rationale**: These are first-party Upwork sources with direct guidance on proposals,
profile setup, and platform workflows.

## Decision 3: Profile blocks to emphasize in synthesis

**Decision**: Profile guidance will focus on observable Upwork profile blocks:
- profile photo
- title/headline (up to ~70 characters in public guidance)
- overview/bio
- skills
- employment history
- portfolio and profile highlights
- testimonials/certifications where mentioned
- profile completeness / visibility signals

**Rationale**: These blocks appear consistently across beginner and profile-tip resources
and are what clients see alongside proposals.

## Decision 4: Proposal limits and structure signals

**Decision**: Synthesis will treat proposals as short, job-specific cover letters with:
- personalized opening tied to the job post
- restated client goals
- relevant proof via profile highlights/portfolio
- screening-question answers when required
- optional Connects boost as a visibility mechanic, not a content-quality substitute
- concise length guidance from editorial sources (roughly a few short paragraphs)

**Rationale**: Upwork Help and Resources emphasize personalization and proof over long
generic letters.

## Decision 5: Uma synergy and video interview edge case

**Decision**: When source text mentions Uma, synthesis will recommend a draft-first workflow:
use Uma to summarize the job post or generate a starting draft, then manually personalize
proof, tone, and next steps. The artifact must note that Uma availability, usage limits,
and embedded workflows (including possible video-interview or in-flow assistance changes)
can evolve independently of editorial articles.

**Rationale**: Help articles reference Uma for proposal drafting, but product behavior and
plan limits change faster than resource pages. Treating AI output as editable draft
reduces overconfidence.

**Edge case**: If a client or job flow introduces Uma-assisted interview steps, the
artifact should warn that live product behavior must be verified at apply time; this
feature does not execute or validate those UI flows.

## Decision 6: Keep output as structured Markdown for MVP

**Decision**: The only required output for the first release is
`artifacts/upwork-intelligence.md`.

**Rationale**: Markdown is readable, diffable, and easy for Cursor agents to reuse in
features 007/008.

## Decision 7: Surface conflicts explicitly

**Decision**: Contradictory or partial AI guidance will appear in
`SourceQualityAndConflicts` instead of being silently merged.

**Rationale**: Upwork editorial content optimizes for conversion, while client behavior
varies by category and competition.
