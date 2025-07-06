import streamlit as st
from utils.io import load_csv
from utils.plotting import altair_histogram
from utils.transform import basic_clean

st.title("TidyTuesday: YYYY-MM-DD")

# df = load_csv("data/YYYY-MM-DD.csv")
# df = basic_clean(df)

st.subheader("Data Preview")
# st.dataframe(df.head())

st.subheader("Replace with analysis")