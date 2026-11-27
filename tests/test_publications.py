import unittest
from sitekit import build, query

FIXTURE = """---
layout: archive
permalink: /zz-pubs/
title: zz
---
{% include area-tags.html publications=true %}

1. [Profile](x)

## 2026

1. {:.speech} S26.

2. {:.speech .multimodal} SM26.

A stray paragraph.

1. {:.acoustics} A26.

## 2025

1. U25.

## 2024

1. {:.speech .acoustics .multimodal} ALL24.
"""

STATE = """
const shown = e => e.getClientRects().length > 0;
return {
  papers: [...document.querySelectorAll('#main ol li')].slice(1).filter(shown)
            .map(li => li.textContent.split('.')[0].trim()),
  years: [...document.querySelectorAll('#main h2')].filter(shown).map(h => h.textContent.trim()),
  pressed: [...document.querySelectorAll('#area-filter [aria-pressed="true"]')].map(b => b.dataset.area),
  profile: shown(document.querySelector('#main ol li')),
  search: location.search };"""

class FilterTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.site = build({"_pages/zz-pubs.md": FIXTURE})

    def state(self, url, before=""):
        return query(self.site, url, before + STATE)

    def test_all_by_default(self):
        s = self.state("/zz-pubs/")
        self.assertEqual(s["papers"], ["S26", "SM26", "A26", "U25", "ALL24"])
        self.assertEqual(s["years"], ["2026", "2025", "2024"])
        self.assertEqual(s["pressed"], ["all"])

    def test_theme_in_url(self):
        s = self.state("/zz-pubs/?theme=speech")
        self.assertEqual(s["papers"], ["S26", "SM26", "ALL24"])
        self.assertEqual(s["years"], ["2026", "2024"])
        self.assertEqual(s["pressed"], ["speech"])
        self.assertTrue(s["profile"])

    def test_split_list_is_filtered(self):
        self.assertEqual(self.state("/zz-pubs/?theme=acoustics")["papers"], ["A26", "ALL24"])

    def test_bad_and_capitalized_theme(self):
        self.assertEqual(self.state("/zz-pubs/?theme=Speech")["pressed"], ["speech"])
        s = self.state("/zz-pubs/?theme=banana")
        self.assertEqual((s["pressed"], len(s["papers"])), (["all"], 5))

    def test_clicks_update_list_and_url(self):
        click = "document.querySelector('#area-filter [data-area=\"%s\"]').click();"
        s = self.state("/zz-pubs/", click % "multimodal")
        self.assertEqual((s["papers"], s["search"]), (["SM26", "ALL24"], "?theme=multimodal"))
        s = self.state("/zz-pubs/?theme=speech", click % "all")
        self.assertEqual((len(s["papers"]), s["search"]), (5, ""))


# Realistic editing slips: a bulleted paper, and a year heading with extra words.
EDITS = """---
layout: archive
permalink: /zz-edits/
title: zz
---
{% include area-tags.html publications=true %}

## 2026

1. {:.speech} S26.

A stray paragraph.

* {:.acoustics} Bullet26.

## 2025 (in press)

1. {:.multimodal} M25.
"""

EDITS_STATE = """
const shown = e => e.getClientRects().length > 0;
return {
  papers: [...document.querySelectorAll('#main ol > li, #main ul > li')].filter(shown)
            .map(li => li.textContent.split('.')[0].trim()),
  years: [...document.querySelectorAll('#main h2')].filter(shown).map(h => h.textContent.trim()),
  counts: [...document.querySelectorAll('.area-dist__row')].map(r =>
            [r.dataset.year, r.querySelector('.area-dist__n').textContent]) };"""


class EditingSlipTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.site = build({"_pages/zz-edits.md": EDITS})

    def state(self, theme):
        return query(self.site, f"/zz-edits/?theme={theme}", EDITS_STATE)

    def test_bulleted_paper_is_filtered_like_a_numbered_one(self):
        self.assertEqual(self.state("speech")["papers"], ["S26"])
        s = self.state("acoustics")
        self.assertEqual((s["papers"], s["years"]), (["Bullet26"], ["2026"]))

    def test_year_heading_with_extra_words_is_a_year(self):
        s = self.state("speech")
        self.assertNotIn("M25", s["papers"])
        self.assertNotIn("2025 (in press)", s["years"])
        s = self.state("multimodal")
        self.assertEqual((s["papers"], s["years"]), (["M25"], ["2025 (in press)"]))

    def test_both_are_counted(self):
        self.assertEqual(self.state("all")["counts"],
                         [["total", "3"], ["2026", "2"], ["2025", "1"]])
