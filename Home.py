import pandas as pd
import numpy as np
import plotly.express as px
import streamlit  as st

# ==================================================================

# Page Configration

st.set_page_config(page_title= 'Retail sales Analysis',
                    layout= 'wide',
                    page_icon = "🛍️",
                    initial_sidebar_state="expanded"
                    )

#================================================

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

    /* Dashboard title */
    .dashboard-title {
        font-size: 38px;
        font-weight: 800;
        color: #172033;
        margin-bottom: 5px;
    }

    .dashboard-subtitle {
        font-size: 16px;
        color: #6B7280;
        margin-bottom: 25px;
    }

    /* KPI Card */
    .kpi-card {
        background-color: #172338;
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
""", unsafe_allow_html=True)

# =================================================================

# Center text and control color

html ="""
    <div style="text-align: center; color: Black ; font-size: 30px; font-weight: bold;">
       Retail sales Analysis
    </div>
    """
st.markdown(html, unsafe_allow_html= True)

#===================================================================

# insert pic 
st.image ('Picture For Project.png')


#==================================================================
st.header(" Project Overview")

st.markdown("""
### Objectives

- Analyze overall sales performance
- Identify high-performing products and categories
- Understand customer behavior
- Analyze payment methods and sales channels
- Evaluate discount and weekend behavior
- Perform statistical analysis
- Generate actionable business recommendations
""")




#==================================================================
# Load Data  

df = pd.read_parquet("retail_store_sales_clean.parquet")
#=================================================================

# Show sample from data 
st.subheader('Data Overview')
st.dataframe(df.head())

#====================================================================
# Data Description Table For all columns

st.title("Data Dictionary:")

# Column descriptions
descriptions = {
    "Transaction ID": "Unique identifier assigned to each sales transaction.",
    "Customer ID": "Unique identifier assigned to the purchasing customer.",
    "Category": "Product category/department (e.g., Patisserie, Milk Products, Butchers).",
    "Item": "Specific product name or item code sold.",
    "Price Per Unit": "Cost of a single unit of the item (in USD/local currency).",
    "Quantity": "Number of units purchased in the transaction.",
    "Total Spent": "Total cost for the item purchase (Price Per Unit × Quantity).",
    "Payment Method": "Method of payment used (e.g., Digital Wallet, Credit Card, Cash).",
    "Location": "Sales channel or store location type (e.g., Online, In-store).",
    "Transaction Date": "Date when the transaction occurred (YYYY-MM-DD).",
    "Discount Applied": "Boolean flag indicating whether a discount was applied to the sale (True/False).",
    "Year": "year.",
    "Month": "Month of the year.",
    "Day": "Day of the week."
    

}

# Construct dataframe with only Column Name and Description
schema_df = pd.DataFrame(
    [
        {
            "Column Name": col,
            "Description": descriptions.get(col, "No description available."),
        }
        for col in df.columns
    ]
)

# Render table in Streamlit
st.dataframe(
    schema_df,
    use_container_width=True,
    hide_index=True,
)
#===========================================================================
# to make space 
st.markdown("------")
#=================================================================================
# Make two tap For Numerical Analysis and Categorical Analysis

tab1,tab2  = st.tabs(["Numerical Analysis","Categorical Analysis"])

with tab1:
    st.subheader("Numerical Analysis")

    num_cols = df.select_dtypes(include='number').columns
    column_select =st.selectbox("Column name", num_cols)


    Chart_Select = st.radio('Chart',['Histogram','box plot'])

    if Chart_Select =='Histogram':
      st.plotly_chart( px.histogram(data_frame = df, 
                                    x=column_select ,
                                    title=column_select,
                                    color_discrete_sequence= ["#12927f"]))

    else: 
       st.plotly_chart(px.box(data_frame = df,
                               x=column_select ,
                               title=column_select
                               ).update_traces(marker_color= "#12927f"))

                    


with tab2:
    st.subheader("Categorical Analysis")

    Cat_cols = df.select_dtypes(include='object').columns.drop(['Transaction ID','Customer ID','Month','Day'])
    column_select =st.selectbox("Column name", Cat_cols)

    Chart_Select = st.radio('Chart',['Histogram','pie'])

    if Chart_Select =='Histogram':
         fig= px.histogram(data_frame = df,
                                         x=column_select ,
                                         title=column_select,
                                         text_auto=True,
                                         color_discrete_sequence= ["#12927f"])

         
         fig.update_xaxes(categoryorder='max descending') 
         st.plotly_chart(fig)
    
    else: 
           if df[column_select].nunique()>10:  
            st.warning("sory,this column has too many unique categories.'please change the chart type to Histogram")
           else:
             st.plotly_chart(px.pie(data_frame = df, 
                                    names=column_select ,
                                    title=column_select,
                                    color=column_select,
                                    color_discrete_sequence=[
                                        "#245C54",
                                        "#03302D",
                                        "#12927F",
                                        "#24DAB8",
                                        "#3F8278",
                                        "#6FAF9A",
                                        "#8FBFAF",
                                        "#A8D5C8",
                                    ]))
    

#======================================================================================
