# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

A multipage Streamlit app with one dashboard per TidyTuesday week. The point of the project is to
learn Streamlit interactivity, not to produce finished analyses: each week's page should exercise a
different slice of the framework (widgets driving charts, interactive tables, caching, layout, ...).
The user picks the datasets; offer recent TidyTuesday weeks as options rather than choosing one.

## Commands

The project uses a local virtualenv at `venv/` (Python 3.12); run everything through it.

```bash
venv/bin/pip install -r requirements.txt          # pinned deps (streamlit 1.46, altair 5.5, pandas 2.3, plotnine, pydytuesday)
venv/bin/streamlit run main.py                    # run the app
venv/bin/python -c "from utils.io import save_tidy_tuesday_data; save_tidy_tuesday_data('2025-07-08')"   # download one week's data into data/week_YYYY-MM-DD/
```

There is no test suite or linter. Verify a page headlessly from the project root with Streamlit's
AppTest instead of eyeballing the browser:

```bash
venv/bin/python -c "
from streamlit.testing.v1 import AppTest
at = AppTest.from_file('pages/2026-09-08.py', default_timeout=60).run()
assert not at.exception, at.exception
print(len(at.title), 'titles;', len(at.dataframe), 'dataframes')
"
```

## Architecture

- `main.py` is the only entrypoint and uses explicit `st.Page` + `st.navigation`, **not** Streamlit's
  automatic `pages/` discovery. Automatic discovery strips the leading numbers from filenames, so
  `2025-07-01.py` would appear as "07-01" in the sidebar. Do not add `st.set_page_config` or
  navigation code to individual pages.
- `utils/io.py` builds the sidebar: `list_week_pages()` globs `pages/YYYY-MM-DD.py` and
  `read_week_title()` pulls the `title:` line out of `data/week_YYYY-MM-DD/meta.yaml` with a regex
  (pyyaml is deliberately not a dependency). A week's label is `YYYY-MM-DD · <title>`, so the data
  folder must exist for the title to show. Non-date pages (`home.py`, `sandbox.py`) are registered
  by hand in `main.py`.
- `utils/io.py` also owns data access: `save_tidy_tuesday_data(date_str)` chdirs into
  `data/week_<date>/` and calls `pydytuesday.get_date`, which downloads every file for that week
  (CSVs plus `.md`, `cleaning.R`, images, `meta.yaml`). `load_tidy_tuesday_data(date_str)` returns
  `{csv_stem: DataFrame}`. Data folders are committed to git.
- `utils/plotting.py` (Altair) and `utils/plotting_plotnine.py` (plotnine) hold small one-liner
  chart helpers; newer pages build Altair charts inline instead.

## Adding a week

1. Create `pages/YYYY-MM-DD.py`; the filename must be exactly the TidyTuesday date.
2. Download the data once (command above) so `data/week_YYYY-MM-DD/meta.yaml` exists.
3. Follow `pages/2026-09-08.py` as the reference pattern: a `@st.cache_data` loader that only calls
   `save_tidy_tuesday_data` when the folder is missing, sidebar filters, `st.warning` + `st.stop()`
   when filters leave nothing, and `st.dataframe(column_config=...)` plus CSV `st.download_button`
   for tables. The two 2025 pages predate this and re-download on every rerun; don't copy that.
4. Watch for pandas `FutureWarning` from `groupby().apply`; use `groupby().agg()` instead.

## Conventions

- Commit messages are short and lowercase, e.g. `added 07-01 dash`. No co-author trailers.
- Commit only after the user asks.
