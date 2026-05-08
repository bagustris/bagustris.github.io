# Copilot Instructions

## Build & Serve

**Docker (preferred):**
```bash
# Docker < 28
docker-compose -f docker-compose.yaml up

# Docker >= 28
docker compose -f docker-compose-28.yaml up
```
The site is served at `http://localhost:4000`.

**Local (without Docker):**
```bash
bundle install
bundle exec jekyll serve --livereload
```
Use `_config_docker.yml` alongside `_config.yml` inside the container (sets `url: ""`).

## Architecture

This is a Jekyll academic personal website using the remote theme [`bagustris/primer2-theme`](https://github.com/bagustris/primer2-theme). Content is organized into Jekyll collections:

| Directory | Collection | Purpose |
|---|---|---|
| `_pages/` | pages | Static pages (about, CV, tutorials, tools, etc.) |
| `_publications/` | publications | Academic papers |
| `_talks/` | talks | Conference/seminar talks (uses `talk` layout) |
| `_teaching/` | teaching | Courses and teaching material |
| `_portfolio/` | portfolio | Project portfolio items |
| `ja/` | — | Japanese-language mirror pages (linked via `lang_ref`) |

Navigation order and bilingual labels are controlled by `_data/navigation.yml`.

## Key Conventions

### Front Matter
Every content file requires front matter. Common fields:
```yaml
---
layout: single          # or: archive, talk, splash, cv-layout
title: "Page Title"
permalink: /url-path/
author_profile: true
description: "SEO description"   # used for <meta description>
---
```

### Bilingual Pages (English ↔ Japanese)
Pages with Japanese equivalents use `lang` and `lang_ref` to link them:
```yaml
# English page (_pages/about.md)
lang: en
lang_ref: about

# Japanese mirror (ja/index.md)
lang: ja
lang_ref: about          # must match the English page's lang_ref
permalink: /ja/          # ja/ prefix for all Japanese URLs
```
Navigation entries in `_data/navigation.yml` support `title_ja` and `url_ja` for bilingual menu items.

### Layouts
- `single` — default for pages, publications, teaching, portfolio
- `talk` — required for `_talks/` collection entries
- `archive` — listing pages (e.g., publications index, tag archive)
- `cv-layout` — CV page
- Layouts are provided by the remote theme; do not override them locally unless customizing.

### Markdown & Highlighting
- Markdown processor: **kramdown** with GFM input
- Syntax highlighter: **rouge**
- Excerpt separator: blank line (`\n\n`)
- Mermaid diagrams are supported in page content (used in `_pages/about.md`).

### Permalinks
- Posts: `/:categories/:title/`
- Collections use `/:collection/:path/` (defined per-collection in `_config.yml`)
- Japanese pages: `/ja/<path>/`

### Static Assets
- Images: `images/` directory
- Downloadable files: `files/` directory (included in build via `_config.yml`)
- Custom SCSS goes in `_sass/`; compiled with compressed output style.

### What's Excluded from Build
`_site/`, `Dockerfile`, `Gemfile`, `.github/`, `vendor/`, `node_modules/`, and several other dev files are excluded in `_config.yml` — do not rely on them being served.
