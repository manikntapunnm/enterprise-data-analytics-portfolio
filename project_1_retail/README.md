# Project 1: Enterprise Retail Revenue & Inventory Optimization Matrix

## 🧠 Strategic Business Questions & Multi-Tool Solutions

### Question 1: Which products are at high risk of a "Stockout" (Inventory Deficit)?
*   **The Business Goal:** Identify products where the current inventory (`stock_on_hand`) has fallen below the company's mandated `safety_stock_level`. This allows store managers to reorder stock before losing sales.
*   **The SQL Solution:**
    ```sql
    SELECT 
        p.product_name,
        p.category,
        i.stock_on_hand,
        i.safety_stock_level,
        (i.safety_stock_level - i.stock_on_hand) as units_deficit
    FROM dim_inventory i
    JOIN dim_products p ON i.product_id = p.product_id
    WHERE i.stock_on_hand < i.safety_stock_level
    ORDER BY units_deficit DESC;
    ```
*   **The Power BI (DAX) Solution:** Create a calculated column or measure to flag the risk level:
    ```dax
    Stock Status = 
    IF(
        SUM(dim_inventory[stock_on_hand]) < SUM(dim_inventory[safety_stock_level]),
        "⚠️ High Reorder Risk",
        "✅ Stock Healthy"
    )
    ```
    *Visual Implementation:* Put this into a **Table Visual** and apply Conditional Formatting to highlight rows labeled "High Reorder Risk" in light red.

---

### Question 2: What is the exact financial impact of promotional discounts on our profit margins?
*   **The Business Goal:** Determine if aggressive discounting (e.g., 10% or 20% off) is destroying product profitability or driving enough volume to make up for it.
*   **The SQL Solution:**
    ```sql
    SELECT 
        f.discount_pct * 100 as discount_tier_pct,
        COUNT(f.transaction_id) as total_orders,
        ROUND(SUM(f.net_revenue), 2) as total_net_revenue,
        ROUND((SUM(f.net_revenue) - SUM(f.total_cost)) / SUM(f.net_revenue) * 100, 2) as realized_profit_margin_pct
    FROM fact_sales f
    GROUP BY 1
    ORDER BY 1 ASC;
    ```
*   **The Power BI (DAX) Solution:** Create two explicit measures to track margin degradation:
    ```dax
    Total Net Revenue = SUM(fact_sales[net_revenue])
    ```
    ```dax
    Gross Margin % = 
    DIVIDE(
        SUM(fact_sales[net_revenue]) - SUM(fact_sales[total_cost]), 
        SUM(fact_sales[net_revenue]), 
        0
    )
    ```
    *Visual Implementation:* Create a **Scatter Plot** with `discount_pct` on the X-axis, `Gross Margin %` on the Y-axis, and `Product Name` as the details. This shows at a glance which products become unprofitable when discounted.

---

### Question 3: Who are our top-performing product categories by absolute profit (not just revenue)?
*   **The Business Goal:** Sometimes a category brings in massive revenue but has very tight profit margins due to manufacturing costs. Executives need to know where the real profit is generated.
*   **The SQL Solution:**
    ```sql
    SELECT 
        p.category,
        ROUND(SUM(f.net_revenue), 2) as total_revenue,
        ROUND(SUM(f.net_revenue) - SUM(f.total_cost), 2) as absolute_profit,
        ROUND((SUM(f.net_revenue) - SUM(f.total_cost)) / SUM(f.net_revenue) * 100, 2) as category_margin_pct
    FROM fact_sales f
    JOIN dim_products p ON f.product_id = p.product_id
    GROUP BY p.category
    ORDER BY absolute_profit DESC;
    ```
*   **The Power BI (DAX) Solution:** Create a measure for total profit:
    ```dax
    Absolute Profit = [Total Net Revenue] - SUM(fact_sales[total_cost])
    ```
    *Visual Implementation:* Use a **Donut Chart** representing `Absolute Profit` by Category next to a **Clustered Bar Chart** showing `Total Net Revenue` by Category to illustrate the structural differences between revenue scale and actual profit.

---

