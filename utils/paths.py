"""
Centralised project paths.

Paths are resolved relative to the project root (the folder that contains
``Home.py``) so the dashboard works no matter which directory Streamlit is
launched from.
"""

from pathlib import Path

# utils/paths.py -> project root is two levels up
ROOT_DIR = Path(__file__).resolve().parent.parent

DATA_PARQUET = ROOT_DIR / "retail_store_sales_clean.parquet"
DATA_CSV = ROOT_DIR / "retail_store_sales.csv"

ASSETS_DIR = ROOT_DIR
HOME_IMAGE = ASSETS_DIR / "Picture For Project.png"
STORE_IMAGE = ASSETS_DIR / "Picture For Project 2 .png.jpg"
