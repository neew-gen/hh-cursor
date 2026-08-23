from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from resume_profile.yaml_io import parse_artifact_yaml
from upwork_proposal.models import (
    ContractTerms,
    JobSnapshot,
    ProposalCoverLetter,
    ProposalPlan,
    ProposalReport,
    ScreeningAnswer,
    SectionStatus,
)


def proposal_plan_to_dict(plan: ProposalPlan) -> dict[str, Any]:
    contract_terms = None
    if plan.contract_terms:
        contract_terms = {
            "bid_type": plan.contract_terms.bid_type,
            "hourly_rate": plan.contract_terms.hourly_rate,
            "fixed_price": plan.contract_terms.fixed_price,
            "duration": plan.contract_terms.duration,
            "weekly_hours": plan.contract_terms.weekly_hours,
            "milestones": list(plan.contract_terms.milestones),
            "connects_required": plan.contract_terms.connects_required,
        }

    return {
        "composed_at": plan.composed_at,
        "job": {
            "url": plan.job.url,
            "title": plan.job.title,
            "client": plan.job.client,
            "description": plan.job.description,
            "budget_type": plan.job.budget_type,
            "key_skills": list(plan.job.key_skills),
            "screening_questions": list(plan.job.screening_questions),
            "extracted_at": plan.job.extracted_at,
        },
        "source_profile": plan.source_profile,
        "target_role": plan.target_role,
        "profile_match_hint": plan.profile_match_hint,
        "cover_letter": {
            "text": plan.cover_letter.text,
            "language": plan.cover_letter.language,
            "char_count": plan.cover_letter.char_count,
        },
        "screening_answers": [
            {"question": item.question, "answer": item.answer}
            for item in plan.screening_answers
        ],
        "contract_terms": contract_terms,
        "rewrite_applied": plan.rewrite_applied,
        "intelligence_path": plan.intelligence_path,
        "intelligence_freshness": plan.intelligence_freshness,
        "intelligence_citations": list(plan.intelligence_citations),
        "limitations": list(plan.limitations),
    }


def render_proposal_plan_yaml(plan: ProposalPlan) -> str:
    lines = [
        f"composed_at: {_yaml_scalar(plan.composed_at)}",
        "job:",
        f"  url: {_yaml_scalar(plan.job.url)}",
        f"  title: {_yaml_scalar(plan.job.title)}",
        f"  client: {_yaml_scalar(plan.job.client)}",
        f"  description: {_yaml_block_scalar(plan.job.description, indent=4)}",
        f"  budget_type: {_yaml_scalar(plan.job.budget_type)}",
        "  key_skills:",
    ]
    for item in plan.job.key_skills:
        lines.append(f"    - {_yaml_scalar(item)}")
    lines.append("  screening_questions:")
    for item in plan.job.screening_questions:
        lines.append(f"    - {_yaml_scalar(item)}")
    lines.append(f"  extracted_at: {_yaml_scalar(plan.job.extracted_at)}")
    lines.extend(
        [
            f"source_profile: {_yaml_scalar(plan.source_profile)}",
            f"target_role: {_yaml_scalar(plan.target_role)}",
            f"profile_match_hint: {_yaml_scalar(plan.profile_match_hint)}",
            "cover_letter:",
            f"  text: {_yaml_block_scalar(plan.cover_letter.text, indent=4)}",
            f"  language: {_yaml_scalar(plan.cover_letter.language)}",
            f"  char_count: {_yaml_scalar(plan.cover_letter.char_count)}",
            "screening_answers:",
        ]
    )
    for answer in plan.screening_answers:
        lines.append(f"  - question: {_yaml_scalar(answer.question)}")
        lines.append(f"    answer: {_yaml_scalar(answer.answer)}")
    lines.append("contract_terms:")
    if plan.contract_terms:
        lines.append(f"  bid_type: {_yaml_scalar(plan.contract_terms.bid_type)}")
        lines.append(f"  hourly_rate: {_yaml_scalar(plan.contract_terms.hourly_rate)}")
        lines.append(f"  fixed_price: {_yaml_scalar(plan.contract_terms.fixed_price)}")
        lines.append(f"  duration: {_yaml_scalar(plan.contract_terms.duration)}")
        lines.append(f"  weekly_hours: {_yaml_scalar(plan.contract_terms.weekly_hours)}")
        lines.append("  milestones:")
        for milestone in plan.contract_terms.milestones:
            lines.append(f"    - {_yaml_scalar(milestone)}")
        lines.append(
            f"  connects_required: {_yaml_scalar(plan.contract_terms.connects_required)}"
        )
    else:
        lines.append("  null")
    lines.extend(
        [
            f"rewrite_applied: {_yaml_scalar(plan.rewrite_applied)}",
            f"intelligence_path: {_yaml_scalar(plan.intelligence_path)}",
            f"intelligence_freshness: {_yaml_scalar(plan.intelligence_freshness)}",
            "intelligence_citations:",
        ]
    )
    for citation in plan.intelligence_citations:
        lines.append(f"  - {_yaml_scalar(citation)}")
    lines.append("limitations:")
    for limitation in plan.limitations:
        lines.append(f"  - {_yaml_scalar(limitation)}")
    return "\n".join(lines) + "\n"


