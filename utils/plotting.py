import altair as alt
import pandas as pd


def altair_histogram(df, column):
    return alt.Chart(df).mark_bar().encode(
        alt.X(column, bin=True),
        y='count()'
    ).properties(width=600)

def altair_boxplot(df, x_col, y_col):
    return alt.Chart(df).mark_boxplot().encode(
        x=x_col,
        y=y_col
    ).properties(width=600)

def altair_scatter(df, x_col, y_col):
    return alt.Chart(df).mark_circle(size=60).encode(
        x=x_col,
        y=y_col,
        tooltip=[x_col, y_col]
    ).interactive().properties(width=600)

def altair_bar_chart(df, category_col):
    return alt.Chart(df).mark_bar().encode(
        x=category_col,
        y='count()'
    ).properties(width=600)

def altair_line_chart(df, x_col, y_col):
    return alt.Chart(df).mark_line().encode(
        x=x_col,
        y=y_col
    ).properties(width=600)