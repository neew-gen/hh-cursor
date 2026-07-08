import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from resume_profile.models import (
    EducationEntry,
    ResumeProfile,
    SkillEntry,
    WorkExperienceEntry,
)
from resume_profile.runner import list_gaps, merge_extracted_profile, write_profile_artifact
from resume_profile.writer import profile_to_dict


class RunnerTests(unittest.TestCase):
    def test_bootstrap_initializes_draft_when_no_artifacts(self):
        with tempfile.TemporaryDirectory() as tmp:
            draft_path = Path(tmp) / "profile-draft.json"
            env = dict(os.environ)
            env["PYTHONPATH"] = "src"
            result = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "resume_profile.cli",
                    "bootstrap",
                    "--output",
                    str(draft_path),
                ],
                capture_output=True,
                text=True,
                check=True,
                env=env,
            )
            payload = json.loads(result.stdout)
            self.assertFalse(payload["has_artifacts"])
            self.assertTrue(payload["draft_initialized"])
            self.assertEqual(payload["draft_path"], str(draft_path))
            self.assertTrue(draft_path.is_file())

    def test_bootstrap_reports_existing_artifacts(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = ResumeProfile(
                target_role="Frontend Developer (Vue)",
                work_experience_status="none",
                skills_hard=[SkillEntry(name="Vue.js", level="medium")],
                no_formal_education=True,
            )
            artifact_dir = Path(tmp) / "artifacts" / "resume-profile"
            artifact_dir.mkdir(parents=True, exist_ok=True)
            artifact_path = artifact_dir / "frontend-developer-vue.yaml"
            write_profile_artifact(base, artifact_path)
            env = dict(os.environ)
            env["PYTHONPATH"] = "/workspace/hh-cursor/src"

            result = subprocess.run(
                [sys.executable, "-m", "resume_profile.cli", "bootstrap"],
                capture_output=True,
                text=True,
                check=True,
                cwd=tmp,
                env=env,
            )
            payload = json.loads(result.stdout)
            self.assertTrue(payload["has_artifacts"])
            self.assertIn("artifacts", payload)
            self.assertEqual(payload["artifacts"][0]["slug"], "frontend-developer-vue")

    def test_write_complete_profile(self):
        profile = ResumeProfile(
            input_mode="questionnaire_only",
            target_role="Developer",
            work_experience_status="none",
            skills_hard=[SkillEntry(name="Go", level="medium")],
            no_formal_education=True,
            limitations=["Questionnaire only"],
        )
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "resume-profile.yaml"
            write_profile_artifact(profile, out)
            content = out.read_text(encoding="utf-8")
            self.assertIn("target_role: Developer", content)

    def test_gaps_json_for_skip_q1_draft(self):
        draft = {
            "input_mode": "questionnaire_only",
            "resume_link": None,
        }
        profile = __import__(
            "resume_profile.writer", fromlist=["profile_from_dict"]
        ).profile_from_dict(draft)
        gaps = list_gaps(profile)
        self.assertTrue(gaps)

    def test_merge_extracted_profile_replaces_resume_fields(self):
        base = ResumeProfile(
            input_mode="questionnaire_only",
            target_role="Frontend Developer (Vue)",
            work_experience_status="has_experience",
            work_experience=[
                WorkExperienceEntry(
                    company="Old Company",
                    position="Frontend Developer",
                    start_date="2021-01",
                    description="Old description",
                )
            ],
            skills_hard=[SkillEntry(name="Vue.js", level="medium")],
            education=[EducationEntry(institution="Old College", degree="Old degree")],
            about_me="Старое описание",
        )
        incoming = ResumeProfile(
            input_mode="questionnaire_with_link",
            resume_link="https://hh.ru/resume/abc123",
            target_role="Frontend Developer (Vue)",
            work_experience_status="has_experience",
            work_experience=[
                WorkExperienceEntry(
                    company="Example Inc",
                    position="Lead Developer",
                    start_date="Июнь 2025",
                    description="Новый опыт",
                    provenance="from_resume_link",
                ),
                WorkExperienceEntry(
                    company="Acme Corp",
                    position="Frontend-разработчик",
                    start_date="Апрель 2020",
                    description="CRM",
                    provenance="from_resume_link",
                ),
            ],
            skills_hard=[
                SkillEntry(name="JavaScript", level="medium", provenance="from_resume_link"),
                SkillEntry(name="TypeScript", level="medium", provenance="from_resume_link"),
            ],
            education=[
                EducationEntry(
                    institution="MSU",
                    degree="Среднее специальное",
                    specialty="Геодезия",
                    graduation_year=2015,
                    provenance="from_resume_link",
                )
            ],
            about_me="Новое описание",
        )

        merged = merge_extracted_profile(base, incoming)

        self.assertEqual(merged.input_mode, "questionnaire_with_link")
        self.assertEqual(merged.resume_link, "https://hh.ru/resume/abc123")
        self.assertEqual(len(merged.work_experience), 2)
        self.assertEqual(merged.work_experience[0].company, "Example Inc")
        self.assertEqual([skill.name for skill in merged.skills_hard], ["JavaScript", "TypeScript"])
        self.assertEqual(merged.education[0].institution, "MSU")
        self.assertEqual(merged.about_me, "Новое описание")

    def test_extract_text_merges_into_existing_draft_and_preserves_meta(self):
        html = """
        <html><body>
        <p class="resume__position">Frontend Developer (Vue)</p>
        <li class="resume-experience">
            <span class="resume-experience__company">Example Inc</span>
            <p class="bloko-form-hint">Июнь 2025 — настоящее время 1 год 2 месяца</p>
            <p class="resume-experience__position">Ведущий программист</p>
            <p>- CRM<br/>Стек: Vue</p>
        </li>
        <li class="resume-experience">
            <span class="resume-experience__company">Acme Corp</span>
            <p class="bloko-form-hint">Апрель 2020 — Апрель 2021 1 год 1 месяц</p>
            <p class="resume-experience__position">Frontend-разработчик</p>
            <p>- CRM на Vue</p>
        </li>
        <p class="resume__block">Образование</p>
        <ul><li class="resume-education">
            <span class="resume-education__name">MSU</span>
            <p class="bloko-form-hint">2015</p>
            <p class="bloko-form-hint">Среднее специальное</p>
        </li><p>Геодезия</p></ul>
        <span class="bloko-form-hint">Навыки</span>
        <p class="resume-skils__item"><span>JavaScript; </span><span>Vue.js; </span></p>
        <span class="bloko-form-hint">Обо мне</span>
        <p class="resume-skils__item">Полный текст о себе<br/>https://example.com</p>
        </body></html>
        """
        draft = {
            "input_mode": "questionnaire_only",
            "resume_link": None,
            "target_role": "Frontend Developer (Vue)",
            "work_experience_status": "has_experience",
            "work_experience": [
                {
                    "company": "Old Company",
                    "position": "Old Position",
                    "start_date": "2021-01",
                    "end_date": None,
                    "is_current": False,
                    "description": "Old description",
                    "company_description": None,
                    "provenance": "from_user_answer",
                }
            ],
            "skills": {"hard": [], "soft": []},
            "education": [],
            "no_formal_education": False,
            "about_me": None,
            "work_preferences": None,
            "languages": [],
            "additional_education": [],
            "portfolio_links": [],
            "personal_links": [],
            "limitations": [],
            "sources": {
                "resume_link_used": False,
                "fields_from_link": 0,
                "fields_from_user": 0,
            },
            "_meta": {
                "skills_mode": "new",
                "source_artifact": "artifacts/resume-profile/frontend-developer-vue.yaml",
                "skip_resume_link": True,
            },
        }
        with tempfile.TemporaryDirectory() as tmp:
            draft_path = Path(tmp) / "profile-draft.json"
            html_path = Path(tmp) / "resume.html"
            draft_path.write_text(json.dumps(draft, ensure_ascii=False, indent=2), encoding="utf-8")
            html_path.write_text(html, encoding="utf-8")
            env = dict(os.environ)
            env["PYTHONPATH"] = "/workspace/hh-cursor/src"

            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "resume_profile.cli",
                    "extract-text",
                    "--input",
                    str(html_path),
                    "--output",
                    str(draft_path),
                    "--resume-link",
                    "https://hh.ru/resume/abc123",
                ],
                capture_output=True,
                text=True,
                check=True,
                cwd=tmp,
                env=env,
            )

            payload = json.loads(draft_path.read_text(encoding="utf-8"))
            self.assertEqual(payload["_meta"]["skills_mode"], "new")
            self.assertEqual(payload["resume_link"], "https://hh.ru/resume/abc123")
            self.assertEqual(len(payload["work_experience"]), 2)
            self.assertEqual(payload["work_experience"][0]["company"], "Example Inc")
            self.assertEqual(payload["skills"]["hard"][0]["name"], "JavaScript")
            self.assertEqual(payload["about_me"], "Полный текст о себе\nhttps://example.com")


if __name__ == "__main__":
    unittest.main()