def load_proposal_plan(path: str | Path) -> ProposalPlan:
    data = parse_artifact_yaml(Path(path).read_text(encoding="utf-8"))
    job_data = data.get("job") or {}
    cover_data = data.get("cover_letter") or {}
    contract_data = data.get("contract_terms")

    contract_terms = None
    if contract_data and contract_data is not None:
        connects = contract_data.get("connects_required")
        contract_terms = ContractTerms(
            bid_type=contract_data.get("bid_type"),
            hourly_rate=contract_data.get("hourly_rate"),
            fixed_price=contract_data.get("fixed_price"),
            duration=contract_data.get("duration"),
            weekly_hours=contract_data.get("weekly_hours"),
            milestones=list(contract_data.get("milestones") or []),
            connects_required=int(connects) if connects is not None else None,
        )

    screening_answers = [
        ScreeningAnswer(
            question=item.get("question", ""),
            answer=item.get("answer", ""),
        )
        for item in data.get("screening_answers") or []
    ]

    return ProposalPlan(
        composed_at=data.get("composed_at", ""),
        job=JobSnapshot(
            url=job_data.get("url", ""),
            title=job_data.get("title", ""),
            client=job_data.get("client", ""),
            description=job_data.get("description", ""),
            budget_type=job_data.get("budget_type", ""),
            key_skills=list(job_data.get("key_skills") or []),
            screening_questions=list(job_data.get("screening_questions") or []),
            extracted_at=job_data.get("extracted_at", ""),
        ),
        source_profile=data.get("source_profile", ""),
        target_role=data.get("target_role", ""),
        profile_match_hint=data.get("profile_match_hint", ""),
        cover_letter=ProposalCoverLetter(
            text=cover_data.get("text", ""),
            language=cover_data.get("language", "en"),
            char_count=int(cover_data.get("char_count") or 0),
        ),
        screening_answers=screening_answers,
        contract_terms=contract_terms,
        rewrite_applied=bool(data.get("rewrite_applied", False)),
        intelligence_path=data.get("intelligence_path"),
        intelligence_freshness=data.get("intelligence_freshness"),
        intelligence_citations=list(data.get("intelligence_citations") or []),
        limitations=list(data.get("limitations") or []),
    )


def write_proposal_plan(plan: ProposalPlan, output_path: str | Path) -> str:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render_proposal_plan_yaml(plan), encoding="utf-8")
    return str(path)


def render_proposal_report_yaml(report: ProposalReport) -> str:
    lines = [
        f"reported_at: {_yaml_scalar(report.reported_at)}",
        f"proposal_plan_path: {_yaml_scalar(report.proposal_plan_path)}",
        f"submitted: {_yaml_scalar(report.submitted)}",
        "blockers:",
    ]
    for blocker in report.blockers:
        lines.append(f"  - {_yaml_scalar(blocker)}")
    lines.append("sections:")
    for section in report.sections:
        lines.append(f"  - section_id: {_yaml_scalar(section.section_id)}")
        lines.append(f"    status: {_yaml_scalar(section.status)}")
        lines.append(f"    notes: {_yaml_scalar(section.notes)}")
    return "\n".join(lines) + "\n"


def write_proposal_report(report: ProposalReport, output_path: str | Path) -> str:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render_proposal_report_yaml(report), encoding="utf-8")
    return str(path)


def build_proposal_report(
    proposal_plan_path: str,
    sections: list[dict[str, str]],
    blockers: list[str] | None = None,
) -> ProposalReport:
    return ProposalReport(
        reported_at=datetime.now(timezone.utc).isoformat(),
        proposal_plan_path=proposal_plan_path,
        submitted=False,
        sections=[
            SectionStatus(
                section_id=item.get("section_id", ""),
                status=item.get("status", "skipped"),
                notes=item.get("notes", ""),
            )
            for item in sections
        ],
        blockers=list(blockers or []),
    )


def _yaml_block_scalar(text: str, indent: int = 2) -> str:
    prefix = " " * indent
    return "|\n" + "\n".join(f"{prefix}{line}" for line in text.splitlines())


def _yaml_scalar(value: Any) -> str:
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (int, float)):
        return str(value)
    text = str(value)
    if text == "":
        return '""'
    if "\n" in text:
        return _yaml_block_scalar(text, indent=2)
    escaped = text.replace("\\", "\\\\").replace('"', '\\"')
    if any(ch in text for ch in ":{}[],&*#?|-<>=!%@`"):
        return f'"{escaped}"'
    return escaped
