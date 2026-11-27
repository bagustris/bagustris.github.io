# Research Area Tags Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Show speech, acoustics and multimodal research across the home, publications, CV and research pages, with filtering and a distribution view.

**Architecture:** The owner marks list items in Markdown with kramdown classes (`{:.speech}`). One include adds tag pills, the publication filter and the distribution bars in the browser. A second include draws the clickable diagram. Tests build the site in Docker and inspect pages in headless Chrome.

**Tech Stack:** Jekyll 3.10 (`github-pages` gem) in the local `jekyll-site` Docker image, vanilla JS and CSS, inline SVG, Python 3 `unittest` (standard library only), `google-chrome`.

**Spec:** `docs/superpowers/specs/2026-11-27-research-area-tags-design.md`

## Global Constraints

- The owner must never need to edit HTML to add a paper or update a page.
- No paper or citation text is lost or reworded. The only rewording is the spec's "Rewording for the hidden themes" table and the typo fixes named in Task 5.
- An area is never shown by color alone: its name is always visible. Tag and label text uses the page's text color.
- Colors, light / dark: speech `#257de0` / `#338ced`, acoustics `#f47230` / `#e76624`, multimodal `#00b894` / `#00a888`. Dark is `html[data-theme="dark"]`.
- Class names `speech`, `acoustics`, `multimodal`; Japanese labels 音声, 音響, マルチモーダル. Fixed order everywhere: speech, acoustics, multimodal.
- `layout: compress` joins lines in production. Inline JS uses `/* */` comments only and ends every statement with a semicolon.
- Do not use the attribute `data-theme` for anything new; the site uses it for dark mode.
- Never edit `_site/`. Never push. Work on branch `research-area-tags`, and `git add` only the files each task lists (the repository has the owner's own untracked files).
- Without JavaScript, pages show their text with no tags, filter or bars.

## Review Focus

1. A new paper added without a tag: listed under "All", absent from themes and the distribution, no script error (Tasks 3, 4).
2. A misspelled class such as `{:.accoustics}`: no pill, treated as untagged (Task 2).
3. `?theme=Speech` or `?theme=banana`: the first filters speech, the second shows "All" (Task 3).
4. A year split into two lists by a stray paragraph: every item is still filtered and counted (Tasks 3, 4).
5. A narrow phone screen with the distribution open: no sideways scrolling (Task 4).

## Files

| File | Responsibility |
|---|---|
| `tests/sitekit.py` | Build the site; run JS in a built page |
| `tests/test_*.py` | One test module per task |
| `_includes/area-tags.html` | Colors, tag pills, filter, distribution |
| `_includes/research-areas.html` | Clickable diagram |
| `_pages/{publications,cv,research,about}.md`, `ja/{cv,research,index}.md` | Content and tags |
| `_config.yml`, `.gitignore` | Keep `docs`, `tests` and caches out |

---

### Task 1: Test harness and publishing exclusions

**Files:**
- Create: `tests/sitekit.py`, `tests/test_build.py`
- Modify: `_config.yml` (`exclude` list), `.gitignore`

**Interfaces:**
- Produces: `build(extra_files: dict[str, str] | None = None) -> pathlib.Path`, the built output directory. `extra_files` maps a repo-relative path to its text and is written into the temporary copy only.
- Produces: `query(site: Path, url: str, js: str, width: int = 1280) -> object`. `js` is a function body run inside the loaded page; it returns a JSON-serializable value. Raises `RuntimeError` if the page raised a script error.

- [ ] **Step 1: Create the branch**

Run: `git switch -c research-area-tags`

- [ ] **Step 2: Write `tests/sitekit.py`**

`build` copies the repo to a temporary directory, excluding top-level `.git`, `_site`, `vendor`, `bak`, `.specstory`, `.vscode` (keep `_sass/vendor`). The source mount must be writable (Sass writes a cache). It needs network access for the remote theme. This command was verified to work:

```python
["docker", "run", "--rm", "--user", f"{os.getuid()}:{os.getgid()}",
 "-e", "JEKYLL_ENV=production", "-e", "HOME=/tmp",
 "-e", "LANG=C.UTF-8", "-e", "LC_ALL=C.UTF-8",
 "-e", "BUNDLE_GEMFILE=/srv/jekyll/Gemfile",
 "-e", "BUNDLE_PATH=/srv/jekyll/vendor/bundle",
 "-v", f"{src}:/usr/src/app", "-v", f"{out}:/out", "-w", "/usr/src/app",
 "jekyll-site", "bundle", "exec", "jekyll", "build",
 "--config", "_config.yml,_config_docker.yml", "-d", "/out"]
```

`query` serves `site` with `http.server` on a free localhost port, plus a wrapper page that loads `url` in an iframe `width` pixels wide (headless Chrome will not make a narrow window). The server injects an `error` listener at the start of each page's `<head>`. After the iframe loads, the wrapper runs `js` in the iframe's window and writes the JSON result and errors into its own DOM. Run Chrome with `--headless=new --disable-gpu --dump-dom --virtual-time-budget=5000 --host-resolver-rules="MAP * ~NOTFOUND, EXCLUDE 127.0.0.1"` and parse the result.

- [ ] **Step 3: Write the failing test `tests/test_build.py`**

```python
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
```

- [ ] **Step 4: Run it and see it fail**

Run: `python3 -m unittest discover -s tests -v`
Expected: `test_internal_folders_not_published` FAILS; `test_query_reads_a_page` passes.

- [ ] **Step 5: Add `docs`, `tests`, `CLAUDE.md`, `CLAUDE.md.0`, `AGENTS.md` and `notes.md` to `exclude` in `_config.yml`; add `__pycache__/` to `.gitignore`**

- [ ] **Step 6: Run again.** Expected: 2 tests PASS.

- [ ] **Step 7: Commit** `tests/sitekit.py tests/test_build.py _config.yml .gitignore docs/superpowers` with message `test: add site test harness; keep docs and tests unpublished`.

### Task 2: Tag pills and CV tags

**Files:**
- Create: `_includes/area-tags.html`, `tests/test_tags.py`
- Modify: `_pages/cv.md`, `ja/cv.md`

**Interfaces:**
- Consumes: `build`, `query`.
- Produces: `{% include area-tags.html %}`, safe to include more than once per page. CSS variables `--area-speech`, `--area-acoustics`, `--area-multimodal` on `:root`.
- Produces: for each `#main li` with an area class, `span.area-tags > span.area-tag.area-tag--<area> > i.area-tag__dot` plus the label. In a list item with a nested list, the wrapper goes immediately before the nested list (inside the preceding `<p>` if there is one). Otherwise it is the last child of the item's last direct `<p>`, or of the `<li>`.

- [ ] **Step 1: Write the failing tests**

Fixtures use `layout: archive` because `single` pages put sidebar links inside `#main`.

```python
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
          return [a, getComputedStyle(dot).backgroundColor,
                  getComputedStyle(tag).color === getComputedStyle(tag.closest('li')).color];"""),
          ["rgb(37, 125, 224)", "rgb(51, 140, 237)", True])

    def test_cv_degrees(self):
        self.assertEqual(self.q("/cv/", CV),
                         [["Multimodal"], ["Speech", "Acoustics"], ["Acoustics"]])
        self.assertEqual(self.q("/ja/cv/", CV),
                         [["マルチモーダル"], ["音声", "音響"], ["音響"]])
```

- [ ] **Step 2: Run** `python3 -m unittest discover -s tests -p test_tags.py -v`. Expected: FAIL (include not found).

- [ ] **Step 3: Write `_includes/area-tags.html`**: one `<style>` and one `<script>` that runs on `DOMContentLoaded` and returns early if `window.areaTags` already exists. Pill: 1.5px border in the area color, fully rounded, 8px dot, small text, `white-space: nowrap`, left margin. Choose labels by whether `document.documentElement.lang` starts with `ja`.

- [ ] **Step 4: Add the include and tags to both CV pages.** Put the include on its own line, blank lines around it, after the opening quote. Tags: Bachelor's `{:.acoustics}`, Master's `{:.speech .acoustics}`, PhD `{:.multimodal}`, written right after the `* ` of each degree line.

- [ ] **Step 5: Run the tests.** Expected: all PASS.

- [ ] **Step 6: Commit** `_includes/area-tags.html tests/test_tags.py _pages/cv.md ja/cv.md`, message `feat: add research area tags and tag the CV`.

### Task 3: Publication tags and filter

**Files:**
- Modify: `_includes/area-tags.html`, `_pages/publications.md`
- Test: `tests/test_publications.py`

**Interfaces:**
- Produces: `{% include area-tags.html publications=true %}` outputs an element `[data-area-publications]` where the distribution will mount, and enables the filter.
- Produces: papers are the direct `li` of every `ol` between a four-digit `h2` and the next `h2` or `hr`. Nothing before the first year heading is a paper.
- Produces: `#area-filter`, inserted just before the first year heading, with `button[data-area="all|speech|acoustics|multimodal"][aria-pressed]` labelled All, Speech, Acoustics, Multimodal. Hidden papers, headings and lists get the `hidden` attribute.

- [ ] **Step 1: Write the failing tests**

```python
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
```

- [ ] **Step 2: Run** `python3 -m unittest discover -s tests -p test_publications.py -v`. Expected: FAIL (no `#area-filter`).

- [ ] **Step 3: Implement the filter** in `_includes/area-tags.html`. Read `theme` with `URLSearchParams`, lower-case it, fall back to `all`; write it with `history.replaceState`, removing it for All. Add a CSS rule so `hidden` always wins over theme styles.

- [ ] **Step 4: Run the tests.** Expected: all PASS.

- [ ] **Step 5: Tag the real list.** Run `grep -cE '^[0-9]+\. ' _pages/publications.md`; expected `91` (88 papers and 3 profile links). If it differs, the owner has added papers: ask for their tags before continuing. Add the include as the first line after the front matter, and apply the spec's "Draft tags / Publications" codes as `N. {:.speech .multimodal} …`; `-` gets nothing.

- [ ] **Step 6: Confirm citation text is unchanged**

Run: `diff <(git show master:_pages/publications.md) <(sed -E 's/^([0-9]+\. )\{:[^}]*\} /\1/' _pages/publications.md)`
Expected: only the added include line and its blank line, plus the `[PDF](../files/O-COCOSDA_2026_paper__49.pdf)` link the owner asked for on 2026 entry 12 (added before this plan ran).

- [ ] **Step 7: Commit** `_includes/area-tags.html _pages/publications.md tests/test_publications.py files/O-COCOSDA_2026_paper__49.pdf`, message `feat: tag publications and filter them by area`.

### Task 4: Distribution

**Files:**
- Modify: `_includes/area-tags.html`
- Test: `tests/test_distribution.py`

**Interfaces:**
- Consumes: Task 3's definition of a paper and `[data-area-publications]`.
- Produces: `details#area-distribution` (closed; `summary` text "Distribution") at the mount point. Column headings Year, No. and the three areas with dots. Rows `.area-dist__row[data-year]` (`total`, labelled "Total", then years newest first), each with `.area-dist__n`, three `.area-dist__val[data-area]`, and bar segments `.area-dist__seg[data-area]`.
- A paper with k tags adds 1/k to each. Values show at most one decimal, no trailing `.0`, then the rounded percentage: `52 (65%)`. Bar length is proportional to tagged papers in that year relative to the largest year; Total is full width. Computed from all tagged papers, regardless of the filter.

- [ ] **Step 1: Write the failing tests**

```python
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
```

- [ ] **Step 2: Run** `python3 -m unittest discover -s tests -p test_distribution.py -v`. Expected: FAIL.

- [ ] **Step 3: Implement** in `_includes/area-tags.html`: a CSS grid per row, 2px gaps between segments, `title` on each segment with area and value; below 600px the values wrap under the bar.

- [ ] **Step 4: Run the tests.** Expected: all PASS.

- [ ] **Step 5: Check the real totals.** Query `/publications/` with `ROWS`. Expected first row `["total", "80", "52 (65%)", "21.5 (27%)", "6.5 (8%)"]` and no `2007` row.

- [ ] **Step 6: Commit** `_includes/area-tags.html tests/test_distribution.py`, message `feat: show publication distribution by area`.

### Task 5: Research pages

**Files:**
- Modify: `_pages/research.md`, `ja/research.md`
- Test: `tests/test_research.py`

**Interfaces:**
- Consumes: `{% include area-tags.html %}`.
- Produces: anchors `#speech`, `#acoustics`, `#multimodal` on `/research/` and `/ja/research/`.

- [ ] **Step 1: Write the failing tests**

```python
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
```

- [ ] **Step 2: Run** `python3 -m unittest discover -s tests -p test_research.py -v`. Expected: FAIL.

- [ ] **Step 3: Reorganize both pages** in the heading order the test lists. Move existing text; demote moved `##` headings to `###`.
  - Research Focus: split the long paragraph before "My approaches…", "For me, science…" and "My research contributes…" (Japanese: before これらの目標を, 私にとって科学は, 私の研究は Society 5.0), then the figure and its HTML comment.
  - Typo fixes only: "intead" → "instead"; "Other consideration is  robustness" → "Another consideration is robustness".
  - Add the include on its own line after the opening quote.
  - Move the "For undergraduate level…" sentence (学部生レベルでは…) to the end of Teaching Policy.
  - Apply the spec's rewording table.

New area copy (each `###` heading carries an explicit id, e.g. `### 音声 {#speech}`, and is followed by the sentence and a link line):

| id | English sentence | English link text |
|---|---|---|
| speech | I study how machines can understand and produce human speech: recognizing speech and emotion, synthesizing expressive voices, and detecting health conditions from the voice. | See speech publications |
| acoustics | I study sound and vibration beyond speech, such as cough sounds, machine noise, acoustic scenes, and sound source separation. | See acoustics publications |
| multimodal | I combine audio with other information, such as text and video, to understand and generate human communication. | See multimodal publications |

| id | Japanese sentence | Japanese link text |
|---|---|---|
| speech | 人間の音声を機械が理解し、生成するための研究です。音声認識、感情認識、表現豊かな音声合成、声からの健康状態の検出に取り組んでいます。 | 音声の論文一覧（英語） |
| acoustics | 咳の音、機械の騒音、音響シーン、音源分離など、音声以外の音や振動を研究しています。 | 音響の論文一覧（英語） |
| multimodal | 音声をテキストや映像などの情報と組み合わせ、人間のコミュニケーションを理解・生成する研究です。 | マルチモーダルの論文一覧（英語） |

Research Journey (`## Research Journey` / `## これまでの歩み {#research-journey}`):

```markdown
* {:.acoustics} **2005–2009, Bachelor's:** machine sound separation for fault detection
* {:.speech .acoustics} **2010–2012, Master's:** source segregation from binaural inputs
* {:.multimodal} **2018–2021, PhD:** speech emotion recognition from acoustic and linguistic information
```

```markdown
* {:.acoustics} **2005〜2009年、学士：** 故障検知のための機械音分離
* {:.speech .acoustics} **2010〜2012年、修士：** 両耳入力に基づく音源分離
* {:.multimodal} **2018〜2021年、博士：** 音響情報と言語情報に基づく音声感情認識
```

Hidden section, placed first under For Prospective Students: wrap the old heading, its lead sentence and the 14 items in `{% comment %}` / `{% endcomment %}`. Tag items with the spec's research theme codes (theme 4 gets none).

- [ ] **Step 4: Run the tests.** Expected: all PASS.

- [ ] **Step 5: Confirm no wording was lost**

Run:
```bash
for f in _pages/research.md ja/research.md; do echo "== $f"; python3 - "$f" <<'EOF'
import re, subprocess, sys
f = sys.argv[1]
old = subprocess.check_output(["git", "show", "master:" + f], text=True)
strip = lambda s: re.sub(r"\{:[^}]*\}|\s+", "", s)
new = strip(open(f, encoding="utf-8").read())
for line in old.splitlines():
    for s in re.split(r"(?<=\. )|(?<=。)", line):
        if s.strip() and not s.startswith("#") and strip(s) not in new:
            print(s)
EOF
done
```
Expected: only the `description` lines, the two replaced Teaching Policy sentences, and the sentences containing the two typos.

- [ ] **Step 6: Commit** `_pages/research.md ja/research.md tests/test_research.py`, message `feat: reorganize research pages around research areas`.

### Task 6: Clickable diagram

**Files:**
- Create: `_includes/research-areas.html`, `tests/test_diagram.py`
- Modify: `_pages/about.md:16-18`, `ja/index.md:19-21` (the `<p align="center">` image blocks)

**Interfaces:**
- Consumes: Task 2's color variables, Task 5's anchors.
- Produces: `{% include research-areas.html base="/research/" %}`; Japanese passes `base="/ja/research/"`. It includes `area-tags.html` itself.

- [ ] **Step 1: Write the failing tests**

```python
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
          return [a, getComputedStyle(e).stroke];"""),
          ["rgb(244, 114, 48)", "rgb(231, 102, 36)"])
```

- [ ] **Step 2: Run** `python3 -m unittest discover -s tests -p test_diagram.py -v`. Expected: FAIL.

- [ ] **Step 3: Write `_includes/research-areas.html`**: `div.area-diagram` holding an SVG, `viewBox="0 0 470 352"`, `width: 100%`, max 470px, centered, `role="group"` with `aria-label` "Research areas" (Japanese 研究分野, chosen by `page.lang`). Three `a.area-diagram__link.area-diagram__link--<area>` in the order multimodal, acoustics, speech, each with an ellipse (area-colored 2px stroke, light fill of the same color) and a label in the text color. Start from centers/radii (235,176 / 230,170), (280,200 / 165,106), (330,214 / 85,60) and labels at (104,104), (204,155), (329,219), centered. Give links a visible hover and keyboard-focus state. Keep the markup free of blank lines.

- [ ] **Step 4: Replace the image block on both home pages** with the include. Change no other text and keep the PNG files.

- [ ] **Step 5: Run the tests.** Expected: all PASS.

- [ ] **Step 6: Commit** `_includes/research-areas.html _pages/about.md ja/index.md tests/test_diagram.py`, message `feat: make the home research diagram clickable`.

### Task 7: Whole-site check

- [ ] **Step 1:** Run `python3 -m unittest discover -s tests -v`. Expected: all PASS.
- [ ] **Step 2:** Run `docker compose -f docker-compose-28.yaml up -d`, wait for `http://localhost:4000/` to answer. Expected: the site serves (development path, with `JEKYLL_ENV=docker`).
- [ ] **Step 3:** View `/`, `/ja/`, `/publications/` (distribution open, one filter on), `/cv/`, `/ja/cv/`, `/research/`, `/ja/research/` in light and dark themes, wide and at phone width. Expected: no overlap, clipping or unreadable text; tags on the last line; clicking each oval lands on its heading; the browser console shows no errors from the new code.
- [ ] **Step 4:** Run `docker compose -f docker-compose-28.yaml down`, then `git status --short`. Expected: only the owner's pre-existing untracked files.
- [ ] **Step 5:** Report to the owner, with screenshots, and list the draft tags and new area sentences for their review.
