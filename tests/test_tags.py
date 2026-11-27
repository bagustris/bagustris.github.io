import unittest
from sitekit import build, query

def page(slug, lang):
    return f"""---
layout: archive
permalink: /{slug}/
title: {slug}
lang: {lang}
---
{{% include area-tags.html %}}
{{% include area-tags.html %}}

1. {{:.multimodal .speech}} Loose. [PDF](x.pdf)

2. Untagged.

## Next

* {{:.acoustics}} Tight
  * Nested
* {{:.accoustics}} Typo
"""

LABELS = """return [...document.querySelectorAll('#main li')].map(li =>
  [...li.querySelectorAll(':scope > .area-tags .area-tag, :scope > p > .area-tags .area-tag')]
  .map(t => t.textContent.trim()));"""

CV = """return [...document.querySelector('#main ul').children].map(li =>
  [...li.querySelectorAll(':scope > .area-tags .area-tag, :scope > p > .area-tags .area-tag')]
  .map(t => t.textContent.trim()));"""

class TagTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.site = build({"_pages/zz-en.md": page("zz-en", "en"),
                          "_pages/zz-ja.md": page("zz-ja", "ja")})

    def q(self, url, js):
        return query(self.site, url, js)

    def test_labels_order_and_unknown_class(self):
        self.assertEqual(self.q("/zz-en/", LABELS),
                         [["Speech", "Multimodal"], [], ["Acoustics"], [], []])

    def test_japanese_labels(self):
        self.assertEqual(self.q("/zz-ja/", LABELS)[0], ["音声", "マルチモーダル"])

    def test_placement(self):
        self.assertEqual(self.q("/zz-en/", """
          const w = document.querySelectorAll('.area-tags');
          return [w.length, w[0].parentElement.tagName, w[0].nextSibling === null,
                  w[1].nextElementSibling.tagName];"""), [2, "P", True, "UL"])

    def test_light_and_dark_colors_and_text_color(self):
        self.assertEqual(self.q("/zz-en/", """
          const dot = document.querySelector('.area-tag--speech .area-tag__dot');
          const a = getComputedStyle(dot).backgroundColor;
          document.documentElement.setAttribute('data-theme', 'dark');
          const tag = dot.parentElement;
          getComputedStyle(dot).backgroundColor; getComputedStyle(tag).color;
          document.getAnimations().forEach(x => x.finish());  /* theme transitions */
          return [a, getComputedStyle(dot).backgroundColor,
                  getComputedStyle(tag).color === getComputedStyle(tag.closest('li')).color];"""),
          ["rgb(37, 125, 224)", "rgb(51, 140, 237)", True])

    def test_cv_degrees(self):
        self.assertEqual(self.q("/cv/", CV),
                         [["Multimodal"], ["Speech", "Acoustics"], ["Acoustics"]])
        self.assertEqual(self.q("/ja/cv/", CV),
                         [["マルチモーダル"], ["音声", "音響"], ["音響"]])
