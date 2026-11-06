import unittest
from pathlib import Path

import build_site


class CourseNavigationTest(unittest.TestCase):
    def test_rewritten_weeks_keep_legacy_steps_mapped(self):
        weeks = build_site.load_week_metadata()
        expected = [
            "Overview",
            "Learning Objectives",
            "Core Ideas and Case Anchor",
            "Engineering Takeaways",
            "Project Reflection and Further Reading",
        ]
        for week in weeks[:5]:
            number = int(week["week"])
            _, body, path = build_site.load_markdown_page(week["content_path"])
            sections = build_site.page_sections(body, path, weeks)
            self.assertEqual([section["title"] for section in sections], expected)
            mapping = build_site.LEGACY_WEEK_STEPS[number]
            self.assertEqual(mapping[-1], 6)  # The existing slides link.
            self.assertTrue(all(1 <= step <= 6 for step in mapping))
            self.assertEqual(mapping[:2], [1, 2])

    def test_timeline_uses_project_dates_and_guide_sections(self):
        events = build_site.timeline_events(build_site.load_week_metadata())
        milestone = next(event for event in events if "Milestone 2" in event["label"])
        self.assertEqual(milestone["when"], "2026-11-08T21:59")
        self.assertEqual(milestone["step"], "7")
        final = next(event for event in events if "Final submission" in event["label"])
        self.assertEqual(final["when"], "2027-01-10T21:59")
        quiz = next(event for event in events if event["label"] == "In-class quiz 4")
        self.assertEqual(quiz["when"], "2026-11-11T13:15")
        self.assertEqual(quiz["href"], "#section-4")

    def test_navigation_is_chronological_and_excludes_presentations(self):
        weeks = build_site.annotate_week_releases(
            build_site.load_week_metadata(),
            build_site.parse_build_time("2026-12-17T12:00:00+01:00"),
        )
        home = {"page_id": "home", "output_path": Path("/tmp/index.html")}
        nav = build_site.build_navigation(
            Path("/tmp/index.html"), "home", home, weeks, []
        )
        group = next(
            group for group in nav["groups"] if group["title"] == "Weekly materials"
        )
        self.assertEqual(
            [int(page["title"].split()[1]) for page in group["pages"]],
            [1, 2, 3, 4, 5, 6, 7, 8, 10, 11, 12, 13],
        )


if __name__ == "__main__":
    unittest.main()
