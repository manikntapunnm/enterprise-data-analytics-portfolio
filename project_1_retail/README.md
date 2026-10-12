# Project 1: Enterprise Retail Revenue & Inventory Optimization Matrix

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