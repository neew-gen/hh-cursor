# Data Model: Resume Intelligence

## SourceDescriptor

Represents one configured source used during a run.

**Fields**
- `id`: stable internal identifier
- `title`: human-readable source title
- `url`: live URL to fetch
- `source_class`: category such as `hh_help`, `vendor_doc`, `academic_research`,
  `career_media`, `career_center`, `resume_checker`
- `trust_tier`: `primary`, `secondary`, or `heuristic`
- `topics`: list of relevant topics such as `screening`, `keywords`, `formatting`,
  `parsing`, `ranking`

## SourceFetchResult

Represents the result of reading a source during a single run.

**Fields**
- `descriptor_id`: reference to `SourceDescriptor`
- `status`: `ok`, `unavailable`, or `empty`
- `fetched_at`: run timestamp
- `http_status`: optional response status
- `content_excerpt`: cleaned text or excerpt used for downstream synthesis
- `error_message`: optional failure reason

## EvidenceClaim

Represents one extracted signal from fetched content.

**Fields**
- `claim_text`: extracted or normalized claim
- `section`: target section such as `HowHRAndATSProcessResumesNow`, `WhatToWrite`,
  `HowToBuildResume`
- `confidence`: `high`, `medium`, or `low`
- `trust_tier`: copied from source
- `source_id`: reference to the originating source
- `topic`: supporting topic label

## RecommendationItem

Represents one final recommendation shown to the user.

**Fields**
- `recommendation_text`: actionable recommendation
- `target`: `content`, `format`, `structure`, `keywords`, or `screening`
- `rationale`: short explanation of why the recommendation appears
- `confidence`: `high`, `medium`, or `low`
- `supporting_sources`: list of source identifiers
- `conflict_note`: optional note if evidence is mixed

## ResumeIntelligenceReport

Represents the final generated artifact before rendering to Markdown.

**Fields**
- `summary_points`: top-level bullets
- `screening_findings`: current screening behavior notes
- `content_recommendations`: recommendations for what to write
- `format_recommendations`: recommendations for how to build the resume
- `conflicts`: explicit disagreements or low-confidence areas
- `source_inventory`: rendered view of source coverage
- `limitations`: missing coverage and run constraints
- `artifact_path`: final output path

## PipelineRun

Represents one end-to-end execution.

**Fields**
- `started_at`: run start timestamp
- `finished_at`: run end timestamp
- `requested_sources`: count of configured sources
- `successful_sources`: count of successfully fetched sources
- `failed_sources`: count of unavailable or empty sources
- `artifact_path`: output artifact path

## Relationships

- One `PipelineRun` includes many `SourceFetchResult` records.
- Each `SourceFetchResult` is derived from exactly one `SourceDescriptor`.
- One `SourceFetchResult` may produce many `EvidenceClaim` records.
- Many `EvidenceClaim` records are consolidated into each `RecommendationItem`.
- One `ResumeIntelligenceReport` belongs to exactly one `PipelineRun`.
