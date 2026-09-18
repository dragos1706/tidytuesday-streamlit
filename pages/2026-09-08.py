import streamlit as st
import pandas as pd
import altair as alt
from pathlib import Path
from utils.io import save_tidy_tuesday_data, load_tidy_tuesday_data


date_str = "2026-09-08"  # TidyTuesday date in YYYY-MM-DD format

st.title(f"TidyTuesday: {date_str} — The Cappuccino Index")

st.markdown("""
In [a video](https://www.youtube.com/watch?v=WtlE3BW9Nqs), James Hoffmann asked a simple question:
**how many minutes does a barista have to work to afford a small cappuccino in their own café?**
He crowdsourced prices and hourly wages from ~2,600 cafés in 87 countries and called the answer the *cappuccino index*.

A few caveats before you start clicking:
- Tips are excluded, so countries with a tipping culture look harsher than they are.
- Sample sizes are wildly uneven: the USA and UK have ~600 cafés each, while more than 30 countries have a single café.
  Use the **minimum cafés per country** slider in the sidebar to see how much the ranking depends on small samples.
- All prices and wages were converted to GBP by the video's author.
""")


# ------------------------------------------------------------------ data
@st.cache_data
def load_data(date_str: str) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Download (if missing), load and tidy this week's two tables."""
    if not Path("data", f"week_{date_str}").exists():
        save_tidy_tuesday_data(date_str)
    dfs = load_tidy_tuesday_data(date_str)

    cafe = dfs["cafe"].copy()
    official = dfs["cappuccino_index"].copy()

    # New Zealand and South Africa contain a non-breaking space in the raw data
    for df in (cafe, official):
        df["country"] = df["country"].str.replace(" ", " ", regex=False)

    cafe["index_min"] = cafe["price_gbp"] / cafe["hourly_wage_gbp"] * 60
    n_flags = cafe[["urban", "suburban", "rural"]].sum(axis=1)
    cafe["area"] = "Mixed"
    cafe.loc[(n_flags == 1) & cafe["urban"], "area"] = "Urban"
    cafe.loc[(n_flags == 1) & cafe["suburban"], "area"] = "Suburban"
    cafe.loc[(n_flags == 1) & cafe["rural"], "area"] = "Rural"
    cafe["currency_code"] = cafe["original_currency"].str[:3]
    return cafe, official


def summarise_by_country(cafe: pd.DataFrame) -> pd.DataFrame:
    """Recompute the cappuccino index (ratio of sums, as in the original) plus spread stats."""
    summary = (
        cafe.groupby("country")
        .agg(
            n=("price_gbp", "size"),
            sum_price=("price_gbp", "sum"),
            sum_wage=("hourly_wage_gbp", "sum"),
            median_price_gbp=("price_gbp", "median"),
            median_wage_gbp=("hourly_wage_gbp", "median"),
            price_q1=("price_gbp", lambda s: s.quantile(0.25)),
            price_q3=("price_gbp", lambda s: s.quantile(0.75)),
            index_mean=("index_min", "mean"),
            index_std=("index_min", "std"),
            pct_urban=("urban", "mean"),
        )
        .reset_index()
    )
    summary["index"] = summary["sum_price"] / summary["sum_wage"] * 60
    summary["price_iqr"] = summary["price_q3"] - summary["price_q1"]
    summary["index_cv"] = summary["index_std"] / summary["index_mean"]
    summary["pct_urban"] = summary["pct_urban"] * 100
    minutes = summary["index"].astype(int)
    seconds = ((summary["index"] - minutes) * 60).astype(int)
    summary["index_as_time"] = minutes.astype(str) + ":" + seconds.astype(str).str.zfill(2)
    return summary.drop(columns=["sum_price", "sum_wage", "price_q1", "price_q3", "index_mean", "index_std"])


cafe, official = load_data(date_str)

with st.expander("Peek at the raw tables"):
    st.write("`cafe` — one row per café")
    st.dataframe(cafe.head(), hide_index=True)
    st.write("`cappuccino_index` — the official per-country index from the video")
    st.dataframe(official.head(), hide_index=True)


# ------------------------------------------------------------------ sidebar filters
st.sidebar.header("Filters")

min_n = st.sidebar.slider(
    "Minimum cafés per country",
    min_value=1, max_value=100, value=5,
    help="Countries with fewer cafés than this are dropped everywhere on the page.",
)

area_options = ["Urban", "Suburban", "Rural", "Mixed"]
selected_areas = st.sidebar.multiselect("Area type", options=area_options, default=area_options)

cafe_area = cafe[cafe["area"].isin(selected_areas)]
counts = cafe_area["country"].value_counts()
eligible_countries = sorted(counts[counts >= min_n].index.tolist())

selected_countries = st.sidebar.multiselect(
    "Countries",
    options=eligible_countries,
    default=eligible_countries,
    help="Only countries passing the minimum-cafés filter are listed.",
)

