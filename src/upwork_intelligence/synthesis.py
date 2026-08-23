from __future__ import annotations

from datetime import datetime

from .models import RecommendationItem, SourceFetchResult, UpworkIntelligenceReport


THEMES = {
    "client_proposal_scan": {
        "keywords": ["skim", "first", "preview", "client", "review", "shortlist", "invite"],
        "target": "proposal_review",
        "section": "proposal_review",
        "text": "Clients often skim proposals quickly and compare cover letters against profile signals, so the opening lines and visible relevance matter more than long generic intros.",
    },
    "personalized_cover_letter": {
        "keywords": ["personal", "tailor", "custom", "specific", "job description", "cover letter"],
        "target": "proposal_content",
        "section": "proposal_content",
        "text": "Winning proposals are personalized to the job post: address the client's problem directly, restate key requirements in your own words, and avoid copy-paste templates.",
    },
    "relevant_proof": {
        "keywords": ["portfolio", "sample", "example", "relevant", "experience", "highlight", "profile highlights"],
        "target": "proposal_content",
        "section": "proposal_content",
        "text": "Attach or link only work that directly matches the posted job, using profile highlights, portfolio items, certificates, or past Upwork jobs as proof instead of listing unrelated credentials.",
    },
    "clear_next_step": {
        "keywords": ["call to action", "next step", "interview", "chat", "message", "conversation"],
        "target": "proposal_content",
        "section": "proposal_content",
        "text": "Close proposals with a clear next step, such as a short call, a clarifying question, or an invitation to review a specific sample, so the client knows how to continue.",
    },
    "uma_draft_synergy": {
        "keywords": ["uma", "ai", "draft", "generat", "tips", "mindful"],
        "target": "proposal_content",
        "section": "proposal_content",
        "text": "Uma can summarize the job post and suggest a starting draft, but the final proposal must still be edited for accuracy, tone, and job-specific proof; treat AI output as a draft, not a finished submission.",
    },
    "profile_storefront": {
        "keywords": ["storefront", "first impression", "profile", "stand out", "attract"],
        "target": "profile",
        "section": "profile",
        "text": "Your Upwork profile acts as a storefront that clients see before and after opening a proposal, so title, overview, portfolio, and completeness should reinforce the same positioning you claim in proposals.",
    },
    "title_and_overview": {
        "keywords": ["title", "headline", "overview", "bio", "keyword", "70 characters"],
        "target": "profile",
        "section": "profile",
        "text": "Use a specific keyword-rich title and a client-centric overview that explains who you help, what outcomes you deliver, and why your expertise fits the projects you pursue.",
    },
    "profile_completeness": {
        "keywords": ["complete", "100%", "photo", "skills", "employment", "portfolio", "testimonial"],
        "target": "profile",
        "section": "profile",
        "text": "A complete profile with photo, skills, work history, portfolio, and testimonials increases trust and makes proposal claims easier for clients to verify at a glance.",
    },
    "uma_profile_alignment": {
        "keywords": ["uma", "profile", "proposal", "match", "skills", "workflow"],
        "target": "profile",
        "section": "profile",
        "text": "When using Uma across profile and proposal workflows, keep skills, title, overview, and highlighted work aligned so AI-assisted drafts stay consistent with what clients can verify on your profile.",
    },
}

FALLBACKS = {
    "proposal_review": "Clients compare proposals against profile signals and skim for relevance, clarity, and proof before inviting freelancers to interview.",
    "proposal_content": "Write concise, job-specific cover letters that restate the client's goals, show relevant proof, and end with a clear next step.",
    "profile": "Build a complete, client-centric profile with a specific title, strong overview, portfolio proof, and skills that match the jobs you target.",
}


def _contains_any(text: str, keywords: list[str]) -> bool:
    lower = text.lower()
    return any(keyword.lower() in lower for keyword in keywords)


def _confidence_for_sources(sources: list[SourceFetchResult]) -> str:
    if any(source.descriptor.trust_tier == "primary" for source in sources):
        return "high"
    if any(source.descriptor.trust_tier == "secondary" for source in sources):
        return "medium"
    return "low"


def _rationale_for_sources(sources: list[SourceFetchResult]) -> str:
    primary_count = sum(1 for source in sources if source.descriptor.trust_tier == "primary")
    secondary_count = sum(1 for source in sources if source.descriptor.trust_tier == "secondary")
    if primary_count and secondary_count:
        return f"Synthesized from {primary_count} primary and {secondary_count} secondary sources"
    if primary_count:
        return f"Synthesized from {primary_count} primary source(s)"
    if secondary_count:
        return f"Synthesized from {secondary_count} secondary source(s)"
    return "Synthesized from heuristic evidence"


def _build_item(text: str, target: str, sources: list[SourceFetchResult]) -> RecommendationItem:
    return RecommendationItem(
        recommendation_text=text,
        target=target,
        rationale=_rationale_for_sources(sources),
        confidence=_confidence_for_sources(sources),
        supporting_sources=[source.descriptor.id for source in sources],
    )


