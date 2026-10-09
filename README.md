# Retail Store Sales Analysis

## Overview

This project analyzes retail sales performance using a cleaned transactional dataset and presents the results in an interactive Streamlit dashboard. The goal is to help stakeholders understand sales trends, customer purchase behavior, product performance, and operational efficiency through data-driven insights.

The dashboard is designed to support business decisions around pricing, promotions, inventory planning, channel strategy, and customer engagement. It gives a clear view of how products, categories, and payment methods contribute to overall store performance.

## Business Objectives

- Measure store and product sales performance over time
- Identify high-performing categories and items
- Understand customer purchasing patterns
- Evaluate the impact of discounts and promotions
- Compare performance by payment type and sales channel
- Analyze seasonal and weekday/weekend sales behavior
- Support operational and strategic business planning

## Project Structure

- `Home.py` — main dashboard application entry point
- `pages/` — supporting dashboard pages and analytics views
- `retail_store_sales_clean.parquet` — cleaned retail dataset used for analysis
- `requirements.txt` — Python dependencies
- `Retail_Store_Sales_Analysis.ipynb` — exploratory data analysis notebook

## Technologies Used

- Python
- Streamlit
- Pandas
- NumPy
- Plotly
- Parquet data storage

## Dataset Description

The project uses transaction-level retail data that includes both product and sales context attributes. Each row represents a sale event and contains information such as item details, transaction values, payment method, date, discount status, and location.

## Data Dictionary

The retail dataset contains the following key fields:

- Transaction ID
- Customer ID
- Category
- Item
- Price Per Unit
- Quantity
- Total Spent
- Payment Method
- Location
- Transaction Date
- Discount Applied
- Year
- Month
- Day

## Dashboard Features

The dashboard includes analysis for:

- Total sales and revenue trends
- Category contribution analysis
- Product performance comparison
- Payment method preferences
- Sales behavior by date and weekday
- Discount impact insights
- Numerical and categorical exploratory visualizations

## Usage

To run the application locally:

```bash
pip install -r requirements.txt
streamlit run Home.py
```

Once launched, the dashboard can be opened in the default browser and used to explore the retail analytics in an interactive format.

## Conclusion

This project demonstrates how raw retail transaction data can be cleaned, structured, and transformed into actionable business intelligence. By combining a clear analytical schema with interactive visual reporting, it provides a strong foundation for understanding sales performance and supporting smarter decision-making.
