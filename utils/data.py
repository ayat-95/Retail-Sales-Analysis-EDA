"""
Data loading, filtering and the data-dictionary builder.

All pages now share a single, cached loader instead of each re-reading the
parquet file on every rerun.
"""

from pathlib import Path

import pandas as pd
import streamlit as st

from utils.paths import DATA_PARQUET, DATA_CSV

# Human-readable description for every column in the dataset.
COLUMN_DESCRIPTIONS = {
    "Transaction ID": "Unique identifier assigned to each sales transaction.",
    "Customer ID": "Unique identifier assigned to the purchasing customer.",
    "Category": "Product category/department (e.g., Patisserie, Milk Products, Butchers).",
    "Item": "Specific product name or item code sold.",
    "Price Per Unit": "Cost of a single unit of the item (in USD/local currency).",
    "Quantity": "Number of units purchased in the transaction.",
    "Total Spent": "Total cost for the item purchase (Price Per Unit x Quantity).",
    "Payment Method": "Method of payment used (e.g., Digital Wallet, Credit Card, Cash).",
    "Location": "Sales channel or store location type (e.g., Online, In-store).",
    "Transaction Date": "Date when the transaction occurred (YYYY-MM-DD).",
    "Discount Applied": "Flag indicating whether a discount was applied to the sale (True/False/Unknown).",
    "Year": "Year of the transaction.",
    "Month": "Month of the year.",
    "Day": "Day of the week.",
    "Day_type": "Whether the transaction happened on a weekend or a weekday.",
}

SELECT_ALL = "Select All"


@st.cache_data(show_spinner=False)
def load_data(path: str | Path | None = None) -> pd.DataFrame:
    """Load the cleaned retail dataset (parquet preferred, CSV fallback)."""
    parquet_path = Path(path) if path else DATA_PARQUET

    if parquet_path.exists():
        df = pd.read_parquet(parquet_path)
    elif DATA_CSV.exists():
        df = pd.read_csv(DATA_CSV)
    else:
        raise FileNotFoundError(
            f"Could not find the dataset. Expected '{parquet_path.name}' "
            f"or '{DATA_CSV.name}' in the project root."
        )

    if "Transaction Date" in df.columns:
        df["Transaction Date"] = pd.to_datetime(
            df["Transaction Date"], errors="coerce"
        )
    return df


def apply_filters(df: pd.DataFrame, selections: dict[str, list]) -> pd.DataFrame:
    """Apply the sidebar selections to the dataframe.

    ``selections`` maps a column name to the list of chosen values. A column is
    ignored when it contains the ``Select All`` sentinel, which matches the
    original filter behaviour.
    """
    filtered = df.copy()
    for column, values in selections.items():
        if not values or SELECT_ALL in values:
            continue
        if column in filtered.columns:
            filtered = filtered[filtered[column].isin(values)]
    return filtered


def build_data_dictionary(df: pd.DataFrame) -> pd.DataFrame:
    """Return a two-column (Column Name, Description) data dictionary."""
    return pd.DataFrame(
        [
            {
                "Column Name": column,
                "Description": COLUMN_DESCRIPTIONS.get(
                    column, "No description available."
                ),
            }
            for column in df.columns
        ]
    )
