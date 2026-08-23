from __future__ import annotations

from .models import SourceDescriptor


def get_default_sources() -> list[SourceDescriptor]:
    return [
        SourceDescriptor(
            id="upwork-help-proposals",
            title="How to submit a proposal on Upwork",
            url="https://support.upwork.com/hc/en-us/articles/211062998-How-to-submit-a-proposal-on-Upwork",
            source_class="upwork_help",
            trust_tier="primary",
            topics=["proposals", "cover_letter", "client_review", "uma"],
        ),
        SourceDescriptor(
            id="upwork-beginners-guide",
            title="How To Use Upwork as a Freelancer (Beginner's Guide)",
            url="https://www.upwork.com/resources/upwork-for-beginners",
            source_class="upwork_editorial",
            trust_tier="primary",
            topics=["profile", "onboarding", "proposals", "visibility"],
        ),
        SourceDescriptor(
            id="upwork-profile-tips",
            title="15 Tips To Make Your Freelancer Profile Stand Out",
            url="https://www.upwork.com/resources/freelancer-profile-tips",
            source_class="upwork_editorial",
            trust_tier="primary",
            topics=["profile", "title", "overview", "portfolio"],
        ),
    ]
