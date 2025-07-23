# 1 Convert CSV Files to SQLite Database
import pandas as pd
import sqlite3

# Load CSV files 
ad_sales = pd.read_csv("AdSales.csv")
total_sales = pd.read_csv("TotalSales.csv")
eligibility = pd.read_csv("Eligibility.csv")

# Create SQLite database
conn = sqlite3.connect("ecommerce.db")

# Save DataFrames to SQL tables
ad_sales.to_sql("ad_sales", conn, if_exists="replace", index=False)
total_sales.to_sql("total_sales", conn, if_exists="replace", index=False)
eligibility.to_sql("eligibility", conn, if_exists="replace", index=False)

print("All 3 tables successfully loaded into ecommerce.db")
conn.close()
