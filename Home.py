import plotly.express as px
import streamlit as st

from styles.theme import apply_theme, CHART_GREENS
from utils.data import build_data_dictionary, load_data
from utils.paths import HOME_IMAGE

# ==================================================================

# Page Configration

st.set_page_config(page_title= 'Retail sales Analysis',
                    layout= 'wide',
                    page_icon = "🛍️",
                    initial_sidebar_state="expanded"
                    )

#================================================

# Shared dashboard styling (see styles/theme.py)

apply_theme(title_color="#172033", subtitle_color="#6B7280", kpi_color="#172338")

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
st.image(str(HOME_IMAGE))


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

df = load_data()
#=================================================================

# Show sample from data
st.subheader('Data Overview')
st.dataframe(df.head())

#====================================================================
# Data Description Table For all columns

st.title("Data Dictionary:")

# Construct dataframe with only Column Name and Description (see utils/data.py)
schema_df = build_data_dictionary(df)

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
                                    color_discrete_sequence=CHART_GREENS))
    

#======================================================================================
