
# 📊 Customer Support SLA & Escalation Analytics

A portfolio-grade data analytics project built using **Python, PostgreSQL 16, Docker Compose, SQL, pytest, and Tableau**.

---

## 🎯 1. Project Overview

Customer support teams must resolve customer issues within agreed Service Level Agreement (SLA) timelines. Delayed resolutions, unresolved tickets, and frequent escalations can reduce customer satisfaction and increase operational costs.

This project analyzes a synthetic dataset of **30,000 customer support tickets** to evaluate SLA compliance, identify unresolved backlogs, monitor escalations, and understand daily ticket volume trends.

### 📌 Business Objectives
* **Measure SLA compliance** across different ticket priorities.
* **Identify critical and high-priority tickets** that miss SLA targets.
* **Monitor unresolved tickets** grouped by priority and status.
* **Identify support categories** with high escalation volumes.
* **Track daily ticket creation trends** over time.
* **Build a repeatable end-to-end pipeline** from raw generation to dashboard-ready datasets.

---

## 🛠️ 2. Technology Stack

| Technology | Purpose |
| :--- | :--- |
| **Python** | Synthetic data generation, validation, and CSV exports |
| **PostgreSQL 16** | Relational storage and analytical SQL queries |
| **Docker Compose** | Local containerized database environment |
| **SQL** | SLA, backlog, escalation, and volume analysis |
| **pytest** | Automated data quality and pipeline testing |
| **Tableau Desktop** | Interactive charts and reporting dashboard |
| **Git & GitHub** | Version control and portfolio publishing |

---

## 🏗️ 3. Architecture

