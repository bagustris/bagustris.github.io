# Repository Guidelines

## Project Structure & Module Organization
This repository is a Jekyll-based personal site. Core configuration lives in [`_config.yml`](/home/bagus/github/bagustris.github.io/_config.yml) and [`_config_docker.yml`](/home/bagus/github/bagustris.github.io/_config_docker.yml). Page content is primarily under [`_pages/`](/home/bagus/github/bagustris.github.io/_pages), with reusable HTML fragments in [`_includes/`](/home/bagus/github/bagustris.github.io/_includes), page templates in [`_layouts/`](/home/bagus/github/bagustris.github.io/_layouts), and Sass partials in [`_sass/`](/home/bagus/github/bagustris.github.io/_sass). Static assets are stored in [`assets/`](/home/bagus/github/bagustris.github.io/assets), [`images/`](/home/bagus/github/bagustris.github.io/images), [`fonts/`](/home/bagus/github/bagustris.github.io/fonts), and downloadable papers in [`files/`](/home/bagus/github/bagustris.github.io/files). Generated output appears in [`_site/`](/home/bagus/github/bagustris.github.io/_site) and should not be edited manually.

## Build, Test, and Development Commands
Preferred local workflow uses Docker:

```bash
docker compose -f docker-compose-28.yaml up
```

Use this on Docker 28+. For older setups, run `docker-compose -f docker-compose.yaml up`. The site is served on `http://localhost:4000` with file watching enabled. If you already have Ruby installed, `bundle install` then `bundle exec jekyll serve -H 0.0.0.0 -w --config _config.yml,_config_docker.yml` provides the same result.

## Coding Style & Naming Conventions
Use YAML front matter at the top of Markdown pages and keep indentation to two spaces in YAML files. Match existing Jekyll conventions: lowercase, hyphenated filenames such as `tag-archive.html` or `about.md`; keep includes and layouts descriptive and scoped to their purpose. Prefer Markdown for page content, HTML only when template logic is required, and Sass edits in existing partials rather than ad hoc inline styles.

## Testing Guidelines
There is no automated test suite in this repository. Validate changes by starting the local Jekyll server, checking the affected pages in a browser, and watching for build errors in the container or Jekyll output. For content changes, verify front matter, internal links, and asset paths such as `/images/...` or `/files/...`.

## Commit & Pull Request Guidelines
Recent history uses short messages like `update` and `update pub`; contributors should be more specific. Use concise, imperative commit subjects such as `Add 2025 publication PDF` or `Fix broken about page link`. Pull requests should include a short summary, list of affected pages or assets, screenshots for visible UI/content changes, and any manual verification steps used to confirm the site builds cleanly.
