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
