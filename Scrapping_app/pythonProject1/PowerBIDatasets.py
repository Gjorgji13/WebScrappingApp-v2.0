import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Dataset 1: Sales Data (Basic)
sales_data_basic = pd.DataFrame({
    'Date': pd.date_range(start='2023-01-01', periods=100, freq='D'),
    'Product': np.random.choice(['Product A', 'Product B', 'Product C'], size=100),
    'Quantity': np.random.randint(1, 20, size=100),
    'Sales Amount': np.random.randint(50, 500, size=100),
    'Cost': np.random.randint(30, 400, size=100)
})

# Dataset 2: Customer Feedback Data
customer_feedback = pd.DataFrame({
    'Customer ID': np.arange(1, 51),
    'Feedback': np.random.choice(['Good', 'Average', 'Bad'], size=50),
    'Rating': np.random.randint(1, 6, size=50),
    'Date': pd.date_range(start='2023-01-01', periods=50, freq='W')
})

# Dataset 3: Product Table
product_table = pd.DataFrame({
    'Product ID': np.arange(1, 11),
    'Product Name': [f'Product {chr(i)}' for i in range(65, 75)],
    'Category': np.random.choice(['Electronics', 'Clothing', 'Groceries'], size=10),
    'Price': np.random.randint(100, 1000, size=10)
})

# Dataset 4: Region Sales Data
region_sales = pd.DataFrame({
    'Region': ['North', 'South', 'East', 'West'],
    'Sales Amount': np.random.randint(1000, 10000, size=4),
    'Target': np.random.randint(5000, 15000, size=4)
})

# Dataset 5: Survey Data
survey_data = pd.DataFrame({
    'Respondent ID': np.arange(1, 21),
    'Q1 Response': np.random.choice(['Yes', 'No'], size=20),
    'Q2 Response': np.random.choice(['Yes', 'No'], size=20),
    'Q3 Response': np.random.choice(['Yes', 'No'], size=20)
})

# Dataset 6: Time Series Sales Data
date_range = pd.date_range(start='2020-01-01', end='2023-12-31', freq='ME')
time_series_sales = pd.DataFrame({
    'Date': date_range,
    'Product': np.random.choice(['Product A', 'Product B', 'Product C'], size=len(date_range)),
    'Sales Amount': np.random.randint(1000, 10000, size=len(date_range)),
    'Cost': np.random.randint(500, 8000, size=len(date_range))
})

# Dataset 7: Employee Performance Data
employee_performance = pd.DataFrame({
    'Employee ID': np.arange(1, 21),
    'Name': [f'Employee {i}' for i in range(1, 21)],
    'Department': np.random.choice(['HR', 'IT', 'Sales', 'Finance'], size=20),
    'Performance Rating': np.random.randint(1, 10, size=20),
    'Manager ID': np.random.randint(1, 5, size=20)
})

# Dataset 8: Financial Data
financial_data = pd.DataFrame({
    'Account': np.random.choice(['Account A', 'Account B', 'Account C'], size=100),
    'Date': pd.date_range(start='2023-01-01', periods=100, freq='D'),
    'Debit': np.random.randint(100, 1000, size=100),
    'Credit': np.random.randint(100, 1000, size=100),
    'Balance': np.random.randint(1000, 10000, size=100)
})

# Dataset 9: Customer Churn Data
customer_churn = pd.DataFrame({
    'Customer ID': np.arange(1, 101),
    'Tenure': np.random.randint(1, 72, size=100),
    'Monthly Charges': np.random.uniform(50, 100, size=100).round(2),
    'Total Charges': np.random.uniform(500, 7000, size=100).round(2),
    'Churn': np.random.choice(['Yes', 'No'], size=100)
})

# Dataset 10: IoT Data Stream
start_time = datetime.now()
time_stamps = [start_time + timedelta(seconds=x) for x in range(100)]
iot_data_stream = pd.DataFrame({
    'Timestamp': time_stamps,
    'Device ID': np.random.choice(['Device A', 'Device B', 'Device C'], size=100),
    'Sensor Reading': np.random.uniform(20.0, 80.0, size=100).round(2),
    'Location': np.random.choice(['Factory A', 'Factory B'], size=100)
})

# Save all datasets as CSV files
datasets = {
    "sales_data_basic.csv": sales_data_basic,
    "customer_feedback.csv": customer_feedback,
    "product_table.csv": product_table,
    "region_sales.csv": region_sales,
    "survey_data.csv": survey_data,
    "time_series_sales.csv": time_series_sales,
    "employee_performance.csv": employee_performance,
    "financial_data.csv": financial_data,
    "customer_churn.csv": customer_churn,
    "iot_data_stream.csv": iot_data_stream
}

for filename, df in datasets.items():
    df.to_csv(f"D:/PowerBI Datasetovi za vezhbanje/PowerBIdatasetovi{filename}", index=False)

# Output the paths to the saved CSV files
list(datasets.keys())
