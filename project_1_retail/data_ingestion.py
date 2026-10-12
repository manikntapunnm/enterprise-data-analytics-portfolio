import pandas as pd
import duckdb
import random
from datetime import datetime, timedelta
import os

# Ensure we write the database file inside the current project folder
db_path = os.path.join(os.path.dirname(__file__), 'retail_analytics.db')
con = duckdb.connect(db_path)

print("⏳ Initializing enterprise retail database schema...")

# 1. Product Master Dimension Table
products = [
    (101, 'Slim Fit Shirt', 'Apparel', 'Formal Wear', 1200, 550),
    (102, 'Denim Jeans', 'Apparel', 'Casual Wear', 2500, 1100),
    (103, 'Leather Belt', 'Accessories', 'Leather Goods', 800, 320),
    (104, 'Chino Trousers', 'Apparel', 'Casual Wear', 1800, 800),
    (105, 'Running Sneakers', 'Footwear', 'Sports', 3500, 1500),
    (106, 'Formal Shoes', 'Footwear', 'Formal Wear', 4000, 1800),
]
df_products = pd.DataFrame(products, columns=['product_id', 'product_name', 'category', 'sub_category', 'mrp', 'unit_cost'])
con.execute("CREATE OR REPLACE TABLE dim_products AS SELECT * FROM df_products")

# 2. Transactional Sales Fact Table (50,000 Records)
sales_data = []
start_date = datetime(2026, 1, 1)

for i in range(50000):
    tx_id = f"TXN_{100000 + i}"
    date = start_date + timedelta(days=random.randint(0, 280))
    prod = random.choice(products)
    units = random.choices([1, 2, 3, 4, 5], weights=[60, 25, 10, 4, 1])[0]
    discount = random.choices([0.0, 0.1, 0.2, 0.5], weights=[70, 15, 10, 5])[0]
    
    gross_revenue = units * prod[4]
    net_revenue = gross_revenue * (1 - discount)
    total_cost = units * prod[5]
    
    sales_data.append([tx_id, date.strftime('%Y-%m-%d'), prod[0], units, discount, round(net_revenue, 2), round(total_cost, 2)])

df_sales = pd.DataFrame(sales_data, columns=['transaction_id', 'order_date', 'product_id', 'units_sold', 'discount_pct', 'net_revenue', 'total_cost'])
con.execute("CREATE OR REPLACE TABLE fact_sales AS SELECT * FROM df_sales")

# 3. Inventory Status Dimension Table
inventory_data = []
for p in products:
    stock_on_hand = random.randint(50, 500)
    safety_stock = 100
    inventory_data.append([p[0], stock_on_hand, safety_stock])
    
df_inventory = pd.DataFrame(inventory_data, columns=['product_id', 'stock_on_hand', 'safety_stock_level'])
con.execute("CREATE OR REPLACE TABLE dim_inventory AS SELECT * FROM df_inventory")

print(f"✅ Success! Corporate Retail Database created at: {db_path}")
con.close()