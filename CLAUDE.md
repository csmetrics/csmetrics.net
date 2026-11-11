# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

The Django (Python 3) web app behind csmetrics.net: it ranks institutions by publications and citations at CS conferences and journals. There is no test suite, linter config or build step. The Django app doubles as the project package (`app/`), and there are no models; the SQLite DB exists only for Django's built-in apps.

## Commands

```bash
pip install -r requirements.txt          # web app deps
pip install -r requirements_update.txt   # extra deps for the data-update notebooks (jupyter, matplotlib)
./run_server.sh                          # makemigrations + migrate + runserver on localhost:8000
python manage.py runserver localhost:8000  # just the server
```

Production runs in Docker (`Dockerfile`): `collectstatic` into `static/`, then gunicorn serves `app.wsgi`. `settings.py` has `DEBUG = True` and `ALLOWED_HOSTS` limited to localhost.

## Architecture

**Request flow.** `views.main` / `views.shareable` render `main.html` (which includes `ctrpanel.html` and `rtable.html`) with defaults and the topic list. The page's JS then:
- POSTs to `/update` with pub/cit year ranges, weight mode (`equal` or `geomean`) and a comma-separated list of venue abbreviations. `utils.get_paper_score` returns per-institution `wpub` (the predicted metric: weighted publication count over the pub years) and `cite` (the measured metric: citations to papers published in the cit years).
- GETs `/venue` for the venue table.
- Computes the **combined score, ranking, filtering (type, region, country) and pagination in the browser** (`rtable.html`: `(measured+ε)^(1-α) * (predicted+ε)^α`, ε=0.01). The server never sees α, and the type, region and country filters are applied only in the browser.

**Data loading (`app/utils.py`).** Everything lives in module-level globals, loaded once per process on the first page view (`load_data()`), from three sources:
- `data/scores/{venue}_{year}_affiliations.json` → `{institution name: {"Publication Count", "Citation Count"}}` (fractional counts). Files ending in `_author` are skipped.
- `app/data/venue_list.csv`: venue key, display abbreviation, two topic-area columns (comma-separated, which is why CSV quoting matters), type, title, dblp URL. The topic areas become the category "tag cloud". Venues are looked up by **key** internally, but the client sends **abbreviations** (`Venue` column), and `get_paper_score` maps between them.
- `app/data/venue_weight.csv`: venue key → arithmetic and geometric mean citations per paper; the GeoMean column is used as the venue weight.
- `app/data/inst_full_clean.csv`: OpenAlex ID, name, type, continent, country, URL. Keyed by **name**, which must match the keys in the score JSONs; institutions missing from it are silently dropped from results. The file has no header row.

**Docs pages.** `/overview`, `/faq` and `/acks` try to render `overview_generated.html` etc. These are not in the repo (presumably produced from `docs/*.md` at deploy time). Without them the page falls back to a GitHub link.

## Yearly data update

The procedure is documented in `data/README.md`. In outline:
1. Snapshot the current files to `*_<year>` copies (`venue_list_YYYY.csv`, `venue_weight_YYYY.csv`, `data/filtered_papers_YYYY`, `data/scores_YYYY`).
2. Crawl DBLP (`data/get_and_clean_DBLP_papers.ipynb`, with filtering rules in `data/paper_filtering.py`).
3. Fetch citations and affiliations from OpenAlex (`get_paper_data_from_OpenAlex.{ipynb,py}`). Prefer `try_again_venue_papers` for incremental re-runs.
4. Run `score_papers.ipynb`, then `score_venues.ipynb`, to produce `data/scores/` and `venue_weight.csv`.

After an update, also bump the hardcoded year range (`[2007, 2023]`) and default pub/cit years in `app/views.py` (`main` and `shareable`), and update the numbers and dates in `README.md`. `docs/YYYY_update_summary/` holds per-year reports.

`app/data/autoupdate.sh` turns `ErrorReport:` lines in `errorfix.txt` into `gsed` commands that fix an institution's type or country in `inst_full_clean.csv`. It prints the commands and doesn't apply them.

`graph/` is legacy tooling for importing Microsoft Academic Graph data into Elasticsearch. The web app doesn't use it.
