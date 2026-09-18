# TidyTuesday Streamlit Template

A clean, minimal multipage Streamlit boilerplate for weekly TidyTuesday EDA challenges.

## Features

- 📁 Organized directory structure
- 📊 Uses `pandas` and `Altair` for exploration and visualization
- 🔁 One file per week
- 🧰 Utility functions for loading, transforming, and plotting data

## Usage

1. Click **"Use this template"** on GitHub to create your own repo.
2. Install dependencies:

   ```bash
   pip install -r requirements.txt

   streamlit run main.py

3. For each new week:
- Create `pages/YYYY-MM-DD.py` (e.g. `pages/2025-07-08.py`) with that week's analysis.
- Download the week's data once so `data/week_YYYY-MM-DD/` exists (the page can call `save_tidy_tuesday_data`, or run it from a shell):

   ```bash
   python -c "from utils.io import save_tidy_tuesday_data; save_tidy_tuesday_data('2025-07-08')"
   ```

- The page is picked up automatically by `main.py` and listed in the sidebar as `YYYY-MM-DD · <dataset title>`, with the title read from `data/week_YYYY-MM-DD/meta.yaml`.
