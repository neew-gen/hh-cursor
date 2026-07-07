# Resume Intelligence

_Generated at: 2026-07-07T08:45:01.816689+00:00_

## Summary
- Processed 10 live sources and preserved trust-ranked guidance in one reusable artifact.
- Covered source classes: academic_research, career_center, hh_editorial, hh_help, vendor_doc.

## HowHRAndATSProcessResumesNow
- [high] HR сначала смотрят на быстрые сигналы из превью и верхних блоков резюме: должность, последний релевантный опыт, ключевые навыки и общую понятность профиля. (sources: `hh-recruiter-preview`, `hh-tailoring-resume`, `sovren-parse-api`, `oleeo-ats-guide`, `reqcore-parsing`, `reqcore-skills`, `csulb-ats-guide`, `frontiers-recruiter-algorithms`; rationale: Synthesized from 4 primary and 4 secondary sources)
- [high] ATS сначала разбирают резюме в структурированные поля, поэтому неочевидная верстка, лишний визуальный шум и нестандартные блоки ухудшают распознавание опыта, навыков и дат. (sources: `hh-recruiter-preview`, `hh-tailoring-resume`, `sovren-parse-api`, `oleeo-ats-guide`, `reqcore-parsing`, `reqcore-skills`, `frontiers-recruiter-algorithms`; rationale: Synthesized from 4 primary and 3 secondary sources)

## WhatToWrite
- [high] Нужно прямо писать релевантные навыки, инструменты и формулировки из вакансии, потому что и ATS, и рекрутеры сопоставляют резюме с требованиями по ключевым сигналам. (sources: `hh-knowledge-create-resume`, `hh-skills-guidance`, `hh-recruiter-preview`, `hh-tailoring-resume`, `sovren-parse-api`, `oleeo-ats-guide`, `reqcore-parsing`, `reqcore-skills`, `csulb-ats-guide`, `frontiers-recruiter-algorithms`; rationale: Synthesized from 6 primary and 4 secondary sources)
- [high] Опыт лучше описывать через конкретные результаты и измеримые достижения, а не через общий список обязанностей. (sources: `hh-knowledge-create-resume`, `hh-recruiter-preview`, `hh-tailoring-resume`, `sovren-parse-api`, `oleeo-ats-guide`, `reqcore-parsing`, `reqcore-skills`, `csulb-ats-guide`, `frontiers-recruiter-algorithms`; rationale: Synthesized from 5 primary and 4 secondary sources)
- [high] Резюме нужно адаптировать под конкретную вакансию: менять акценты, порядок фактов и словарь так, чтобы они отвечали именно текущим требованиям роли. (sources: `hh-knowledge-create-resume`, `hh-skills-guidance`, `hh-recruiter-preview`, `hh-tailoring-resume`, `oleeo-ats-guide`, `reqcore-skills`, `csulb-ats-guide`, `frontiers-recruiter-algorithms`; rationale: Synthesized from 5 primary and 3 secondary sources)

## HowToBuildResume
- [high] Лучше использовать простую парсабельную структуру: стандартные разделы, последовательное описание опыта и минимум сложных таблиц, колонок и декоративной верстки. (sources: `hh-knowledge-create-resume`, `hh-skills-guidance`, `hh-recruiter-preview`, `hh-tailoring-resume`, `sovren-parse-api`, `oleeo-ats-guide`, `reqcore-parsing`, `reqcore-skills`, `csulb-ats-guide`, `frontiers-recruiter-algorithms`; rationale: Synthesized from 6 primary and 4 secondary sources)
- [high] Раздел навыков нужно делать заметным и конкретным: выбирать релевантные hard skills, указывать уровень владения там, где это уместно, и не смешивать их с абстрактными личными качествами. (sources: `hh-knowledge-create-resume`, `hh-skills-guidance`, `hh-recruiter-preview`, `hh-tailoring-resume`, `sovren-parse-api`, `oleeo-ats-guide`, `reqcore-parsing`, `reqcore-skills`, `csulb-ats-guide`, `frontiers-recruiter-algorithms`; rationale: Synthesized from 6 primary and 4 secondary sources)

## SourceQualityAndConflicts
- Some recommendations include secondary evidence and should be validated against role-specific vacancy context.
- Vendor documentation explains parsing and ranking mechanics well, but marketing claims should not be treated as proof of identical behavior across all employers.

## Sources
- `hh-knowledge-create-resume` | primary | hh_help | https://feedback.hh.ru/knowledge-base/article/1628
- `hh-skills-guidance` | primary | hh_help | https://feedback.hh.ru/knowledge-base/article/5453
- `hh-recruiter-preview` | primary | hh_editorial | https://career.hh.ru/article/kak-sostavit-rezyume-chtoby-poluchit-maksimalnyj-otklik
- `hh-tailoring-resume` | primary | hh_editorial | https://hh.ru/article/24864
- `sovren-parse-api` | primary | vendor_doc | https://www.sovren.com/technical-specs/latest/rest-api/resume-parser/api/
- `oleeo-ats-guide` | secondary | vendor_doc | https://www.oleeo.com/blog/what-is-an-applicant-tracking-system-ats/
- `reqcore-parsing` | secondary | vendor_doc | https://reqcore.com/blog/ai-resume-parsing-explained
- `reqcore-skills` | secondary | vendor_doc | https://reqcore.com/blog/ai-skills-extraction-mapping-competencies
- `csulb-ats-guide` | secondary | career_center | https://www.csulb.edu/college-of-business/legal-resource-center/article/understanding-applicant-tracking-systems-ats
- `frontiers-recruiter-algorithms` | primary | academic_research | https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2022.895997/full

## FreshnessAndLimitations
- Recommendations describe public-market signals and do not guarantee the behavior of every employer or internal ATS workflow.
- Use the artifact as a current evidence brief, then tailor the final resume to the specific vacancy and role.
