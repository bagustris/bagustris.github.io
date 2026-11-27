import unittest
from sitekit import build, query
from test_publications import FIXTURE

EMPTY = """---
layout: archive
permalink: /zz-empty/
title: zz
---
{% include area-tags.html publications=true %}

## 2026

1. Untagged only.
"""

ROWS = """return [...document.querySelectorAll('.area-dist__row')].map(r => [r.dataset.year,
  r.querySelector('.area-dist__n').textContent.trim(),
  ...[...r.querySelectorAll('.area-dist__val')].map(v => v.textContent.trim())]);"""

EXPECTED = [
    ["total", "4", "1.8 (46%)", "1.3 (33%)", "0.8 (21%)"],
    ["2026", "3", "1.5 (50%)", "1 (33%)", "0.5 (17%)"],
    ["2024", "1", "0.3 (33%)", "0.3 (33%)", "0.3 (33%)"],
]

class DistributionTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.site = build({"_pages/zz-pubs.md": FIXTURE, "_pages/zz-empty.md": EMPTY})

    def test_counts(self):
        self.assertEqual(query(self.site, "/zz-pubs/", ROWS), EXPECTED)

    def test_filter_does_not_change_counts(self):
        self.assertEqual(query(self.site, "/zz-pubs/?theme=acoustics", ROWS), EXPECTED)

    def test_closed_by_default_and_titled(self):
        self.assertEqual(query(self.site, "/zz-pubs/", """
          const d = document.querySelector('#area-distribution');
          return [d.open, d.querySelector('summary').textContent.trim()];"""),
          [False, "Distribution"])

    def test_bar_lengths(self):
        w = query(self.site, "/zz-pubs/", """
          document.querySelector('#area-distribution').open = true;
          return [...document.querySelectorAll('.area-dist__row')].map(r =>
            [...r.querySelectorAll('.area-dist__seg')]
              .reduce((n, s) => n + s.getBoundingClientRect().width, 0));""")
        self.assertAlmostEqual(w[1] / w[0], 1.0, delta=0.05)
        self.assertAlmostEqual(w[2] / w[0], 1 / 3, delta=0.05)

    def test_no_tagged_papers(self):
        self.assertIsNone(query(self.site, "/zz-empty/",
                          "return document.querySelector('#area-distribution');"))

    def test_narrow_screen_has_no_sideways_scroll(self):
        self.assertTrue(query(self.site, "/publications/", """
          const d = document.querySelector('#area-distribution');
          d.open = true;
          return d.getBoundingClientRect().right <= window.innerWidth
            && d.scrollWidth <= d.clientWidth + 1;""", width=390))
