import streamlit as st

from styles.theme import apply_theme, kpi_card, section_title
from utils.charts import (
    revenue_by_day_type,
    revenue_by_month,
    revenue_by_year,
)
from utils.data import apply_filters, load_data
from utils.ui import render_filters

# ==================================================================

# Page Configration

st.set_page_config(page_title= 'Retail sales Analysis',
                    layout= 'wide',
                    page_icon = "")

# =================================================================
# CSS

# Shared dashboard styling (see styles/theme.py)
apply_theme(title_color="#245c54", subtitle_color="#245c54", kpi_color="#245c54")

#==================================================================
#Title in html

st.markdown(
    '<div class="dashboard-title">🛍️ Retail Store Sales Dashboard</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="dashboard-subtitle">'
    'Overview of retail store sales performance and customer behavior'
    '</div>',
    unsafe_allow_html=True
)
#===================================================================

# insert pic
# st.image ('shutterstock_342248561_688941.jpg')

#==================================================================
# Load Data

df = load_data()

#====================================================================

# Fillters

selections = render_filters(df, key_prefix="overview")

#==========================================================================
# Applied Filters

filterd_df = apply_filters(df, selections)


#==============================================================================
# KPIs

# Calculations

Total_Revenue = filterd_df['Total Spent'].sum()
Total_Quantity_Sold = filterd_df['Quantity'].sum()
Unique_Customers = filterd_df['Customer ID'].nunique()
Total_Transactions = filterd_df['Transaction ID'].count()

#KPIs Cards

col1, col2, col3 ,col4 =st.columns(4)

with col1:
    kpi_card("Total Revenue", f"${Total_Revenue:,.0f}")


with col2:
    kpi_card("Transactions", f"{Total_Transactions:,}")


with col3:
    kpi_card(" Quantity Sold", f"{Total_Quantity_Sold:,.0f}")


with col4:
    kpi_card(" Uniqe Customer ", f"{Unique_Customers:,}")

#==================================================================================

# Title of Sales Performance

section_title("📊 Sales Performance")


#=================================================================================

chart1, chart2 = st.columns(2)
# Total Yearly Revenue

with chart1:
    st.plotly_chart(revenue_by_year(filterd_df))

with chart2:
##Total Monthly Revenue
    st.plotly_chart(revenue_by_month(filterd_df))


#===========================================================
# Difference in revenue between weekdays and weekends

st.plotly_chart(revenue_by_day_type(filterd_df))  
    