filtered = cafe_area[cafe_area["country"].isin(selected_countries)]
summary = summarise_by_country(filtered)
summary = summary.merge(
    official[["country", "index_as_time"]].rename(columns={"index_as_time": "official_index_as_time"}),
    on="country", how="left",
)

st.sidebar.caption(
    f"{len(filtered):,} of {len(cafe):,} cafés · {summary['country'].nunique()} of {cafe['country'].nunique()} countries"
)

if filtered.empty:
    st.warning("No cafés match the current filters. Loosen them in the sidebar.")
    st.stop()


# ------------------------------------------------------------------ A. ranking
st.header("A. Country ranking")
st.markdown("Pick what to rank by. Bars are shaded by sample size, so pale bars are the ones to distrust.")

metric_labels = {
    "index": "Cappuccino index (minutes of work)",
    "median_price_gbp": "Median cappuccino price (GBP)",
    "median_wage_gbp": "Median hourly wage (GBP)",
    "price_iqr": "Price spread within country (IQR, GBP)",
}
col1, col2, col3 = st.columns([2, 1, 1])
metric = col1.selectbox("Rank by", options=list(metric_labels), format_func=metric_labels.get)
order = col2.radio("Order", options=["Highest first", "Lowest first"], horizontal=True)
top_n = col3.slider("Show top N", min_value=5, max_value=max(5, len(summary)), value=min(20, len(summary)))

ranked = summary.sort_values(metric, ascending=(order == "Lowest first")).head(top_n)

ranking_chart = (
    alt.Chart(ranked)
    .mark_bar()
    .encode(
        x=alt.X(f"{metric}:Q", title=metric_labels[metric]),
        y=alt.Y("country:N", sort=ranked["country"].tolist(), title=None),
        color=alt.Color(
            "n:Q",
            title="Cafés",
            scale=alt.Scale(type="log", scheme="viridis"),
        ),
        tooltip=[
            alt.Tooltip("country:N", title="Country"),
            alt.Tooltip("index_as_time:N", title="Index (mm:ss)"),
            alt.Tooltip("n:Q", title="Cafés"),
            alt.Tooltip("median_price_gbp:Q", title="Median price £", format=".2f"),
            alt.Tooltip("median_wage_gbp:Q", title="Median wage £/h", format=".2f"),
            alt.Tooltip("price_iqr:Q", title="Price IQR £", format=".2f"),
        ],
    )
    .properties(height=max(300, 22 * len(ranked)))
)
st.altair_chart(ranking_chart, use_container_width=True)


# ------------------------------------------------------------------ B. variability
st.header("B. How much does the index vary within a country?")
st.markdown(
    "The official index is one number per country, but individual cafés spread widely. "
    "Boxes show the per-café index; dots are the cafés themselves."
)

default_compare = summary.nlargest(8, "n")["country"].tolist()
compare_countries = st.multiselect(
    "Countries to compare",
    options=sorted(summary["country"]),
    default=default_compare,
    key="compare_countries",
)
log_y = st.checkbox("Log scale (tames the extreme outliers)", value=False, key="log_box")

compare_df = filtered[filtered["country"].isin(compare_countries)]
if compare_df.empty:
    st.info("Select at least one country.")
else:
    y_scale = alt.Scale(type="log") if log_y else alt.Scale(zero=False)
    base = alt.Chart(compare_df).encode(
        x=alt.X("country:N", title=None, sort=compare_countries),
        y=alt.Y("index_min:Q", title="Minutes of work per cappuccino", scale=y_scale),
    )
    boxes = base.mark_boxplot(extent="min-max", opacity=0.5, size=30)
    dots = (
        base.mark_circle(size=30, opacity=0.6)
        .transform_calculate(jitter="sqrt(-2*log(random()))*cos(2*PI*random())")
        .encode(
            xOffset=alt.XOffset("jitter:Q", scale=alt.Scale(domain=[-4, 4])),
            color=alt.Color("area:N", title="Area"),
            tooltip=[
                alt.Tooltip("country:N", title="Country"),
                alt.Tooltip("city:N", title="City"),
                alt.Tooltip("area:N", title="Area"),
                alt.Tooltip("price_gbp:Q", title="Price £", format=".2f"),
                alt.Tooltip("hourly_wage_gbp:Q", title="Wage £/h", format=".2f"),
                alt.Tooltip("index_min:Q", title="Minutes", format=".1f"),
            ],
        )
    )
    st.altair_chart((boxes + dots).properties(height=420), use_container_width=True)


# ------------------------------------------------------------------ C. scatter
st.header("C. Price vs wage, café by café")
st.markdown(
    "Every dot is one café. Lines of constant index are diagonals through the origin: "
    "the steeper the point sits above the pack, the longer the barista works for their coffee. "
    "Drag to pan, scroll to zoom."
)
c1, c2 = st.columns([1, 1])
color_by = c1.selectbox("Colour by", options=["area", "country"], format_func=str.title, key="scatter_color")
log_xy = c2.checkbox("Log axes", value=False, key="log_scatter")

