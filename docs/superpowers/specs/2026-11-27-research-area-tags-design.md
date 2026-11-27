# Research area tags: design

Status: approved by the owner, 2026-11-27.

## Intent

Readers should see the site owner's research by area: **speech**, **acoustics** and
**multimodal**. The owner also wants insight into how their papers are spread across
these areas, and wants the home, publications, CV and research pages to tell the
same story. All content stays editable in Markdown.

## Goals

1. Click an area in the home diagram and read about the research in that area.
2. See each paper's area on the publications page, and filter by area.
3. See the number and percentage of papers per area, in total and per year.
4. Show the degree path (acoustics, then speech and acoustics, then multimodal) on
   the CV and research pages.
5. Reorganize the research page.

## Non-goals

- Citation counts, or sorting by anything other than year and area.
- Moving publications into a data file.
- Changing the Japanese publications list or the home page mindmap.

## Anti-goals

The work has failed if the owner must edit HTML to add a paper or update a page, if
any paper or citation text is lost or reworded, or if an area can only be recognized
by its color.

## Constraints

- Jekyll with the remote theme `bagustris/primer2-theme`, hosted statically.
- `layout: compress` minifies HTML. Inline JavaScript must survive it (no `//`
  line comments).
- Light and dark themes (`html[data-theme="dark"]`; page backgrounds `#fff` and
  `#2d2d2d`).
- Never edit `_site/`.

## Approaches

| Question | Options considered | Choice and reason |
|---|---|---|
| Where tags live | Tags in the existing Markdown; separate data file | **Tags in Markdown.** Adding a paper stays as it is today. A data file would make other sorting easier. |
| Diagram click target | Research Areas section; filtered publication list; page per area; panel on home page | **Research Areas section.** It answers "what is your research in this area" and links to the papers, at the cost of one more click. |
| Colors | Match the old diagram (purple, blue, green); furthest apart (blue, orange, aqua) | **Furthest apart.** Owner's preference. The diagram is recolored to match. |
| Tag style | Outlined tag; dot and name | **Outlined tag.** |
| Distribution view | Table of papers carrying each tag; stacked bars adding to 100% | **Stacked bars.** Trends are visible at a glance. |
| Offered themes | Collapsed; fully hidden | **Fully hidden.** The owner asked to hide them. |

## Decided by the owner

### Tags and colors

| Area | Class | Light | Dark | Japanese label |
|---|---|---|---|---|
| Speech | `speech` | `#257de0` | `#338ced` | 音声 |
| Acoustics | `acoustics` | `#f47230` | `#e76624` | 音響 |
| Multimodal | `multimodal` | `#00b894` | `#00a888` | マルチモーダル |

A tag is an outlined pill with a colored dot and the area name. It sits at the end of
the entry's last line (after the year, DOI or PDF link) and wraps only when there is
no room. Text uses the page's text color. This matters because the light orange and
aqua are below 3:1 contrast on white.

The owner writes tags as kramdown attributes at the start of a list item:

```markdown
1. {:.speech .multimodal} H. Wu, ... "Talking Face Generation by Tri-Flow" ...
```

This syntax was tested with local kramdown (GFM) on ordered lists and on lists with
nested bullets. It still needs checking in the site's own build.

### Publications page (`_pages/publications.md`)

- Area filter, listed by year. "All" is the default.
- Distribution as stacked bars with counts and percentages, in total and per year.
- Untagged papers are left out of the distribution. A paper with two tags counts as
  half in each (three tags: a third each), so every bar adds to 100%. Bar length is
  the number of tagged papers.

### CV (`_pages/cv.md`)

| Degree | Tags |
|---|---|
| Bachelor's | acoustics |
| Master's | speech, acoustics |
| PhD | multimodal |

### Research page (`_pages/research.md`)

```
Research
  opening quote
  Research Focus              existing intro and figure, shorter paragraphs
  Research Areas       new    Speech, Acoustics, Multimodal
  Research Journey     new    Bachelor's, Master's, PhD, each tagged
  For Prospective Students
    Offered Research Themes   hidden, tagged in the source
    Other Topics, Typical Timeline, Style Guide, Teaching Policy
  Funding and Awards
    Research Grants, Travel Grants, Scholarships
```

Existing wording is kept apart from small typo fixes and the rewording listed below.

**Offered Research Themes is hidden.** Neither the heading nor the list appears on
the page, in English or Japanese. Both stay in the Markdown file, with their tags,
inside `{% comment %}` and `{% endcomment %}`, so they are left out of the published
HTML. Removing those two lines shows them again.

Research Journey wording:

- `acoustics` 2005–2009, Bachelor's: machine sound separation for fault detection
- `speech` `acoustics` 2010–2012, Master's: source segregation from binaural inputs
- `multimodal` 2018–2021, PhD: speech emotion recognition from acoustic and
  linguistic information

