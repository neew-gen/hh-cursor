import unittest

from resume_profile.extractor import (
    extract_from_download_html,
    extract_from_page_text,
    extract_resume_content,
    is_valid_hh_resume_link,
)


class ExtractorTests(unittest.TestCase):
    def test_valid_resume_link(self):
        self.assertTrue(
            is_valid_hh_resume_link("https://hh.ru/resume/abc123def")
        )
        self.assertFalse(is_valid_hh_resume_link("https://example.com/resume/1"))

    def test_extract_skills_and_role_from_text(self):
        text = """
        Backend Developer
        Желаемая должность: Backend Developer
        Ключевые навыки
        Python, PostgreSQL, Docker
        Опыт работы
        Компания: Acme Corp
        Должность: Python Developer
        03.2021 - по настоящее время
        - Built REST APIs
        - Reduced deploy time by 30%
        Образование
        MSU
        Applied Mathematics
        Bachelor
        2020
        """
        profile = extract_from_page_text(
            text,
            resume_link="https://hh.ru/resume/abc123",
        )
        self.assertEqual(profile.target_role, "Backend Developer")
        self.assertTrue(profile.skills_hard)
        self.assertEqual(profile.work_experience_status, "has_experience")
        self.assertTrue(profile.work_experience)
        self.assertTrue(profile.education)


    def test_extract_full_about_me(self):
        about_body = (
            "В разработке стараюсь придерживаться простоты кода, использую KISS, DRY, YAGNI, SOLID. "
            "Использую IDE Cursor для написания кода. "
            "Также в свободное от работы время я занимаюсь разработкой пет-проектов:\n"
            "- Библиотека — аналог TanStack Query. https://github.com/acme-corp/demo-ui\n"
            "- Браузерная игра https://example.com/game\n"
            "Примеры кода: https://github.com/acme-corp/code-samples\n"
            "Контакты доступны по запросу"
        )
        text = f"""
        Frontend Developer
        Желаемая должность: Frontend Developer
        Ключевые навыки
        JavaScript, TypeScript
        Опыт работы
        Компания: Acme
        Должность: Developer
        01.2020 - 01.2024
        - Built apps
        Образование
        MSU 2020
        О себе
        {about_body}
        Повышение квалификации, курсы
        freeCodeCamp 2020
        """
        profile = extract_from_page_text(text)
        self.assertIsNotNone(profile.about_me)
        assert profile.about_me is not None
        self.assertIn("github.com/acme-corp/demo-ui", profile.about_me)
        self.assertIn("example.com/game", profile.about_me)
        self.assertGreater(len(profile.about_me), 200)
        self.assertNotIn("freeCodeCamp", profile.about_me)

    def test_extract_multiple_experience_entries_without_blank_lines(self):
        text = """
        Frontend Developer
        Опыт работы
        Acme Corp
        2 года 5 месяцев
        Frontend-разработчик / Старший Frontend-разработчик
        Апрель 2021 — Август 2023
        - Разработка и поддержка системы на Vue, Nuxt
        - Интеграция API бэкенда
        Beta LLC
        1 год 8 месяцев
        Старший Frontend-разработчик / Fullstack-разработчик
        Сентябрь 2023 — Апрель 2025
        - Разработка и поддержка системы проведения мероприятий на Vue
        - Написание и рефакторинг бэкенда на NestJS
        Example Inc
        1 год 2 месяца
        Ведущий программист
        Июнь 2025 — по настоящее время
        - Разработка с нуля внутренней CRM системы
        - Разработка UI Kit
        Образование
        MSU
        """
        profile = extract_from_page_text(text)
        self.assertEqual(profile.work_experience_status, "has_experience")
        self.assertEqual(len(profile.work_experience), 3)
        self.assertEqual(profile.work_experience[0].company, "Acme Corp")
        self.assertEqual(profile.work_experience[1].company, "Beta LLC")
        self.assertEqual(profile.work_experience[2].company, "Example Inc")
        self.assertEqual(profile.work_experience[2].start_date, "Июнь 2025")
        self.assertTrue(profile.work_experience[2].is_current)

    def test_extract_current_experience_with_seychas(self):
        text = """
        Frontend Developer
        Опыт работы
        Example Inc
        1 год 2 месяца
        Ведущий программист
        Июнь 2025 — сейчас
        - Разработка с нуля внутренней CRM системы
        Образование
        MSU
        """
        profile = extract_from_page_text(text)
        self.assertEqual(len(profile.work_experience), 1)
        self.assertEqual(profile.work_experience[0].company, "Example Inc")
        self.assertTrue(profile.work_experience[0].is_current)

    def test_extract_from_download_html_contains_all_jobs(self):
        html = """
        <html><body>
        <p class="resume__position">Frontend Developer (Vue)</p>
        <li class="resume-profession-role">Программист, разработчик</li>
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
        profile = extract_from_download_html(html, resume_link="https://hh.ru/resume/abc")
        self.assertEqual(profile.target_role, "Frontend Developer (Vue)")
        self.assertEqual(len(profile.work_experience), 2)
        self.assertEqual(profile.work_experience[0].company, "Example Inc")
        self.assertTrue(profile.work_experience[0].is_current)
        self.assertEqual(profile.work_experience[1].company, "Acme Corp")
        self.assertEqual(profile.skills_hard[0].name, "JavaScript")
        self.assertEqual(profile.skills_hard[0].level, "")
        self.assertNotIn("...", [skill.name for skill in profile.skills_hard])
        self.assertIn("https://example.com", profile.about_me or "")

    def test_extract_resume_content_detects_download_html(self):
        html = '<html><body><li class="resume-experience"><span class="resume-experience__company">Example Inc</span><p class="bloko-form-hint">Июнь 2025 — сейчас</p><p class="resume-experience__position">Dev</p><p>- work</p></li></body></html>'
        profile = extract_resume_content(html)
        self.assertEqual(profile.work_experience[0].company, "Example Inc")

    def test_extract_from_download_html_with_extra_attributes(self):
        html = """
        <html><body>
        <p class="resume__position" data-cursor-ref="e1">Frontend Developer (Vue)</p>
        <li class="resume-profession-role" data-cursor-ref="e2">Программист, разработчик</li>
        <li class="resume-experience" data-cursor-ref="e3">
            <span class="resume-experience__company" data-cursor-ref="e4">Example Inc</span>
            <p class="bloko-form-hint" data-cursor-ref="e5">Июнь 2025 — настоящее время 1 год 2 месяца</p>
            <p class="resume-experience__position" data-cursor-ref="e6">Ведущий программист</p>
            <p data-cursor-ref="e7">- CRM<br/>Стек: Vue, TypeScript</p>
        </li>
        <p class="resume__block" data-cursor-ref="e8">Образование</p>
        <ul><li class="resume-education" data-cursor-ref="e9">
            <span class="resume-education__name" data-cursor-ref="e10">MSU</span>
            <p class="bloko-form-hint" data-cursor-ref="e11">2015</p>
            <p class="bloko-form-hint" data-cursor-ref="e12">Среднее специальное</p>
        </li><p data-cursor-ref="e13">Геодезия</p></ul>
        <span class="bloko-form-hint" data-cursor-ref="e14">Навыки</span>
        <p class="resume-skils__item" data-cursor-ref="e15"><span>JavaScript; </span><span>Vue.js; </span><span>Nuxt; </span></p>
        <span class="bloko-form-hint" data-cursor-ref="e16">Обо мне</span>
        <p class="resume-skils__item" data-cursor-ref="e17">Полный текст о себе<br/>https://example.com</p>
        </body></html>
        """
        profile = extract_from_download_html(html, resume_link="https://hh.ru/resume/abc")
        self.assertEqual(profile.target_role, "Frontend Developer (Vue)")
        self.assertEqual(profile.work_experience[0].company, "Example Inc")
        self.assertEqual([skill.name for skill in profile.skills_hard], ["JavaScript", "Vue.js", "Nuxt"])
        self.assertEqual([skill.level for skill in profile.skills_hard], ["", "", ""])
        self.assertEqual(profile.education[0].institution, "MSU")
        self.assertIn("https://example.com", profile.about_me or "")

    def test_extract_from_download_html_parses_resume_skills_class(self):
        html = """
        <html><body>
        <li class="resume-skills">
            <span class="bloko-form-hint">Навыки</span>
            <p class="resume-skills__item">
                <span>JavaScript; </span><span>TypeScript; </span><span>Vue.js; </span>
            </p>
        </li>
        </body></html>
        """
        profile = extract_from_download_html(html, resume_link="https://hh.ru/resume/abc")
        self.assertEqual(
            [skill.name for skill in profile.skills_hard],
            ["JavaScript", "TypeScript", "Vue.js"],
        )

    def test_extract_from_download_html_deduplicates_entries_and_parses_languages(self):
        html = """
        <html><body>
        <p class="resume__position">Frontend Developer</p>
        <li class="resume-profession-role">Программист, разработчик</li>
        <li class="resume-profession-role">Программист, разработчик</li>
        <li class="resume-experience">
            <span class="resume-experience__company">Example Inc</span>
            <p class="bloko-form-hint">Июнь 2025 — настоящее время 1 год 2 месяца</p>
            <p class="resume-experience__position">Ведущий программист</p>
            <p>- CRM<br/>Стек: Vue</p>
        </li>
        <li class="resume-experience">
            <span class="resume-experience__company">Example Inc</span>
            <p class="bloko-form-hint">Июнь 2025 — настоящее время 1 год 2 месяца</p>
            <p class="resume-experience__position">Ведущий программист</p>
            <p>- CRM<br/>Стек: Vue</p>
        </li>
        <span class="bloko-form-hint">Навыки</span>
        <p class="resume-skils__item"><span>JavaScript; </span><span>JavaScript; </span><span>Vue.js; </span></p>
        <span class="bloko-form-hint">Знание языков</span>
        <ul class="resume-skils__item">
            <li data-cursor-ref="e1">Русский <span class="info"> — Родной</span></li>
            <li data-cursor-ref="e2">Английский <span class="info"> — B1 — Средний</span></li>
        </ul>
        </body></html>
        """
        profile = extract_from_download_html(html, resume_link="https://hh.ru/resume/abc")
        self.assertEqual(profile.specializations, ["Программист, разработчик"])
        self.assertEqual(len(profile.work_experience), 1)
        self.assertEqual([skill.name for skill in profile.skills_hard], ["JavaScript", "Vue.js"])
        self.assertEqual(
            [(lang.name, lang.level) for lang in profile.languages],
            [("Русский", "Родной"), ("Английский", "B1 — Средний")],
        )


if __name__ == "__main__":
    unittest.main()
