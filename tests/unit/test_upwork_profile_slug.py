import unittest

from upwork_profile.slug import slugify_profile_title


class UpworkSlugTests(unittest.TestCase):
    def test_latin_title(self):
        self.assertEqual(
            slugify_profile_title("Full Stack Developer (React)"),
            "full-stack-developer-react",
        )

    def test_cyrillic_title(self):
        self.assertEqual(
            slugify_profile_title("Старший Frontend-разработчик"),
            "starshiy-frontend-razrabotchik",
        )

    def test_empty_title_defaults_to_profile(self):
        self.assertEqual(slugify_profile_title(""), "profile")


if __name__ == "__main__":
    unittest.main()