def build_report(
    results: list[SourceFetchResult],
    artifact_path: str,
    generated_at: datetime,
) -> UpworkIntelligenceReport:
    report = UpworkIntelligenceReport(generated_at=generated_at, artifact_path=artifact_path)
    successful = [result for result in results if result.status == "ok"]
    failed = [result for result in results if result.status != "ok"]

    if successful:
        report.summary_points.append(
            f"Processed {len(successful)} live Upwork sources and preserved trust-ranked guidance in one reusable artifact."
        )
    else:
        report.summary_points.append(
            "No live sources were successfully processed; the artifact reflects fallback limitations only."
        )

    source_classes = sorted({result.descriptor.source_class for result in successful})
    if source_classes:
        report.summary_points.append(
            "Covered source classes: " + ", ".join(source_classes) + "."
        )

    matched_themes: dict[str, list[SourceFetchResult]] = {}
    for theme_name, theme in THEMES.items():
        theme_sources = [
            result for result in successful if _contains_any(result.text, theme["keywords"])
        ]
        if theme_sources:
            matched_themes[theme_name] = theme_sources

    proposal_review_items = [
        _build_item(theme["text"], theme["target"], matched_themes[theme_name])
        for theme_name, theme in THEMES.items()
        if theme["section"] == "proposal_review" and theme_name in matched_themes
    ]
    proposal_content_items = [
        _build_item(theme["text"], theme["target"], matched_themes[theme_name])
        for theme_name, theme in THEMES.items()
        if theme["section"] == "proposal_content" and theme_name in matched_themes
    ]
    profile_items = [
        _build_item(theme["text"], theme["target"], matched_themes[theme_name])
        for theme_name, theme in THEMES.items()
        if theme["section"] == "profile" and theme_name in matched_themes
    ]

    if not proposal_review_items:
        report.proposal_review_findings.append(
            RecommendationItem(
                recommendation_text=FALLBACKS["proposal_review"],
                target="proposal_review",
                rationale="Fallback summary due to sparse or unavailable source text",
                confidence="low",
                supporting_sources=[],
            )
        )
    else:
        report.proposal_review_findings.extend(proposal_review_items)

    if not proposal_content_items:
        report.proposal_recommendations.append(
            RecommendationItem(
                recommendation_text=FALLBACKS["proposal_content"],
                target="proposal_content",
                rationale="Fallback summary due to sparse or unavailable source text",
                confidence="low",
                supporting_sources=[],
            )
        )
    else:
        report.proposal_recommendations.extend(proposal_content_items)

    if not profile_items:
        report.profile_recommendations.append(
            RecommendationItem(
                recommendation_text=FALLBACKS["profile"],
                target="profile",
                rationale="Fallback summary due to sparse or unavailable source text",
                confidence="low",
                supporting_sources=[],
            )
        )
    else:
        report.profile_recommendations.extend(profile_items)

    primary_missing = [
        result.descriptor.id
        for result in failed
        if result.descriptor.trust_tier == "primary"
    ]
    if primary_missing:
        report.conflicts.append(
            "Primary sources unavailable during this run: " + ", ".join(primary_missing) + "."
        )

    uma_sources = [result for result in successful if _contains_any(result.text, ["uma", "ai"])]
    if uma_sources and len(uma_sources) < len(successful):
        report.conflicts.append(
            "Uma and AI-assisted drafting guidance appears in only part of the source set; treat AI suggestions as drafts and verify them against the live job post."
        )

    if successful:
        report.conflicts.append(
            "Upwork editorial guidance emphasizes visibility and conversion, but client behavior varies by category, budget, and competition level."
        )

    for result in results:
        channel = result.fetch_channel or "unknown"
        if result.status == "ok":
            report.source_notes.append(
                f"`{result.descriptor.id}` | {result.descriptor.trust_tier} | "
                f"{result.descriptor.source_class} | {channel} | {result.descriptor.url}"
            )
        else:
            reason = result.error_message or result.status
            report.source_notes.append(
                f"`{result.descriptor.id}` | {result.descriptor.trust_tier} | "
                f"{result.descriptor.source_class} | {channel} | unavailable | {reason}"
            )

    if failed:
        report.limitations.append(
            f"{len(failed)} source(s) were unavailable or unreadable during this run."
        )
    if failed and not any(result.fetch_channel == "browser_cache" for result in results):
        report.limitations.append(
            "Upwork blocks direct HTTP fetch (403) for help/resources pages; use Browser Tab cache via --sources-dir."
        )
    report.limitations.append(
        "Recommendations describe public Upwork guidance and do not guarantee invitation rates for every category or client."
    )
    report.limitations.append(
        "Uma availability, usage limits, and video-interview workflows can change; verify current product behavior before relying on AI-assisted drafts."
    )
    report.limitations.append(
        "Use the artifact as a current evidence brief, then tailor proposals and profile updates to each specific job post."
    )

    return report
