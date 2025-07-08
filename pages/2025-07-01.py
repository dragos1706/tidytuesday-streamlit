import streamlit as st
from types import SimpleNamespace
import pandas as pd
import altair as alt
import plotnine as p9
from typing import Tuple
from utils.plotting import altair_histogram, altair_boxplot, altair_scatter, altair_bar_chart, altair_line_chart
from utils.plotting_plotnine import plotnine_histogram, plotnine_boxplot, plotnine_scatter, plotnine_bar_chart, plotnine_line_chart
from utils.transform import basic_clean 
from utils.io import save_tidy_tuesday_data, load_tidy_tuesday_data
from utils.plotting import altair_bar_chart
from utils.plotting_plotnine import plotnine_bar_chart




date_str = "2025-07-01" # TidyTuesday date in YYYY-MM-DD format

st.title(f"TidyTuesday: {date_str}")
folder_path = save_tidy_tuesday_data(date_str)
dfs = load_tidy_tuesday_data(date_str)
st.write("Loaded datasets:", list(dfs.keys()))

# Convert the dictionary of DataFrames to a SimpleNamespace for easier access
# You can access the datasets using `dfs.dataset_name` where `dataset_name` is the name of the dataset without the `.csv` extension.
# # For example, to access the API categories dataset, use `dfs.api_categories`.
dfs = SimpleNamespace(**dfs)

# list all datasets
st.subheader("Available Datasets")
st.write("Here are the first few rows of each dataset:")
for name, df in dfs.__dict__.items():
    st.subheader(name)
    st.dataframe(df.head())

# prep data
df = dfs.weekly_gas_prices.copy()
df["date"] = pd.to_datetime(df["date"]) 

# Date range filter 
min_date = df["date"].dt.date.min()
max_date = df["date"].dt.date.max()
date_range = st.sidebar.date_input(
    "Select date range:",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)
    # Unpack the date range
start_date, end_date = date_range
# Convert date range to datetime
start_date = pd.to_datetime(start_date)
end_date = pd.to_datetime(end_date) 

# Fuel filter widget
fuel_types = df["fuel"].unique().tolist()
selected_types = st.sidebar.multiselect(
    "Select fuel type(s):",
    options=fuel_types,
    default=fuel_types
)

# Formulation filter
formulations = df["formulation"].unique().tolist()
selected_forms = st.sidebar.multiselect(
    "Select formulation(s):",
    options=formulations,
    default=formulations
)

# Grade filter
grades = df["grade"].unique().tolist()
selected_grades = st.sidebar.multiselect(
    "Select grade(s):",
    options=grades,
    default=grades
)

# Filter the DataFrame
mask = (
    df["fuel"].isin(selected_types) &
    df["formulation"].isin(selected_forms) &
    df["grade"].isin(selected_grades) &
    (df["date"] >= start_date) &
    (df["date"] <= end_date)
)
filtered = df.loc[mask]

# Create the Altair chart
chart = (
    alt.Chart(filtered)
       .mark_line()
       .encode(
          x="date:T",
          y="price:Q",
          color="formulation:N"
       )
)

st.altair_chart(chart, use_container_width=True)