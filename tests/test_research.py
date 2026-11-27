import unittest
from sitekit import build, query

AREAS = ["speech", "acoustics", "multimodal"]

class ResearchTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.site = build()

    def headings(self, url):
        return query(self.site, url, """return [...document.querySelectorAll(
          '#main .page__content h2, #main .page__content h3')].map(h => h.textContent.trim());""")

    def test_structure(self):
        self.assertEqual(self.headings("/research/"), [
            "Research Focus", "Research Areas", "Speech", "Acoustics", "Multimodal",
            "Research Journey", "For Prospective Students", "Other Topics/Themes",
            "Typical Timeline", "Style Guide", "Teaching Policy", "Funding and Awards",
            "Research Grants", "Travel Grants", "Scholarships"])
        self.assertEqual(self.headings("/ja/research/"), [
            "研究の焦点", "研究分野", "音声", "音響", "マルチモーダル", "これまでの歩み",
            "学生の方へ", "その他のトピック・テーマ", "標準的なタイムライン", "スタイルガイド",
            "指導方針", "助成と奨学金", "助成研究プロジェクト", "渡航助成", "奨学金"])

    def test_area_anchors_and_links(self):
        for url in ("/research/", "/ja/research/"):
            got = query(self.site, url, """return ['speech','acoustics','multimodal'].map(id => {
              let e = document.getElementById(id).nextElementSibling;
              while (e && !e.querySelector('a')) e = e.nextElementSibling;
              return e.querySelector('a').getAttribute('href'); });""")
            self.assertEqual(got, [f"/publications/?theme={a}" for a in AREAS])

    def test_themes_hidden(self):
        for path, texts in [("research", ["Offered Research Themes", "Calfem-Python"]),
                            ("ja/research", ["提供してきた研究テーマ", "Calfem-Python"])]:
            html = (self.site / path / "index.html").read_text()
            for t in texts:
                self.assertNotIn(t, html)

    def test_rewording(self):
        en = (self.site / "research/index.html").read_text()
        ja = (self.site / "ja/research/index.html").read_text()
        self.assertIn('content="Research interests of Bagus Tris Atmaja: speech, acoustics, and multimodal."', en)
        self.assertIn("My research interests are speech, acoustics, and multimodal. PhD students should propose their themes independently.", en)
        self.assertNotIn("my given research themes", en)
        self.assertIn('content="Bagus Tris Atmaja の研究分野：音声、音響、マルチモーダル。"', ja)
        self.assertIn("私の研究分野は音声、音響、マルチモーダルです。博士学生は独自にテーマを提案すべきです。", ja)
        self.assertNotIn("私が提示する研究テーマ", ja)

    def test_journey_tags(self):
        self.assertEqual(query(self.site, "/research/", """
          return [...document.querySelector('#research-journey + ul').children].map(li =>
            [...li.querySelectorAll('.area-tag')].map(t => t.textContent.trim()));"""),
          [["Acoustics"], ["Speech", "Acoustics"], ["Multimodal"]])