### Question 4: How do we track our running cumulative (YTD) revenue performance?
*   **The Business Goal:** Corporate leadership tracks cumulative Year-to-Date (YTD) charts to check if the business is on track to hit annual financial targets compared to previous months.
*   **The SQL Solution:**
    ```sql
    WITH monthly_totals AS (
        SELECT 
            DATE_TRUNC('month', CAST(order_date AS DATE)) as sales_month,
            SUM(net_revenue) as monthly_revenue
        FROM fact_sales
        GROUP BY 1
    )
    SELECT 
        sales_month,
        ROUND(monthly_revenue, 2) as revenue_this_month,
        ROUND(SUM(monthly_revenue) OVER (ORDER BY sales_month), 2) as cumulative_ytd_revenue
    FROM monthly_totals
    ORDER BY sales_month;
    ```
*   **The Power BI (DAX) Solution:** Ensure your `fact_sales[order_date]` is marked as a date data type, then write a time-intelligence measure:
    ```dax
    YTD Cumulative Revenue = TOTALYTD([Total Net Revenue], 'fact_sales'[order_date])
    ```
    *Visual Implementation:* Display this measure using an **Area Chart** with `order_date` on the X-axis. The smooth, upward-sloping visualization lets executives track total business scaling smoothly over time.

---

## 🏢 Business Context & Core Problem
In major retail operations (like Amazon, Flipkart, or reliance networks), overstocking ties up critical working capital, while stockouts lead directly to revenue leakage and customer frustration. 

This project builds a localized **Medallion Data Architecture** using **DuckDB OLAP technology** to ingest 50,000 transaction records. It optimizes inventory turns, monitors gross margins, and protects profitability from excessive promotional discount patterns.

---

## ⚙️ Data Pipeline Architecture
The system runs entirely free of cost on local architecture utilizing a structured relational design:

```unset
[ Raw Transaction Sources ] ➡️ Ingested via Pandas DataFrames
                                      ⬇️
[ DuckDB Analytical Storage ] ➡️ Normalized into Fact & Dimension Tables
                                      ⬇️
[ Enterprise SQL Logic ]      ➡️ Executed via CTEs & Window Functions (LAG)
                                      ⬇️
[ Production CSV Sinks ]      ➡️ Clean data models exported for BI Layers
```

### Relational Schema Blueprint
*   `fact_sales`: `transaction_id` (PK), `order_date`, `product_id` (FK), `units_sold`, `discount_pct`, `net_revenue`, `total_cost`.
*   `dim_products`: `product_id` (PK), `product_name`, `category`, `sub_category`, `mrp`, `unit_cost`.
*   `dim_inventory`: `product_id` (PK/FK), `stock_on_hand`, `safety_stock_level`.

---

## 📊 Analytical Insights & System Discoveries

By executing advanced window functions across the 50,000 transaction baseline, the following high-level performance patterns were identified:

### 1. Month-over-Month (MoM) Revenue Trajectory
*   **The Trend:** Sales data exhibits structural stabilization following initial normalization phases.
*   **The Risk:** Specific promotional periods show high transaction counts but compressed net margins due to aggressive compounding discount structures (up to 20%).

### 2. Profitability Leakage Analysis
*   **The Discovery:** The **Apparel** category (specifically *Slim Fit Shirts* and *Denim Jeans*) generates the highest raw transaction volumes but suffers from inconsistent product margins due to arbitrary markdown actions.
*   **The Optimization:** Implementing an automated ceiling of **15% on promotional discounts** preserves gross margins above a target **45% threshold** without sacrificing volume.

---

## 🎨 Visualization Layer Requirements (Power BI / Tableau)

To turn these data models into operational business insights, construct a single-page executive dashboard using the following three strategic components:

### 1. High-Level Executive Status Cards
*   **Net Revenue Container:** A card displaying total accumulated company revenue.
*   **Gross Margin Gauge:** A visual tracking overall profitability against a fixed **45% operational benchmark**.
*   **Discount Leakage Metric:** An indicator highlighting average revenue lost to active store markdowns.

### 2. Growth & Margin Line-Column Chart
*   **X-Axis:** `sales_month` (Chronological order).
*   **Column Values (Primary Y-Axis):** Total `net_revenue` per month to show baseline scale.
*   **Line Values (Secondary Y-Axis):** `mom_growth_pct` to highlight sudden acceleration or deceleration spikes.

