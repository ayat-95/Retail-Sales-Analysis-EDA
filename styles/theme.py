"""
Shared visual theme for the Retail Store Sales Analysis dashboard.

Centralising the CSS avoids repeating the same <style> block in every page
and keeps the dashboard's look consistent across the whole app.

Colours are kept identical to the original design.
"""

import streamlit as st

# ---------------------------------------------------------------------------
# Brand palette (unchanged from the original dashboard)
# ---------------------------------------------------------------------------
BRAND_DARK = "#172033"
BRAND_GREEN = "#245C54"
BRAND_ACCENT = "#097C77"
BRAND_MINT = "#19B5D8"
SURFACE = "#F6F8FB"
BORDER = "#D9E1EA"

# Chart palette reused by the categorical/pie visualisations
CHART_GREENS = [
    "#245C54",
    "#03302D",
    "#12927F",
    "#24DAB8",
    "#3F8278",
    "#6FAF9A",
    "#8FBFAF",
    "#A8D5C8",
]

# CSS shared by every page. `variant` lets a page pick the accent title colour.
_CSS_TEMPLATE = """
<style>
    /* Main background */
    .stApp {
        background-color: #F6F8FB;
    }

    /* Main content */
    .main .block-container {
        padding-top: 2rem;
        padding-left: 3rem;
        padding-right: 3rem;
        max-width: 1500px;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #EEF2F7;
        border-right: 1px solid #D9E1EA;
    }

    section[data-testid="stSidebar"] > div {
        padding-top: 2rem;
    }

    /* Green accents for selected sidebar filters */
    section[data-testid="stSidebar"] [data-baseweb="tag"] {
        background-color: #245C54;
    }

    section[data-testid="stSidebar"] [data-baseweb="select"] > div:focus-within {
        border-color: #245C54;
        box-shadow: 0 0 0 1px #245C54;
    }

    section[data-testid="stSidebar"] [role="option"][aria-selected="true"] {
        background-color: #E6F7F3;
    }

    /* Dashboard title */
    .dashboard-title {
        font-size: 38px;
        font-weight: 800;
        color: __TITLE_COLOR__;
        margin-bottom: 5px;
    }

    .dashboard-subtitle {
        font-size: 16px;
        color: __SUBTITLE_COLOR__;
        margin-bottom: 25px;
    }

    /* KPI Card */
    .kpi-card {
        background-color: __KPI_COLOR__;
        padding: 22px;
        border-radius: 15px;
        min-height: 135px;
        box-shadow: 0px 5px 15px rgba(23, 35, 56, 0.12);
        margin-bottom: 20px;
    }

    .kpi-title {
        color: #9FB2CC;
        font-size: 13px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    .kpi-value {
        color: white;
        font-size: 30px;
        font-weight: 800;
        margin-top: 10px;
    }

    .kpi-description {
        color: #36C9A5;
        font-size: 13px;
        margin-top: 5px;
    }

    /* Section title */
    .section-title {
        border-left: 5px solid #19B5D8;
        padding-left: 12px;
        color: #172033;
        font-size: 22px;
        font-weight: 750;
        margin-top: 25px;
        margin-bottom: 20px;
    }

    /* Insight box */
    .insight-box {
        background-color: white;
        border-radius: 15px;
        padding: 20px;
        border: 1px solid #E5EAF0;
        box-shadow: 0px 4px 12px rgba(23, 35, 56, 0.06);
    }
</style>
"""


def apply_theme(title_color: str = "#172033", subtitle_color: str = "#6B7280",
                kpi_color: str = "#172338") -> None:
    """Inject the shared dashboard CSS into the current page.

    Parameters
    ----------
    title_color:
        Colour of the main dashboard title.
    subtitle_color:
        Colour of the dashboard subtitle.
    kpi_color:
        Background colour of the KPI cards.
    """
    css = (
        _CSS_TEMPLATE
        .replace("__TITLE_COLOR__", title_color)
        .replace("__SUBTITLE_COLOR__", subtitle_color)
        .replace("__KPI_COLOR__", kpi_color)
    )
    st.markdown(css, unsafe_allow_html=True)


def kpi_card(title: str, value: str) -> None:
    """Render a single KPI card using the shared card styling."""
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-title">{title}</div>
            <div class="kpi-value">{value}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def section_title(text: str) -> None:
    """Render a section heading with the shared accent bar."""
    st.markdown(
        f'<div class="section-title">{text}</div>',
        unsafe_allow_html=True,
    )
