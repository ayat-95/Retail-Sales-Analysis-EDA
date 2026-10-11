import plotly.express as px
import streamlit  as st

from styles.theme import apply_theme, kpi_card
from utils.data import apply_filters, load_data
from utils.paths import STORE_IMAGE
from utils.ui import render_filters

# ==================================================================

# Page Configration

st.set_page_config(page_title= 'Retail sales Analysis',
                    layout= 'wide',
                    page_icon = "🛍️")

# =================================================================

# Center text and control color
# CSS

# Shared dashboard styling (see styles/theme.py)
apply_theme(title_color="#245c54", subtitle_color="#245c54", kpi_color="#245c54")

#==================================================================
#Title in html

st.markdown(
    '<div class="dashboard-title">Retail Store Sales Dashboard</div>',
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
st.image(str(STORE_IMAGE))
#==================================================================
#Title in html

st.markdown(
    '<div class="dashboard-title">Retail Store Analysis </div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="dashboard-subtitle">'
    'Understand product performance, customer behavior ,payment method and Location metrics '
    '</div>',
    unsafe_allow_html=True
)
#===========================================================================
# Load Data

df = load_data()


#==================================================================

# Fillters

selections = render_filters(df, key_prefix="store")

#==========================================================================
# Applied Filters

filterd_df = apply_filters(df, selections)

#========================================================================
# KPIs



# Calculations

Total_Revenue = filterd_df['Total Spent'].sum()
Total_Quantity_Sold = filterd_df['Quantity'].sum()
Unique_Customers = filterd_df['Customer ID'].nunique()
Total_Items = filterd_df['Item'].nunique()

#KPIs Cards

col1, col2, col3 ,col4 =st.columns(4)

with col1:
    kpi_card("Total Revenue", f"${Total_Revenue:,.0f}")


with col2:
    kpi_card("Total Items", f"{Total_Items:,}")


with col3:
    kpi_card(" Quantity Sold", f"{Total_Quantity_Sold:,.0f}")


with col4:
    kpi_card(" Unique Customer ", f"{Unique_Customers:,}")

#==================================================================================

# Title of Product Performance


#=========================================================================
# Tabs for Product Analysis and  Customer Analysis

tab1, tab2 ,tab3,tab4= st.tabs([
    " Product Analysis",
    " Customer Analysis",
    "  Payment Analysis",
    "  Location Analysis"

])
#========================================================================
 #  product category has the highest revenue
with tab1:

        Revenue_by_Category = filterd_df.groupby('Category')['Total Spent'].sum().sort_values(ascending=False).reset_index()

        fig = px.bar(data_frame=Revenue_by_Category,
                    x='Category',
                    y='Total Spent',
                    title='Revenue by Category',
                    text_auto=True,
                    color_continuous_scale='Mint',
                    color ='Total Spent',
        )

        fig.update_traces(texttemplate='%{y:.0f}', textposition='outside')
        fig.update_yaxes(title_text='Total Revenue',showticklabels=False)
        fig.update_layout(margin=dict(t=50))

        st.plotly_chart(fig)

        #====================================================================
        # Top(10) products has the biggest revenue contributors? 

        Revenue_by_products = filterd_df.groupby('Item')['Total Spent'].sum().sort_values(ascending=False).reset_index().head(10)

        fig = px.bar(data_frame= Revenue_by_products,
                    x='Item',
                    y='Total Spent',
                    title=' Top 10 Revenue by products',
                    text_auto=True,
                    color_continuous_scale='Mint',
                    color ='Total Spent',
                    )

        fig.update_traces(texttemplate='%{y:.0f}', textposition='outside')
        fig.update_yaxes(title_text='Total Revenue',showticklabels=False)
        fig.update_layout(margin=dict(t=50))

        st.plotly_chart(fig)

#============================================================================
# Top(10) customers generate the most revenue 
with tab2:
     
    customer_revenue = filterd_df.groupby('Customer ID')['Total Spent'].sum().reset_index().sort_values(by='Total Spent', ascending=False).head(10)

    fig = px.bar(data_frame= customer_revenue,
                x='Customer ID',
                y='Total Spent',
                title='Revenue by Customer ',
                text_auto=True,
                color_continuous_scale='Mint',
                            color ='Total Spent',
                
                )

    fig.update_traces(texttemplate='%{y:.0f}', textposition='outside')
    fig.update_yaxes(title_text='Total Revenue',showticklabels=False)
    fig.update_layout(margin=dict(t=50))

    st.plotly_chart(fig)

    #=============================================================================
    # customers who received discounts VS who did not receive discounts

    Discount_Vs_NonDiscount =filterd_df.groupby(['Discount Applied'])['Total Spent'].mean().sort_values(ascending=False).reset_index()
    fig= px.bar(data_frame= Discount_Vs_NonDiscount,
                x= 'Discount Applied',
                y= 'Total Spent',
                title= 'Discount vs Non-Discount Spending',
                color_continuous_scale='Mint',
                            color ='Total Spent',
                text_auto=True,
                labels={'Total Spent': 'Total Revenue', 'Discount Applied': 'Discount Applied'},
                

    )  
    fig.update_traces( textposition='outside')
    fig.update_yaxes(showticklabels=False)
    fig.update_layout(margin=dict(t=50))

    st.plotly_chart(fig)

    #================================================================================
    # customers make the most transactions

    customer_frequency = (
        filterd_df.groupby('Customer ID')['Transaction ID']
        .nunique()
        .reset_index(name='Transactions')
        .sort_values('Transactions', ascending=False)
        .head(10)
    )

    fig = px.bar(data_frame= customer_frequency,
                x='Transactions',
                y='Customer ID',
                title='Top 10 Transaction by Customer ',
                text_auto=True,
                color_continuous_scale='Mint',
                color ='Transactions',
                )

    fig.update_traces( textposition='outside')
    fig.update_yaxes(title_text='Customer ID')
    fig.update_layout(margin=dict(t=50))

    st.plotly_chart(fig)
    #=====================================================================================
with tab3:
#payment methods contribute the most to revenue

    Revenue_by_payment_method = filterd_df.groupby('Payment Method')['Total Spent'].sum().sort_values(ascending=False).reset_index()
    fig= px.bar(data_frame= Revenue_by_payment_method,
                x= 'Payment Method',
                y= 'Total Spent',
                title= 'Revenue Contribution by Payment Method',
                color_continuous_scale='Mint',
                color ='Total Spent',
                text_auto=True,
                labels={'Total Spent': 'Total Revenue', 'Payment Method': 'Payment Method'},
                

    )  
    fig.update_traces( textposition='outside')
    st.plotly_chart(fig)

    #==========================================================================
    # payment methods are used most frequently

    payment_usage = (
        filterd_df.groupby('Payment Method')['Transaction ID']
        .nunique()
        .reset_index(name='Transactions')
        .sort_values('Transactions', ascending=False)
    )

    fig= px.bar(data_frame = payment_usage,
                x= 'Transactions',
                y= 'Payment Method',
                title= 'Payment Method Usage',
                color_continuous_scale='Mint',
                                    color ='Transactions',
                text_auto=True,
                    

    )  
    fig.update_traces( textposition='outside')

    fig.update_layout(margin=dict(t=50))
    st.plotly_chart(fig)

with tab4:
#location has the highest revenue

    Total_Spent_by_Location = filterd_df.groupby('Location')['Total Spent'].sum().sort_values(ascending=False).reset_index()
    fig= px.pie(data_frame= Total_Spent_by_Location,
                names= 'Location',
                values= 'Total Spent',
                title= 'Total Revenue by Location',
                color_discrete_sequence=["#097C769B","#175752DA"],
                hole=0.5
    ) 

    st.plotly_chart(fig)
        

