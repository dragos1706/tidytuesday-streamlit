import altair as alt
import pandas as pd

def altair_histogram(df: pd.DataFrame, column: str) -> alt.Chart:
    return alt.Chart(df).mark_bar().encode(
        alt.X(column, bin=True),
        y='count()'
    ).properties(width=600)