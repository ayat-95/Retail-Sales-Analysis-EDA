import pandas as pd
import numpy as np
import plotly.express as px
import streamlit  as st

# ==================================================================

# Page Configration

st.set_page_config(page_title= 'Retail sales Analysis',
                    layout= 'wide',
                    page_icon = "")

# =================================================================
# CSS

st.markdown("""
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

    /* Dashboard green accents for selected sidebar filters */
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
        color: #245c54;
        margin-bottom: 5px;
    }

    .dashboard-subtitle {
        font-size: 16px;
        color: #245c54;
        margin-bottom: 25px;
    }

    /* KPI Card */
    .kpi-card {
        background-color: #245c54;
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
""", unsafe_allow_html=True)

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

df = pd.read_parquet("retail_store_sales_clean.parquet")

#====================================================================

# Fillters 

st.sidebar.markdown(
    "## 🔎 Dashboard Filters"
)

# 1 Year filters
df_sorted = df.sort_values(by='Transaction Date', ascending=True)
Year_list = ["Select All"]+ df_sorted['Year'].unique().tolist()
selected_year = st.sidebar.multiselect("📅 Year",
  Year_list,default=["Select All"] 
)

# 2 Category 
Categories = df['Category'].unique()
Categor_list =["Select All"]+df['Category'].unique().tolist()
selected_Category = st.sidebar.multiselect('Category',
                                           Categor_list,
                                           default= ["Select All"]
                                           )

# 3 Payment Methods = 
Payment_Methods = df['Payment Method'].unique()
Method_list =["Select All"]+df['Payment Method'].unique().tolist()
selected_Payment_Method = st.sidebar.multiselect('Payment Method',
                                                 Method_list,
                                                 default=["Select All"]
                                                 
     )

# 4 Location
Locations = df['Location'].unique()
Location_list = ["Select All"]+df['Location'].unique().tolist()
selected_Location = st.sidebar.multiselect('Location',
                                            Location_list,
                                             default=["Select All"] )

#==========================================================================
# Applied Filters 

filterd_df = df.copy()

if "Select All" not in selected_year:
    filterd_df = filterd_df[filterd_df['Year'].isin(selected_year)]

if "Select All" not in selected_Category:    
    filterd_df=filterd_df[filterd_df['Category'].isin(selected_Category)]

if "Select All" not in selected_Payment_Method:     
   filterd_df=filterd_df[filterd_df['Payment Method'].isin(selected_Payment_Method)]

if "Select All" not in selected_Location:   
   filterd_df= filterd_df[filterd_df['Location'].isin(selected_Location)]


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
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">Total Revenue</div>
        <div class="kpi-value">${Total_Revenue:,.0f}</div>
    
    </div>
    """, unsafe_allow_html=True)


with col2:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">Transactions</div>
        <div class="kpi-value">{Total_Transactions:,}</div>
    </div>
    """, unsafe_allow_html=True)


with col3:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title"> Quantity Sold</div>
        <div class="kpi-value">{Total_Quantity_Sold:,.0f}</div>
    </div>
    """, unsafe_allow_html=True)


with col4:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title"> Uniqe Customer </div>
        <div class="kpi-value">{Unique_Customers:,}</div>
    </div>
    """, unsafe_allow_html=True)

#==================================================================================

# Title of Sales Performance

st.markdown(

    '<div class="section-title">📊 Sales Performance</div>',
    
    unsafe_allow_html=True
)



#=================================================================================

chart1, chart2 = st.columns(2)
# Total Yearly Revenue 

with chart1:
    df_sorted = filterd_df.sort_values(by='Transaction Date', ascending=True)
    Revenue_by_Year = df_sorted.groupby('Year')['Total Spent'].sum().reset_index()
    fig= px.bar(data_frame= Revenue_by_Year,
             x= 'Year',
             y= 'Total Spent',
             title= 'Revenue Trend Over Time',
             color_discrete_sequence=["#097C77"],
             text_auto=True
            )
    
    
    fig.update_traces(texttemplate='%{y:.0f}', textposition='outside')
    fig.update_layout (margin=dict(t=50))
    fig.update_xaxes(type='category')
    fig.update_yaxes(title_text='Total Revenue',
                     showticklabels=False,
                    )
    st.plotly_chart(fig) 

with chart2:
##Total Monthly Revenue
#      
    Revenue_by_Month = df_sorted.groupby('Month')['Total Spent'].sum().reset_index()

    month_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

    Revenue_by_Month['Month'] = pd.Categorical(Revenue_by_Month['Month'], categories=month_order, ordered=True)
    Revenue_by_Month = Revenue_by_Month.sort_values('Month')


    fig= px.line(data_frame = Revenue_by_Month,
            x= 'Month',
            y= 'Total Spent',
            title= 'Revenue Trend Over Months',
            color_discrete_sequence=["#097C77"],
            category_orders= {'Month': month_order},
            markers=True
            
            
            )


    fig.update_yaxes(title_text='',showticklabels=True)
    fig.update_layout(margin=dict(t=50))
    st.plotly_chart(fig)  


#===========================================================
# Difference in revenue between weekdays and weekends

week_day = filterd_df.groupby('Day_type')['Total Spent'].mean().sort_values(ascending=False).reset_index()

fig = px.bar(data_frame= week_day,
             x='Day_type',
             y='Total Spent',
             title='Revenue by Day Type',
             text_auto=True,
             labels={'Day_type': '', 'Total Spent': ''},
             color_discrete_sequence=["#097C77"])

fig.update_traces( textposition='outside')
fig.update_yaxes(showticklabels=False)
fig.update_layout(margin=dict(t=50))

st.plotly_chart(fig)  
    