```text
Python Ticket Generator
          │
          ▼
Synthetic Ticket Dataset
          │
          ▼
PostgreSQL Database (Docker Compose)
          │
          ▼
SQL Analytics & Metrics Exporter
          │
          ▼
Dashboard-Ready CSV Files
          │
          ▼
Tableau Worksheets & Support Dashboard
Note: The pipeline runs entirely locally and does not require a paid cloud service.

📋 4. Dataset Overview
The project generated and validated 30,000 synthetic support tickets.

Data Quality Metric	Result
Total tickets	30,000
Unique ticket IDs	30,000
Resolved tickets	16,510
Unresolved tickets	13,490
Escalated tickets	3,455
Priority levels	4
Support categories	6
Automated tests passed	5 / 5
🏷️ Ticket Priorities
P1-Critical: Highest urgency; strict SLAs.

P2-High: High-priority customer issues.

P3-Medium: Standard-priority issues.

P4-Low: Lower-urgency issues.

🚦 Ticket Statuses
Open

In Progress

Resolved

Escalated

🗄️ 5. Database Schema
The primary analytical table is support_tickets. Refer to sql/schema.sql for exact database definitions and data types.

Column	Purpose
ticket_id	Unique ticket identifier
priority	Ticket priority level
status	Current ticket status
category	Support issue category
resolved_at	Resolution timestamp (null for unresolved tickets)
resolution_minutes	Time taken to resolve a ticket
sla_target_minutes	Target resolution time per priority
escalated	Boolean indicating if a ticket was escalated
💡 6. Key Business Questions & Answers
Q1. How many support tickets were generated?
Answer: 30,000 tickets were generated with 30,000 unique ticket IDs, confirming zero duplicates.

Q2. Which priority has the lowest SLA compliance?
Answer: P1-Critical has the lowest observed SLA compliance at 17.99%. Only 817 critical tickets were successfully resolved within target timelines, indicating a major operational bottleneck.

Q3. How does SLA compliance differ by priority?
Priority	Resolved Tickets	SLA Compliance (%)
P1-Critical	817	17.99%
P2-High	3,334	67.19%
P3-Medium	7,463	98.89%
P4-Low	4,896	99.92%
Business Interpretation: SLA compliance improves substantially for lower-priority tickets. Critical and high-priority queues require immediate operational investigation.

Q4. How many tickets remain unresolved?
Answer: 13,490 tickets remain unresolved across Open, In Progress, and Escalated statuses. Backlog analysis helps managers understand workload distribution.

Q5. Which support category has the most escalations?
Category	Escalated Tickets
Hardware	627
Account Access	583
Login	582
Application	565
Payment	552
Network	546
Answer: Hardware has the highest escalation count with 627 tickets.

Q6. How can daily ticket volume help support managers?
The daily ticket volume dataset contains 181 rows. Time-series charts help identify increases and decreases in ticket creation to plan staffing and monitor workload patterns.

📈 7. SLA Calculation
The reported SLA compliance metric is calculated for resolved tickets by priority using the following SQL query:

SQL
SELECT
    priority,
    COUNT(*) AS resolved_tickets,
    ROUND(
        100.0 * COUNT(*) FILTER (
            WHERE resolution_minutes <= sla_target_minutes
        ) / NULLIF(COUNT(*), 0),
        2
    ) AS sla_compliance_pct
FROM support_tickets
WHERE resolved_at IS NOT NULL
GROUP BY priority
ORDER BY priority;
📊 8. Dashboard Visualizations
(Tip: Drag and drop your dashboard screenshots into GitHub's file editor or reference them locally below)

Customer Support SLA & Escalation Dashboard

SLA Compliance by Priority

Backlog by Priority & Status

Escalations by Category

Daily Ticket Volume Trends

📂 9. Project Structure
Plaintext
project_2_support/
├── data/
│   └── support_tickets.csv
├── exports/
│   ├── sla_by_priority.csv
│   ├── backlog_by_priority_status.csv
│   ├── escalations_by_category.csv
│   └── daily_ticket_volume.csv
├── sql/
│   ├── schema.sql
│   └── sla_metrics.sql
├── tests/
│   └── test_log_generator.py
├── log_generator.py
├── load_data.py
├── export_metrics.py
├── docker-compose.yml
├── requirements.txt
├── support_sla_dashboard.twb
├── support_sla_dashboard.twbx
└── README.md
🚀 10. How to Run the Project
Prerequisites
Python 3.13+

Docker Desktop

Git

Tableau Desktop (optional, for viewing .twbx)

Step-by-Step Execution
Start PostgreSQL via Docker:

Bash
docker compose up -d
docker compose ps
Install Python Dependencies:

Bash
python -m pip install -r requirements.txt
Generate Synthetic Dataset:

Bash
python log_generator.py
Load Data into PostgreSQL:

Bash
python load_data.py
Run Automated Tests:

Bash
python -m pytest tests -v
Export Analytical Metrics:

Bash
python export_metrics.py
✅ 11. Testing & Data Quality
Five automated tests passed successfully via pytest:

Expected total ticket count verification.

Unique ticket ID constraints.

Missing resolution values for unresolved tickets.

SLA targets matching ticket priority definitions.

Reproducible synthetic data generation.

🔍 12. Key Findings
Critical Bottleneck: Critical tickets exhibit the lowest reported SLA compliance (17.99%).

High Priority Gaps: High-priority tickets show substantial compliance gaps (67.19%).

Active Backlog: The unresolved backlog contains 13,490 active tickets.

Escalation Driver: Hardware accounts for the largest escalation volume across all categories.

Staffing Visibility: Daily ticket volume tracking provides effective visibility for team resource planning.

🔮 13. Limitations & Future Improvements
Dataset is synthetic rather than real enterprise customer data.

SLA compliance currently evaluates resolved tickets only.

Future extension possibilities include aging analysis for unresolved tickets and percentile resolution tracking.

🏆 14. Skills Demonstrated
Python Data Generation, PostgreSQL, Analytical SQL, Docker Compose, Data Validation, Automated Testing (pytest), CSV Pipeline Design, Tableau Dashboard Development, Git, and GitHub Portfolio Publishing.