### Home diagram

Clicking an area opens that area under Research Areas.

## Proposed by Claude, approved by the owner

- **Distribution placement:** a section titled "Distribution", closed by default, at
  the top of the publications page, visible to everyone. It always covers all tagged
  papers, whatever the filter. Years with no tagged paper are omitted.
- **Filter behavior:** `/publications/?theme=speech` opens filtered. A theme shows
  only papers carrying that tag; the areas are not nested for filtering. Empty year
  headings are hidden. Numbering follows the visible items.
- **Counting:** only numbered entries under a year heading are papers. The numbered
  profile links at the top of the page are not.
- **Shared code:** styles and scripts live in one include
  (`_includes/area-tags.html`), added to each page with one line. Counts are worked
  out in the browser from the list itself. Without JavaScript, pages show their
  text with no tags, filter or bars.
- **Diagram:** redrawn as an SVG include with three nested ovals in the new colors,
  flat rather than the current hand-sketched style. The innermost oval wins a click.
  Each is a keyboard-reachable link to `#speech`, `#acoustics` or `#multimodal` on
  `/research/` (English home) or `/ja/research/` (Japanese home). The old PNG files
  stay in `images/`. The home page text and mindmap are unchanged.
- **Research Areas:** one or two new sentences per area, drafted for the owner's
  review, each with a link to the filtered publication list. The Japanese research
  page links to the same English publications page.
- **Japanese pages:** `ja/cv.md` and `ja/research.md` get the same tags and structure.
- **Publishing:** add `docs` to `exclude` in `_config.yml`, so this document is not
  published with the site. Also exclude `CLAUDE.md`, `CLAUDE.md.0`, `AGENTS.md`
  and `notes.md` (requested by the owner).

## Rewording for the hidden themes

Two places refer to the themes. Replace them as follows; the owner may edit later.

| File | Replace | With |
|---|---|---|
| `_pages/research.md` front matter `description` | the whole value | Research interests of Bagus Tris Atmaja: speech, acoustics, and multimodal. |
| `_pages/research.md` Teaching Policy | the sentence starting "Master's students may work on my given research themes" | My research interests are speech, acoustics, and multimodal. PhD students should propose their themes independently. |
| `ja/research.md` front matter `description` | the whole value | Bagus Tris Atmaja の研究分野：音声、音響、マルチモーダル。 |
| `ja/research.md` 指導方針 | the sentence starting 修士学生は私が提示する研究テーマに | 私の研究分野は音声、音響、マルチモーダルです。博士学生は独自にテーマを提案すべきです。 |

## Draft tags (owner to correct)

Rule: *speech* analyzes or generates human speech or voice, including vocal bursts.
*Acoustics* covers other sound and vibration, including cough, source separation and
noise. *Multimodal* combines more than one kind of input, such as audio with text or
video.

### Publications

One code per entry, in page order within each year.
`s` speech, `a` acoustics, `m` multimodal, `-` untagged.

| Year | Codes |
|---|---|
| 2026 | s s s s s sm a s s s s sa s s s |
| 2025 | a s s s s a s a s s |
| 2024 | a a s a s s m a |
| 2023 | s s s |
| 2022 | sm s s s s s s s |
| 2021 | sm a sm s s s |
| 2020 | sm sm sm sa s sm s sm |
| 2019 | s s sm sm s |
| 2018 | a s |
| 2017 | a |
| 2016 | s a a |
| 2014 | sa |
| 2012 | a a - s a |
| 2011 | a s - - |
| 2010 | s - |
| 2009 | a - a - - a |
| 2007 | - |

The eight untagged entries are Islamic, Quran-science and *pesantren* essays,
weather forecasting papers and a traffic light paper. They stay listed under "All".
The three Quran recitation software papers are speech recognition and are tagged
speech.

### Offered research themes

Hidden for now. These tags show only if the section is turned back on.

| Theme | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Code | s | s | s | - | a | s | s | s | s | s | m | s | sm | m |

Theme 4 (Calfem-Python) fits none of the three areas.

## Done when

- The site builds with `docker compose -f docker-compose-28.yaml up`.
- With the draft tags and the 88 entries present on 2026-11-27, the distribution
  total is 80 papers: speech 52 (65%), acoustics 21.5 (27%), multimodal 6.5 (8%).
- Each filter and `?theme=` link shows the right papers.
- Citation text is unchanged apart from the added tag markers.
- The offered themes appear in neither research page's published HTML.
- Home, publications, CV and research pages are checked in a browser in light and
  dark themes, on a wide and a narrow screen.

## Left to the builder

Markup and script structure, the filter button styling, and the diagram's exact
geometry.
