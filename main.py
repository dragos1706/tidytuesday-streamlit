import streamlit as st
from utils.io import list_week_pages, read_week_title

st.set_page_config(page_title="TidyTuesday EDA", layout="wide")

# Explicit navigation so each week's label keeps its full date (Streamlit's
# automatic pages/ discovery would strip the leading year as a sort prefix).
home = st.Page("pages/home.py", title="Home", icon="🏠", default=True)

weeks = [
    st.Page(path, title=f"{date_str} · {read_week_title(date_str) or 'TidyTuesday'}", url_path=date_str)
    for date_str, path in list_week_pages()
]

sandbox = st.Page("pages/sandbox.py", title="Sandbox", icon="🧪")

st.navigation({"": [home], "Weekly dashboards": weeks, "Other": [sandbox]}).run()
