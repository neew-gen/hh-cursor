import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from resume_profile.artifacts import (
    artifact_path,
    has_saved_artifacts,
    load_artifact,
    resolve_artifact_path,
    write_artifact_bundle,
)
from resume_profile.draft import SKILLS_MODE_APPEND, save_draft
from resume_profile.models import EducationEntry, ResumeProfile, SkillEntry
from resume_profile.runner import prepare_supplement_draft, write_profile_artifact


class ArtifactTests(unittest.TestCase):
    def test_artifact_path_use_translit_slug(self):
        path = artifact_path("Frontend Developer (Vue)")
        self.assertEqual(path.name, "frontend-developer-vue.yaml")

    def test_has_saved_artifacts_false_when_directory_missing(self):
        with tempfile.TemporaryDirectory() as tmp:
            missing_legacy = Path(tmp) / "legacy.yaml"
            missing_dir = Path(tmp) / "resume-profile"
            with patch("resume_profile.artifacts.LEGACY_ARTIFACT_PATH", missing_legacy):
                with patch("resume_profile.artifacts.ARTIFACTS_DIR", missing_dir):
                    self.assertFalse(has_saved_artifacts())

    def test_has_saved_artifacts_true_when_yaml_exists(self):
        with tempfile.TemporaryDirectory() as tmp:
            missing_legacy = Path(tmp) / "legacy.yaml"
            artifacts_dir = Path(tmp) / "resume-profile"
            artifacts_dir.mkdir(parents=True, exist_ok=True)
            (artifacts_dir / "dev.yaml").write_text("target_role: Dev\n", encoding="utf-8")
            with patch("resume_profile.artifacts.LEGACY_ARTIFACT_PATH", missing_legacy):
                with patch("resume_profile.artifacts.ARTIFACTS_DIR", artifacts_dir):
                    self.assertTrue(has_saved_artifacts())

    def test_resolve_artifact_path_adds_numeric_suffix_when_slug_exists(self):
        with tempfile.TemporaryDirectory() as tmp:
            missing_legacy = Path(tmp) / "legacy.yaml"
            artifacts_dir = Path(tmp) / "resume-profile"
            artifacts_dir.mkdir(parents=True, exist_ok=True)
            existing = artifacts_dir / "frontend-developer-vue.yaml"
            existing.write_text("target_role: Frontend Developer (Vue)\n", encoding="utf-8")
            with patch("resume_profile.artifacts.LEGACY_ARTIFACT_PATH", missing_legacy):
                with patch("resume_profile.artifacts.ARTIFACTS_DIR", artifacts_dir):
                    resolved = resolve_artifact_path("Frontend Developer (Vue)")
                    self.assertEqual(resolved.name, "frontend-developer-vue (2).yaml")

    def test_write_append_merges_base_skills(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = ResumeProfile(
                target_role="Frontend Developer (Vue)",
                work_experience_status="none",
                skills_hard=[SkillEntry(name="Vue.js", level="medium")],
                no_formal_education=True,
            )
            yaml_path = Path(tmp) / artifact_path(base.target_role).name
            write_artifact_bundle(base, yaml_path)

            draft_path = Path(tmp) / "draft.json"
            prepare_supplement_draft(
                yaml_path,
                skills_mode=SKILLS_MODE_APPEND,
                draft_path=draft_path,
            )
            data = json.loads(draft_path.read_text(encoding="utf-8"))
            profile = ResumeProfile(
                target_role=data["target_role"],
                work_experience_status=data["work_experience_status"],
                skills_hard=[SkillEntry(name="React", level="advanced")],
                no_formal_education=data["no_formal_education"],
            )
            save_draft(draft_path, profile, data["_meta"])
            out = write_profile_artifact(profile, yaml_path, meta=data["_meta"])
            saved = load_artifact(out)
            names = [item.name for item in saved.skills_hard]
            self.assertEqual(names, ["Vue.js", "React"])

    def test_load_saved_yaml_artifact(self):
        path = Path("artifacts/resume-profile/frontend-developer-vue.yaml")
        if not path.is_file():
            self.skipTest("artifact file not present")
        profile = load_artifact(path)
        self.assertEqual(profile.target_role, "Frontend Developer (Vue)")
        self.assertTrue(profile.skills_hard)

    def test_write_artifact_bundle_does_not_create_json_sidecar(self):
        with tempfile.TemporaryDirectory() as tmp:
            profile = ResumeProfile(
                target_role="Backend Developer",
                work_experience_status="none",
                no_formal_education=True,
            )
            yaml_path = Path(tmp) / "backend-developer.yaml"
            write_artifact_bundle(profile, yaml_path)
            self.assertTrue(yaml_path.is_file())
            self.assertFalse(yaml_path.with_suffix(".json").exists())


if __name__ == "__main__":
    unittest.main()
