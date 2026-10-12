# Project 2: Customer Support SLA & Ticket Escalation Tracker

## 🧠 Strategic Support Analytics Questions & Solutions

### Question 1: Which engineering modules cause the most critical SLA violations?
*   **The Business Goal:** Pinpoint which issue categories have the highest rate of service level breaches, letting the software dev team fix the underlying software bug.
*   **The SQL Solution:**
    ```sql
    SELECT 
        issue_category,
        COUNT(ticket_id) as critical_incidents,
        SUM(sla_violated_flag) as total_breaches,
        ROUND((SUM(sla_violated_flag)::NUMERIC / COUNT(ticket_id)) * 100, 2) as breach_rate_pct
    FROM support_operations
    WHERE priority_tier IN ('P1-Critical', 'P2-High')
    GROUP BY issue_category
    ORDER BY breach_rate_pct DESC;
    ```

---

## 🏢 Business Context & Operational Architecture
Customer support turnaround speeds dictate customer retention in SaaS and digital platforms. Delays in critical P1 tickets lead to contract cancellations. 

This project processes **30,000 application support incidents** to build an automated tracking engine evaluating resolution efficiency across priority tiers.

```unset
[ Microservice Incident Logs ] ➡️ Extracted via Log Python Handlers
                                        ⬇Lock
[ Data Transformation Engine ] ➡️ Aggregate Operations via SQL Analysis
                                        ⬇
[ Tableau Presentation Canvas] ➡️ Interactive SLA Matrix & Operational Alerts
```
