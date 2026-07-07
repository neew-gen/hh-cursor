# Research: Resume Intelligence

## Decision 1: Use a curated live source registry for MVP

**Decision**: The first version will fetch live content from a curated list of URLs rather
than attempting broad autonomous discovery.

**Rationale**: The feature needs current information, but fully open crawling would reduce
traceability, make runs unstable, and complicate review. A curated registry keeps scope
small while still allowing live evidence collection.

**Alternatives considered**:
- Open-ended web search on every run: rejected because results are unstable and harder to
  test.
- Static offline corpus in the repository: rejected because the user explicitly wants
  current information.

## Decision 2: Expand source classes beyond the initial user list

**Decision**: The MVP registry will include the user's source classes plus additional source
classes for academic research, career-center guidance, and specialized vendor documentation
on parsing, normalization, and scoring.

**Rationale**: The initial list is important but incomplete. It captures official guidance
and market commentary, but misses evidence layers that explain how screening actually works
or where vendor claims need grounding.

**Alternatives considered**:
- Keep only the user-provided source classes: rejected because it would leave the feature
  unable to verify whether the list is complete.
- Treat all sources equally: rejected because the trust model would become misleading.

## Decision 3: Rank sources by trust tier

**Decision**: Every source will be labeled `primary`, `secondary`, or `heuristic`.

**Rationale**:
- `primary` sources provide the strongest evidence for current screening mechanics.
- `secondary` sources provide interpretation and practical recruiter context.
- `heuristic` sources provide potentially useful but lower-accountability advice.

**Alternatives considered**:
- Binary trusted/untrusted split: rejected because it cannot represent useful but weaker
  evidence.
- No ranking at all: rejected because the final guidance would overstate certainty.

## Decision 4: Keep output as structured Markdown for MVP

**Decision**: The only required output for the first release is
`artifacts/resume-intelligence.md`.

**Rationale**: `Markdown` is readable by humans, easy for Cursor to reuse, and sufficient
for a deterministic single-artifact workflow.

**Alternatives considered**:
- Require both `JSON` and `Markdown`: rejected for MVP because it increases surface area
  without immediate user benefit.
- Return guidance only in chat: rejected because the artifact must be reusable later.

## Decision 5: Use deterministic extraction and synthesis rules

**Decision**: The MVP will rely on deterministic text extraction and rule-based synthesis
instead of model-generated freeform summarization.

**Rationale**: This repository currently has no model runtime or service layer. A
deterministic approach is easier to review, test, and evolve from a small baseline.

**Alternatives considered**:
- LLM synthesis at runtime: rejected because it introduces additional dependencies and
  harder-to-test variability.
- Manual annotations only: rejected because it would remove the live-run value of the
  feature.

## Decision 6: Surface conflicts explicitly

**Decision**: Contradictory advice from different sources will be represented in a dedicated
`SourceQualityAndConflicts` section instead of being silently merged into a single
recommendation.

**Rationale**: Hiring guidance is noisy, vendor claims are often marketing-heavy, and even
recruiter advice can diverge across markets. Surfacing conflicts preserves user trust.

**Alternatives considered**:
- Suppress minority views: rejected because it would falsely increase confidence.
- Dump all raw excerpts only: rejected because the user also needs a synthesized output.
