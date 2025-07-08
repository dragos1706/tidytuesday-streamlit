import streamlit as st
from types import SimpleNamespace
import pandas as pd
import altair as alt
from utils.plotting import altair_histogram
from utils.transform import basic_clean
from utils.io import save_tidy_tuesday_data, load_tidy_tuesday_data
from utils.plotting import altair_bar_chart
from utils.plotting_plotnine import plotnine_bar_chart




date_str = "2025-06-17" # TidyTuesday date in YYYY-MM-DD format

st.title(f"TidyTuesday: {date_str}")
folder_path = save_tidy_tuesday_data(date_str)
dfs = load_tidy_tuesday_data("2025-06-17")
st.write("Loaded datasets:", list(dfs.keys()))

# Convert the dictionary of DataFrames to a SimpleNamespace for easier access
# You can access the datasets using `dfs.dataset_name` where `dataset_name` is the name of the dataset without the `.csv` extension.
# # For example, to access the API categories dataset, use `dfs.api_categories`.
dfs = SimpleNamespace(**dfs)


# e.g. dfs.api_categories, dfs.api_info, etc.   

# list all datasets
st.subheader("Available Datasets")
st.write("Here are the first few rows of each dataset:")
for name, df in dfs.__dict__.items():
    st.subheader(name)
    st.dataframe(df.head())

# One way of producing a barplot using Altair
st.altair_chart(
    alt.Chart(dfs.api_categories) \
        .mark_bar() \
        .encode(x = "apisguru_category", y = "count()"), 
    use_container_width=True
    )

# Another way of producing a barplot using a custom utility function
st.altair_chart(
    altair_bar_chart(dfs.api_categories, "apisguru_category"), 
                    use_container_width=True
                )

# Using Plotnine to create a bar chart
st.subheader("Bar Chart using Plotnine")
st.pyplot(
    plotnine_bar_chart(dfs.api_categories, "apisguru_category")
)
