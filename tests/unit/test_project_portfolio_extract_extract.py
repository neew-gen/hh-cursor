import unittest
from pathlib import Path

from project_portfolio_extract.compose import compose_portfolio
from project_portfolio_extract.extract import extract_facts


FIXTURE_ROOT = Path("tests/fixtures/sample-vue-repo")


class ProjectPortfolioExtractTests(unittest.TestCase):
    def test_extract_facts_from_fixture(self) -> None:
        facts = extract_facts(
            FIXTURE_ROOT,
            repo_url="https://github.com/example/vue-use-api-call",
            source_type="local_path",
        )
        self.assertEqual(facts.name, "vue-use-api-call")
        self.assertIn("Vue composable", facts.summary)
        self.assertIn("vue", facts.dependencies)
        self.assertIn("TypeScript", facts.languages_hint)
        self.assertFalse(facts.stale)

    def test_compose_portfolio_from_fixture(self) -> None:
        facts = extract_facts(
            FIXTURE_ROOT,
            repo_url="https://github.com/example/vue-use-api-call",
            source_type="local_path",
        )
        draft = compose_portfolio(facts)
        self.assertEqual(draft.title, "vue-use-api-call")
        self.assertIn("Vue composable", draft.description)
        self.assertEqual(draft.project_url, "https://github.com/example/vue-use-api-call")
        self.assertIn("Vue.js", draft.skills)


if __name__ == "__main__":
    unittest.main()
