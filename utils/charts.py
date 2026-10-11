"""
Reusable Plotly chart builders used by the Sales Overview page.

Each function returns a figure (it does not render it), so the caller keeps
full control over layout in Streamlit.
"""

import pandas as pd
import plotly.express as px

from styles.theme import BRAND_ACCENT, CHART_GREENS

MONTH_ORDER = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December",
]


def revenue_by_year(df: pd.DataFrame):
    """Bar chart: total revenue per year."""
    data = df.sort_values(by="Transaction Date", ascending=True)
    data = data.groupby("Year")["Total Spent"].sum().reset_index()

    fig = px.bar(
        data_frame=data,
        x="Year",
        y="Total Spent",
        title="Revenue Trend Over Time",
        color_discrete_sequence=[BRAND_ACCENT],
        text_auto=True,
    )
    fig.update_traces(texttemplate="%{y:.0f}", textposition="outside")
    fig.update_layout(margin=dict(t=50))
    fig.update_xaxes(type="category")
    fig.update_yaxes(title_text="Total Revenue", showticklabels=False)
    return fig


def revenue_by_month(df: pd.DataFrame):
    """Line chart: total revenue per month (calendar ordered)."""
    data = df.groupby("Month")["Total Spent"].sum().reset_index()
    data["Month"] = pd.Categorical(
        data["Month"], categories=MONTH_ORDER, ordered=True
    )
    data = data.sort_values("Month")

    fig = px.line(
        data_frame=data,
        x="Month",
        y="Total Spent",
        title="Revenue Trend Over Months",
        color_discrete_sequence=[BRAND_ACCENT],
        category_orders={"Month": MONTH_ORDER},
        markers=True,
    )
    fig.update_yaxes(title_text="", showticklabels=True)
    fig.update_layout(margin=dict(t=50))
    return fig


def revenue_by_day_type(df: pd.DataFrame):
    """Bar chart: average revenue by weekend vs weekday."""
    data = (
        df.groupby("Day_type")["Total Spent"]
        .mean()
        .sort_values(ascending=False)
        .reset_index()
    )

    fig = px.bar(
        data_frame=data,
        x="Day_type",
        y="Total Spent",
        title="Revenue by Day Type",
        text_auto=True,
        labels={"Day_type": "", "Total Spent": ""},
        color_discrete_sequence=[BRAND_ACCENT],
    )
    fig.update_traces(textposition="outside")
    fig.update_yaxes(showticklabels=False)
    fig.update_layout(margin=dict(t=50))
    return fig
