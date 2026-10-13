# 📊 Customer Support SLA & Escalation Analytics

A portfolio-grade data analytics project built using Python, PostgreSQL 16, Docker Compose, SQL, pytest, and Tableau.

---

## 1. Project Overview

Customer support teams must resolve customer issues within agreed Service Level Agreement (SLA) timelines. Delayed resolutions, unresolved tickets, and frequent escalations can reduce customer satisfaction and increase operational costs.

This project analyzes a synthetic dataset of **30,000 customer support tickets** to evaluate SLA compliance, identify unresolved backlogs, monitor escalations, and understand daily ticket volume trends.

### Business Objectives
* **Measure SLA compliance** across different ticket priorities.
* **Identify critical and high-priority tickets** that miss SLA targets.
* **Monitor unresolved tickets** grouped by priority and status.
* **Identify support categories** with high escalation volumes.
* **Track daily ticket creation trends** over time.
* **Build a repeatable end-to-end pipeline** from raw generation to dashboard-ready datasets.

---

## 2. Technology Stack

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

## 3. Architecture

* **Python Ticket Generator** generates the synthetic ticket dataset.
* **PostgreSQL Database** handles relational storage via Docker Compose.
* **SQL Analytics & Metrics Exporter** extracts analytical datasets.
* **Tableau Worksheets & Dashboard** visualize support metrics locally.

> *Note: The pipeline runs entirely locally and does not require a paid cloud service.*

---

## 4. Dataset Overview

The project generated and validated **30,000 synthetic support tickets**.

| Data Quality Metric | Result |
| :--- | :--- |
| Total tickets | 30,000 |
| Unique ticket IDs | 30,000 |
| Resolved tickets | 16,510 |
| Unresolved tickets | 13,490 |
| Escalated tickets | 3,455 |
| Priority levels | 4 |
| Support categories | 6 |
| Automated tests passed | 5 / 5 |

### Ticket Priorities
* **P1-Critical:** Highest urgency; strict SLAs.
* **P2-High:** High-priority customer issues.
* **P3-Medium:** Standard-priority issues.
* **P4-Low:** Lower-urgency issues.

### Ticket Statuses
* `Open`
* `In Progress`
* `Resolved`
* `Escalated`

---

## 5. Database Schema

The primary analytical table is `support_tickets`. Refer to `sql/schema.sql` for exact database definitions and data types.

| Column | Purpose |
| :--- | :--- |
| `ticket_id` | Unique ticket identifier |
| `priority` | Ticket priority level |
| `status` | Current ticket status |
| `category` | Support issue category |
| `resolved_at` | Resolution timestamp (null for unresolved tickets) |
| `resolution_minutes` | Time taken to resolve a ticket |
| `sla_target_minutes` | Target resolution time per priority |
| `escalated` | Boolean indicating if a ticket was escalated |

---

## 6. Key Business Questions & Answers

### Q1. How many support tickets were generated?
* **Answer:** **30,000 tickets** were generated with 30,000 unique ticket IDs, confirming zero duplicates.

### Q2. Which priority has the lowest SLA compliance?
* **Answer:** **P1-Critical** has the lowest observed SLA compliance at **17.99%**. Only 817 critical tickets were successfully resolved within target timelines, indicating a major operational bottleneck.

### Q3. How does SLA compliance differ by priority?
| Priority | Resolved Tickets | SLA Compliance (%) |
| :--- | :--- | :--- |
| **P1-Critical** | 817 | 17.99% |
| **P2-High** | 3,334 | 67.19% |
| **P3-Medium** | 7,463 | 98.89% |
| **P4-Low** | 4,896 | 99.92% |

> *Business Interpretation:* SLA compliance improves substantially for lower-priority tickets. Critical and high-priority queues require immediate operational investigation.

### Q4. How many tickets remain unresolved?
* **Answer:** **13,490 tickets** remain unresolved across Open, In Progress, and Escalated statuses. Backlog analysis helps managers understand workload distribution.

### Q5. Which support category has the most escalations?
| Category | Escalated Tickets |
| :--- | :--- |
| **Hardware** | 627 |
| **Account Access** | 583 |
| **Login** | 582 |
| **Application** | 565 |
| **Payment** | 552 |
| **Network** | 546 |

> *Answer:* **Hardware** has the highest escalation count with **627 tickets**.

### Q6. How can daily ticket volume help support managers?
The daily ticket volume dataset contains 181 rows. Time-series charts help identify increases and decreases in ticket creation to plan staffing and monitor workload patterns.

---

## 7. SLA Calculation

The reported SLA compliance metric is calculated for resolved tickets by priority using the SQL query located in `sql/sla_metrics.sql`. The denominator evaluates resolved tickets only, keeping unresolved backlogs separate.

---

## 8. Dashboard Visualizations

* **Customer Support SLA & Escalation Dashboard:** `![Dashboard Overview](screenshots/dashboard_overview.png)`
* **SLA Compliance by Priority:** `![SLA Compliance](screenshots/sla_compliance.png)`
* **Backlog by Priority & Status:** `![Backlog Analysis](screenshots/backlog_analysis.png)`
* **Escalations by Category:** `![Escalations by Category](screenshots/escalations_category.png)`
* **Daily Ticket Volume Trends:** `![Daily Ticket Volume](screenshots/daily_ticket_volume.png)`

---

## 9. Project Structure

* `data/support_tickets.csv` - Synthetic ticket dataset
* `exports/` - Analytical CSV outputs for Tableau
* `sql/schema.sql` - Database schema definitions
* `sql/sla_metrics.sql` - Analytical queries
* `tests/test_log_generator.py` - Automated tests using pytest
* `log_generator.py` - Python script for data generation
* `load_data.py` - Data loading script
* `export_metrics.py` - Metrics export script
* `docker-compose.yml` - PostgreSQL local container setup
* `support_sla_dashboard.twbx` - Tableau workbook

---

## 10. How to Run the Project

### Prerequisites
* Python 3.13+
* Docker Desktop
* Git
* Tableau Desktop (optional)

### Step-by-Step Execution
1. **Start PostgreSQL via Docker:** Run `docker compose up -d` and verify with `docker compose ps`.
2. **Install Python Dependencies:** Run `python -m pip install -r requirements.txt`.
3. **Generate Synthetic Dataset:** Run `python log_generator.py`.
4. **Load Data into PostgreSQL:** Run `python load_data.py`.
5. **Run Automated Tests:** Run `python -m pytest tests -v`.
6. **Export Analytical Metrics:** Run `python export_metrics.py`.

---

## 11. Testing & Data Quality

Five automated tests passed successfully:
1. Expected total ticket count verification.
2. Unique ticket ID constraints.
3. Missing resolution values for unresolved tickets.
4. SLA targets matching ticket priority definitions.
5. Reproducible synthetic data generation.

---

## 12. Key Findings

* Critical tickets exhibit the lowest reported SLA compliance (17.99%).
* High-priority tickets show substantial compliance gaps.
* The unresolved backlog contains 13,490 active tickets.
* Hardware accounts for the largest escalation volume across all categories.
* Daily ticket volume tracking provides effective visibility for team staffing.

---

## 13. Limitations & Future Improvements

* Dataset is synthetic rather than real enterprise customer data.
* SLA compliance currently evaluates resolved tickets only.
* Future extension possibilities include aging analysis for unresolved tickets and percentile resolution tracking.

---

## 14. Skills Demonstrated

Python Data Generation, PostgreSQL, Analytical SQL, Docker Compose, Data Validation, Automated Testing (`pytest`), CSV Pipeline Design, Tableau Dashboard Development, Git, and GitHub Portfolio Publishing.