"""
Reusable Streamlit UI components.

The sidebar filters were previously duplicated verbatim in several pages;
``render_filters`` centralises them while keeping the exact same labels,
defaults and behaviour.
"""

import pandas as pd
import streamlit as st

from utils.data import SELECT_ALL

# Filter definition: (sidebar label, dataframe column)
FILTER_FIELDS = [
    ("📅 Year", "Year"),
    ("Category", "Category"),
    ("Payment Method", "Payment Method"),
    ("Location", "Location"),
]


def sidebar_heading() -> None:
    """Render the sidebar heading shown on the filtered pages."""
    st.sidebar.markdown("## 🔎 Dashboard Filters")


def render_filters(df: pd.DataFrame, key_prefix: str = "") -> dict[str, list]:
    """Render the sidebar multiselect filters and return the selections.

    Parameters
    ----------
    df:
        Source dataframe used to populate the filter options.
    key_prefix:
        Optional prefix so multiple pages can share the same widget keys
        without colliding.

    Returns
    -------
    dict
        Mapping of column name -> selected values.
    """
    sidebar_heading()
    selections: dict[str, list] = {}

    for label, column in FILTER_FIELDS:
        if column not in df.columns:
            continue
        options = [SELECT_ALL] + df[column].dropna().unique().tolist()
        selections[column] = st.sidebar.multiselect(
            label,
            options,
            default=[SELECT_ALL],
            key=f"{key_prefix}_filter_{column}",
        )

    return selections
