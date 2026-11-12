import tempfile
import unittest
from pathlib import Path

import build_site


class StandalonePageTest(unittest.TestCase):
    def setUp(self):
        self.build_dir = build_site.BUILD_DIR
        self.temp_dir = tempfile.TemporaryDirectory()
        build_site.BUILD_DIR = Path(self.temp_dir.name) / "docs"

    def tearDown(self):
        build_site.BUILD_DIR = self.build_dir
        self.temp_dir.cleanup()

    def test_supervisors_page_is_standalone_and_noindex(self):
        build_site.build_site()

        page = (build_site.BUILD_DIR / "supervisors" / "index.html").read_text(
            encoding="utf-8"
        )

        self.assertIn('<body class="page-standalone">', page)
        self.assertIn('<meta name="robots" content="noindex">', page)
        self.assertIn('src="../assets/brand/light_logo_long.png"', page)
        self.assertNotIn('id="site-sidebar"', page)
        self.assertNotIn('class="sidebar-toggle"', page)
        self.assertNotIn("data-paginator", page)
        self.assertNotIn('rel="canonical"', page)
        self.assertEqual(page.count('class="supervisor-photo"'), 6)
        for supervisor in (
            "Mallo Henriet",
            "Fabrice Nemo",
            "David Sasu",
            "Trevor Brokowski",
            "Xavier Theimer-Lienhard",
            "Yusuf Kesmen",
        ):
            self.assertIn(f"<h2>{supervisor}</h2>", page)
        self.assertNotIn("Sahaj Vaidya", page)


if __name__ == "__main__":
    unittest.main()
