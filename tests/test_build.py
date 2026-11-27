import unittest

from sitekit import build, query


class BuildTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.site = build()

    def test_internal_folders_not_published(self):
        self.assertFalse((self.site / "docs").exists())
        self.assertFalse((self.site / "tests").exists())
        for name in ("CLAUDE.md", "CLAUDE.md.0", "AGENTS.md", "notes.md"):
            self.assertFalse((self.site / name).exists(), name)

    def test_query_reads_a_page(self):
        n = query(self.site, "/publications/", "return document.querySelectorAll('h2').length;")
        self.assertGreaterEqual(n, 17)


if __name__ == "__main__":
    unittest.main()
