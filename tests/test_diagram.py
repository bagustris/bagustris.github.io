import unittest
from sitekit import build, query

HIT = """
document.querySelector('.area-diagram').scrollIntoView();
const at = (area, fx) => {
  const r = document.querySelector('.area-diagram__link--' + area + ' ellipse').getBoundingClientRect();
  const hit = document.elementFromPoint(r.left + r.width * fx, r.top + r.height / 2);
  return hit.closest('a').getAttribute('href'); };
return [at('speech', 0.5), at('acoustics', 0.08), at('multimodal', 0.06)];"""

class DiagramTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.site = build()

    def test_links_and_labels(self):
        for url, base, labels in [
            ("/", "/research/", ["Multimodal", "Acoustics", "Speech"]),
            ("/ja/", "/ja/research/", ["マルチモーダル", "音響", "音声"])]:
            got = query(self.site, url, """return [...document.querySelectorAll('.area-diagram a')]
              .map(a => [a.getAttribute('href'), a.textContent.trim()]);""")
            self.assertEqual(got, [[f"{base}#{a}", l] for a, l in
                             zip(["multimodal", "acoustics", "speech"], labels)])

    def test_innermost_oval_wins(self):
        for width in (1280, 390):
            self.assertEqual(query(self.site, "/", HIT, width=width),
                [f"/research/#{a}" for a in ("speech", "acoustics", "multimodal")])

    def test_old_image_gone_and_fits(self):
        for url, path in [("/", "index.html"), ("/ja/", "ja/index.html")]:
            self.assertNotIn("research_bta_", (self.site / path).read_text())
            self.assertTrue(query(self.site, url,
              "return document.querySelector('.area-diagram svg').getBoundingClientRect().right <= innerWidth;",
              width=390))

    def test_theme_colors(self):
        self.assertEqual(query(self.site, "/", """
          const e = document.querySelector('.area-diagram__link--acoustics ellipse');
          const a = getComputedStyle(e).stroke;
          document.documentElement.setAttribute('data-theme', 'dark');
          getComputedStyle(e).stroke;
          document.getAnimations().forEach(x => x.finish());  /* theme transitions */
          return [a, getComputedStyle(e).stroke];"""),
          ["rgb(244, 114, 48)", "rgb(231, 102, 36)"])
