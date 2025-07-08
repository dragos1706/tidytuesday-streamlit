import streamlit as st

st.set_page_config(page_title="TidyTuesday EDA", layout="wide")

st.title("📊 TidyTuesday EDA Viewer")

st.markdown("""
Welcome! This app hosts your weekly **TidyTuesday** data explorations.
Use the sidebar to navigate to each week's analysis.

**Raison d'être**:       
I've built this app because I wanted to familiarise myself with the Streamlit framework and its capabilities. 
I feel that TidyTuesday data is a great way to explore this, as it provides a wide range of datasets that can be used for various types of analyses and visualisations.

The focus of each week's exploration is to showcase how Streamlit could be used to maximise interactivity and visualisation of the data.
There is one dashboard for each week, which contains a variety of interactive widgets and visualisations that allow users to explore the data in different ways.
As such , each week's dashboard isn't designed to be an analysis itself, but rather to allow user to analyse the data through the use of interactive widgets and visualisations.
""")

st.markdown("""
**How to use this app**:
- Use the sidebar to navigate to each week's analysis.
- Each week has its own dashboard, which contains a variety of interactive widgets and visualisations that allow users to explore the data in different ways.
- You can interact with the widgets to filter the data, change the visualisations, and explore the data in different ways.
- The app is designed to be interactive, so feel free to explore the data and visualisations as you wish.
"""
)

st.markdown("""
**A note on expectations**:
            Some of the dashboards might be very basic, as I am still learning how to use Streamlit and its capabilities.
            I am constantly improving the app and adding new features, so future weeks will likely have more advanced features and visualisations.
            """
)