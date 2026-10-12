-- Month-over-Month Revenue Growth and Gross Margin Analysis
WITH monthly_sales AS (
    SELECT 
        DATE_TRUNC('month', CAST(order_date AS DATE)) as sales_month,
        SUM(net_revenue) as current_month_revenue,
        SUM(total_cost) as current_month_cost
    FROM fact_sales
    GROUP BY 1
),
mom_metrics AS (
    SELECT 
        sales_month,
        current_month_revenue,
        LAG(current_month_revenue) OVER (ORDER BY sales_month) as previous_month_revenue,
        (current_month_revenue - current_month_cost) / current_month_revenue * 100 as gross_margin_pct
    FROM monthly_sales
)
SELECT 
    sales_month,
    ROUND(current_month_revenue, 2) as net_revenue,
    ROUND(((current_month_revenue - previous_month_revenue) / previous_month_revenue) * 100, 2) as mom_growth_pct,
    ROUND(gross_margin_pct, 2) as gross_margin_pct
FROM mom_metrics;