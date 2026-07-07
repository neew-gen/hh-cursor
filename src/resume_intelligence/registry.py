from __future__ import annotations

from .models import SourceDescriptor


def get_default_sources() -> list[SourceDescriptor]:
    return [
        SourceDescriptor(
            id="hh-knowledge-create-resume",
            title="Как создать резюме на hh.ru",
            url="https://feedback.hh.ru/knowledge-base/article/1628",
            source_class="hh_help",
            trust_tier="primary",
            topics=["formatting", "structure", "screening"],
        ),
        SourceDescriptor(
            id="hh-skills-guidance",
            title="Ключевые навыки в резюме на hh.ru",
            url="https://feedback.hh.ru/knowledge-base/article/5453",
            source_class="hh_help",
            trust_tier="primary",
            topics=["keywords", "skills", "screening"],
        ),
        SourceDescriptor(
            id="hh-recruiter-preview",
            title="Как правильно составить резюме, чтобы получить отклик",
            url="https://career.hh.ru/article/kak-sostavit-rezyume-chtoby-poluchit-maksimalnyj-otklik",
            source_class="hh_editorial",
            trust_tier="primary",
            topics=["screening", "content", "keywords"],
        ),
        SourceDescriptor(
            id="hh-tailoring-resume",
            title="Зачем и как адаптировать резюме под разные вакансии",
            url="https://hh.ru/article/24864",
            source_class="hh_editorial",
            trust_tier="primary",
            topics=["keywords", "content", "tailoring"],
        ),
        SourceDescriptor(
            id="sovren-parse-api",
            title="Sovren Parse API",
            url="https://www.sovren.com/technical-specs/latest/rest-api/resume-parser/api/",
            source_class="vendor_doc",
            trust_tier="primary",
            topics=["parsing", "formatting", "normalization"],
        ),
        SourceDescriptor(
            id="oleeo-ats-guide",
            title="What is an Applicant Tracking System?",
            url="https://www.oleeo.com/blog/what-is-an-applicant-tracking-system-ats/",
            source_class="vendor_doc",
            trust_tier="secondary",
            topics=["screening", "ranking", "keywords"],
        ),
        SourceDescriptor(
            id="reqcore-parsing",
            title="AI Resume Parsing Explained",
            url="https://reqcore.com/blog/ai-resume-parsing-explained",
            source_class="vendor_doc",
            trust_tier="secondary",
            topics=["parsing", "structured_fields", "screening"],
        ),
        SourceDescriptor(
            id="reqcore-skills",
            title="AI Skills Extraction",
            url="https://reqcore.com/blog/ai-skills-extraction-mapping-competencies",
            source_class="vendor_doc",
            trust_tier="secondary",
            topics=["skills", "taxonomy", "ranking"],
        ),
        SourceDescriptor(
            id="csulb-ats-guide",
            title="Understanding ATS Software Before Submitting a Resume",
            url="https://www.csulb.edu/college-of-business/legal-resource-center/article/understanding-applicant-tracking-systems-ats",
            source_class="career_center",
            trust_tier="secondary",
            topics=["formatting", "keywords", "screening"],
        ),
        SourceDescriptor(
            id="frontiers-recruiter-algorithms",
            title="Recruiters’ behavior with algorithm-based recommendations",
            url="https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2022.895997/full",
            source_class="academic_research",
            trust_tier="primary",
            topics=["screening", "decision_making", "bias"],
        ),
    ]