axis_scale = alt.Scale(type="log") if log_xy else alt.Scale(zero=False)
scatter = (
    alt.Chart(filtered)
    .mark_circle(size=45, opacity=0.6)
    .encode(
        x=alt.X("hourly_wage_gbp:Q", title="Barista hourly wage (GBP)", scale=axis_scale),
        y=alt.Y("price_gbp:Q", title="Small cappuccino price (GBP)", scale=axis_scale),
        color=alt.Color(f"{color_by}:N", title=color_by.title(),
                        legend=alt.Legend(columns=2) if color_by == "country" else alt.Legend()),
        tooltip=[
            alt.Tooltip("country:N", title="Country"),
            alt.Tooltip("city:N", title="City"),
            alt.Tooltip("area:N", title="Area"),
            alt.Tooltip("price_gbp:Q", title="Price £", format=".2f"),
            alt.Tooltip("hourly_wage_gbp:Q", title="Wage £/h", format=".2f"),
            alt.Tooltip("index_min:Q", title="Minutes", format=".1f"),
        ],
    )
    .interactive()
    .properties(height=450)
)
st.altair_chart(scatter, use_container_width=True)


# ------------------------------------------------------------------ D. tables
st.header("D. Tables")

st.subheader("Country summary")
st.markdown(
    "Click a column header to sort. The **official** column comes from the video's own table "
    "(all cafés, no filters) so you can see how the filters move the index."
)
summary_view = summary[
    ["country", "n", "index", "index_as_time", "official_index_as_time",
     "median_price_gbp", "median_wage_gbp", "price_iqr", "index_cv", "pct_urban"]
].sort_values("index")

st.dataframe(
    summary_view,
    hide_index=True,
    use_container_width=True,
    column_config={
        "country": st.column_config.TextColumn("Country"),
        "n": st.column_config.NumberColumn("Cafés", format="%d"),
        "index": st.column_config.ProgressColumn(
            "Index (minutes)", format="%.1f",
            min_value=0, max_value=float(summary_view["index"].max()),
        ),
        "index_as_time": st.column_config.TextColumn("Index (mm:ss)"),
        "official_index_as_time": st.column_config.TextColumn("Official (mm:ss)"),
        "median_price_gbp": st.column_config.NumberColumn("Median price", format="£%.2f"),
        "median_wage_gbp": st.column_config.NumberColumn("Median wage /h", format="£%.2f"),
        "price_iqr": st.column_config.NumberColumn("Price IQR", format="£%.2f"),
        "index_cv": st.column_config.NumberColumn("Index CV", format="%.2f",
                                                  help="Std / mean of the per-café index. Blank when n = 1."),
        "pct_urban": st.column_config.NumberColumn("Urban", format="%.0f%%"),
    },
)
st.download_button(
    "Download country summary (CSV)",
    data=summary_view.to_csv(index=False).encode("utf-8"),
    file_name=f"cappuccino_index_summary_{date_str}.csv",
    mime="text/csv",
)

st.subheader("Cafés")
search = st.text_input("Search by country or city", placeholder="e.g. Lisbon, Portugal, Mumbai")
cafe_view = filtered[
    ["country", "city", "area", "price_gbp", "hourly_wage_gbp", "index_min", "currency_code", "price", "hourly_wage"]
]
if search:
    q = search.strip().lower()
    cafe_view = cafe_view[
        cafe_view["country"].str.lower().str.contains(q, na=False)
        | cafe_view["city"].str.lower().str.contains(q, na=False)
    ]
st.caption(f"{len(cafe_view):,} cafés shown")
st.dataframe(
    cafe_view.sort_values("index_min", ascending=False),
    hide_index=True,
    use_container_width=True,
    column_config={
        "country": st.column_config.TextColumn("Country"),
        "city": st.column_config.TextColumn("City"),
        "area": st.column_config.TextColumn("Area"),
        "price_gbp": st.column_config.NumberColumn("Price", format="£%.2f"),
        "hourly_wage_gbp": st.column_config.NumberColumn("Wage /h", format="£%.2f"),
        "index_min": st.column_config.NumberColumn("Minutes of work", format="%.1f"),
        "currency_code": st.column_config.TextColumn("Currency"),
        "price": st.column_config.NumberColumn("Local price", format="%.2f"),
        "hourly_wage": st.column_config.NumberColumn("Local wage /h", format="%.2f"),
    },
)
st.download_button(
    "Download cafés (CSV)",
    data=cafe_view.to_csv(index=False).encode("utf-8"),
    file_name=f"cafes_{date_str}.csv",
    mime="text/csv",
)
