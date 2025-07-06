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
- Copy pages/template_week.py → rename it to pages/2_2025_07_08.py, etc.
- Add that week's CSV to the data/ folder
- Replace placeholder content in the new template_weekly.py file with your new analysis.