from __future__ import annotations

from datetime import datetime

from .models import RecommendationItem, ResumeIntelligenceReport, SourceFetchResult


THEMES = {
    "preview_screening": {
        "keywords": ["preview", "превью", "recruiter", "рекрутер", "invite", "приглаш"],
        "target": "screening",
        "section": "screening",
        "text": "HR сначала смотрят на быстрые сигналы из превью и верхних блоков резюме: должность, последний релевантный опыт, ключевые навыки и общую понятность профиля.",
    },
    "structured_parsing": {
        "keywords": ["parse", "parsing", "extract", "structured", "fields", "извлек", "структур"],
        "target": "screening",
        "section": "screening",
        "text": "ATS сначала разбирают резюме в структурированные поля, поэтому неочевидная верстка, лишний визуальный шум и нестандартные блоки ухудшают распознавание опыта, навыков и дат.",
    },
    "keyword_matching": {
        "keywords": ["keyword", "skills", "навык", "требован", "search", "filter"],
        "target": "content",
        "section": "content",
        "text": "Нужно прямо писать релевантные навыки, инструменты и формулировки из вакансии, потому что и ATS, и рекрутеры сопоставляют резюме с требованиями по ключевым сигналам.",
    },
    "achievement_focus": {
        "keywords": ["achievement", "result", "достиж", "результат", "impact", "metric"],
        "target": "content",
        "section": "content",
        "text": "Опыт лучше описывать через конкретные результаты и измеримые достижения, а не через общий список обязанностей.",
    },
    "tailoring": {
        "keywords": ["tailor", "adapt", "vacancy", "адапт", "ваканс", "role-specific"],
        "target": "content",
        "section": "content",
        "text": "Резюме нужно адаптировать под конкретную вакансию: менять акценты, порядок фактов и словарь так, чтобы они отвечали именно текущим требованиям роли.",
    },
    "simple_format": {
        "keywords": ["pdf", "docx", "format", "section", "layout", "формат", "раздел"],
        "target": "format",
        "section": "format",
        "text": "Лучше использовать простую парсабельную структуру: стандартные разделы, последовательное описание опыта и минимум сложных таблиц, колонок и декоративной верстки.",
    },
    "skills_visibility": {
        "keywords": ["visibility", "visible", "подтверж", "видим", "skills"],
        "target": "format",
        "section": "format",
        "text": "Раздел навыков нужно делать заметным и конкретным: выбирать релевантные hard skills, указывать уровень владения там, где это уместно, и не смешивать их с абстрактными личными качествами.",
    },
}

FALLBACKS = {
    "screening": "Рекрутеры и ATS ищут понятные, структурированные сигналы: релевантный опыт, навыки, ключевые слова и удобочитаемую структуру.",
    "content": "Пишите измеримые достижения, релевантные навыки и формулировки, совпадающие с требованиями вакансии.",
    "format": "Собирайте резюме в простой и парсабельной структуре: ясные разделы, минимум визуального шума и понятные поля.",
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
) -> ResumeIntelligenceReport:
    report = ResumeIntelligenceReport(generated_at=generated_at, artifact_path=artifact_path)
    successful = [result for result in results if result.status == "ok"]
    failed = [result for result in results if result.status != "ok"]

    if successful:
        report.summary_points.append(
            f"Processed {len(successful)} live sources and preserved trust-ranked guidance in one reusable artifact."
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

    screening_items = [
        _build_item(theme["text"], theme["target"], matched_themes[theme_name])
        for theme_name, theme in THEMES.items()
        if theme["section"] == "screening" and theme_name in matched_themes
    ]
    content_items = [
        _build_item(theme["text"], theme["target"], matched_themes[theme_name])
        for theme_name, theme in THEMES.items()
        if theme["section"] == "content" and theme_name in matched_themes
    ]
    format_items = [
        _build_item(theme["text"], theme["target"], matched_themes[theme_name])
        for theme_name, theme in THEMES.items()
        if theme["section"] == "format" and theme_name in matched_themes
    ]

    if not screening_items:
        report.screening_findings.append(
            RecommendationItem(
                recommendation_text=FALLBACKS["screening"],
                target="screening",
                rationale="Fallback summary due to sparse or unavailable source text",
                confidence="low",
                supporting_sources=[],
            )
        )
    else:
        report.screening_findings.extend(screening_items)

    if not content_items:
        report.content_recommendations.append(
            RecommendationItem(
                recommendation_text=FALLBACKS["content"],
                target="content",
                rationale="Fallback summary due to sparse or unavailable source text",
                confidence="low",
                supporting_sources=[],
            )
        )
    else:
        report.content_recommendations.extend(content_items)

    if not format_items:
        report.format_recommendations.append(
            RecommendationItem(
                recommendation_text=FALLBACKS["format"],
                target="format",
                rationale="Fallback summary due to sparse or unavailable source text",
                confidence="low",
                supporting_sources=[],
            )
        )
    else:
        report.format_recommendations.extend(format_items)

    primary_missing = [
        result.descriptor.id
        for result in failed
        if result.descriptor.trust_tier == "primary"
    ]
    if primary_missing:
        report.conflicts.append(
            "Primary sources unavailable during this run: " + ", ".join(primary_missing) + "."
        )

    if any(result.descriptor.trust_tier != "primary" for result in successful):
        report.conflicts.append(
            "Some recommendations include secondary evidence and should be validated against role-specific vacancy context."
        )
    if successful:
        report.conflicts.append(
            "Vendor documentation explains parsing and ranking mechanics well, but marketing claims should not be treated as proof of identical behavior across all employers."
        )

    for result in results:
        if result.status == "ok":
            report.source_notes.append(
                f"`{result.descriptor.id}` | {result.descriptor.trust_tier} | {result.descriptor.source_class} | {result.descriptor.url}"
            )
        else:
            reason = result.error_message or result.status
            report.source_notes.append(
                f"`{result.descriptor.id}` | {result.descriptor.trust_tier} | {result.descriptor.source_class} | unavailable | {reason}"
            )

    if failed:
        report.limitations.append(
            f"{len(failed)} source(s) were unavailable or unreadable during this run."
        )
    report.limitations.append(
        "Recommendations describe public-market signals and do not guarantee the behavior of every employer or internal ATS workflow."
    )
    report.limitations.append(
        "Use the artifact as a current evidence brief, then tailor the final resume to the specific vacancy and role."
    )

    return report