### 3. Category Breakdown Decomposition Tree
*   **Root Element:** Total Global Revenue.
*   **Branches:** `category` ➡️ `sub_category` ➡️ `product_name`.
*   **Tooltips Embedded:** `stock_on_hand` vs. `safety_stock_level`.
*   **Executive Purpose:** Allows category leads to instantly identify which exact styles are over-stocked or sitting below safe operational inventory thresholds.

---

## 🎨 Enterprise Dashboard Interactive Storyboard

Below is the live operational walkthrough of the analytical engine, proving how business users leverage cross-filtering matrices to audit revenue leakage, target category margin changes, and track supply pipeline risk profiles:

### 1. Global Executive System Baseline
*Tracks total corporate revenue intake and average gross profit bounds across all segments simultaneously.*
![1. Global System Baseline]
<img width="1188" height="697" alt="global_overview" src="https://github.com/user-attachments/assets/785cf369-fc9d-48c6-bb30-4d5208e688d0" />



### 2. Segment Drill-Down: Transaction Isolation (Denim Jeans)
*Isolates individual product groupings to track performance stability under target sales volume conditions.*
![2. Denim Jeans Isolation]
<img width="1189" height="685" alt="filter_denim_jeans" src="https://github.com/user-attachments/assets/1dbae174-6b96-475a-9b8d-5f8168e0f1d9" />

### 3. Core Margin Density Maximization (Leather Belt)
*Pinpoints peak margin categories yielding top efficiency benchmarks to direct active pricing optimization.*
![3. Leather Belt Performance]

<img width="1185" height="678" alt="filter_leather_belt" src="https://github.com/user-attachments/assets/8870c12c-229c-4958-af12-37bd6a39dcb5" />


### 4. Revenue/Margin Variance Matrix (Chino Trousers)
*Balances volume allocations against corresponding margin margins to evaluate category commercial health.*
![4. Chino Trousers Audit]

<img width="1189" height="688" alt="ilter_chino_trousers" src="https://github.com/user-attachments/assets/d5147f5a-7823-4159-9dbd-eb53627d8a6f" />


### 5. Tactical Review Vector (Formal Shoes)
*Aggregates inventory tracking parameters across premium categories to verify regional warehouse flow logs.*
![5. Formal Shoes Analysis]<img width="1194" height="692" alt="filter_slim_fit_shirt" src="https://github.com/user-attachments/assets/a3ae68a9-0ff5-4c72-b1c3-4b8d365c00b7" />


<img width="1190" height="693" alt="filter_formal_shoes" src="https://github.com/user-attachments/assets/dab1b4c7-244b-476b-bf3d-c5f0ae553030" />


### 6. Discount Degradation Matrix (Slim Fit Shirt)
*Exposes margin shrinkage down to 51.22% caused by loose, non-automated promotional markdown strategies.*
![6. Slim Fit Shirt Variance]

<img width="1194" height="692" alt="filter_slim_fit_shirt" src="https://github.com/user-attachments/assets/443112a6-d30f-4896-b48d-d974fca949a1" />


### 7. Logistics Footprint Profiling (Running Sneakers)
*Maintains active monitoring loops over incoming active inventory stocks to balance distribution speeds.*
![7. Running Sneakers Check]

<img width="1193" height="690" alt="filter_running_sneakers" src="https://github.com/user-attachments/assets/05d77d04-916a-4c23-8cd8-947b6fb4aae6" />


### 8. Automated Supply Exception Alert Grid
*The system-wide exception engine shading low-stock profiles in red where volumes drop beneath the 200-unit safe threshold.*
![8. Active Stockout Warnings]
<img width="1177" height="652" alt="active_stockout_alerts" src="https://github.com/user-attachments/assets/b8f17f64-8c61-4f2b-9c40-645716adcb57" />



### 9. Production DAX Semantic Measure Implementation
*Validates the implementation of custom explicit analytics calculators running natively inside the Power BI memory pool.*
![9. DAX Implementation Layer]

<img width="757" height="195" alt="dax_measures" src="https://github.com/user-attachments/assets/8e880b2b-ac81-4d69-afa7-dbaff59b021e" />


### 10. Relational Star-Schema Relationship Model Map
*Displays the normalized data mapping architecture connecting transactional facts directly to independent dimension lookup nodes.*
![10. Relational Schema Data Model](10_relationship_model.png)

<img width="1064" height="643" alt="relationship_model" src="https://github.com/user-attachments/assets/ddd85189-ec68-45a0-a136-4031734d04ce" />

