# Customer Support SLA & Escalation Analytics

A portfolio-grade data analytics project built using Python, PostgreSQL 16, Docker Compose, SQL, pytest, and Tableau.

---

## 1. Project Overview

Customer support teams must resolve customer issues within agreed Service Level Agreement (SLA) timelines. Delayed resolutions, unresolved tickets, and frequent escalations can reduce customer satisfaction and increase operational costs.

This project analyzes a synthetic dataset of **30,000 customer support tickets** to evaluate SLA compliance, identify unresolved backlogs, monitor escalations, and understand daily ticket volume trends.

### Business Objectives
* Measure SLA compliance across different ticket priorities.
* Identify critical and high-priority tickets that miss SLA targets.
* Monitor unresolved tickets grouped by priority and status.
* Identify support categories with high escalation volumes.
* Track daily ticket creation trends over time.
* Build a repeatable end-to-end analytics pipeline from raw data generation to dashboard-ready datasets.

---

## 2. Technology Stack

| Technology | Purpose |
| :--- | :--- |
| **Python** | Synthetic data generation, validation, and CSV exports |
| **PostgreSQL 16** | Relational storage and analytical SQL queries |
| **Docker Compose** | Local database environment |
| **SQL** | SLA, backlog, escalation, and volume analysis |
| **pytest** | Automated testing |
| **Tableau Desktop** | Interactive charts and reporting dashboard |
| **Git and GitHub** | Version control and portfolio publishing |

---

## 3. Architecture

```text
Python Ticket Generator
          |
          v
Synthetic Ticket Dataset
          |
          v
PostgreSQL Database (Docker Compose)
          |
          v
SQL Analytics
          |
          v
Python Metrics Exporter
          |
          v
Dashboard-Ready CSV Files
          |
          v
Tableau Worksheets
          |
          v
Support Analytics Dashboard
Note: The pipeline runs locally and does not require a paid cloud service.4. Dataset OverviewThe project generated and validated 30,000 synthetic support tickets.Data Quality MetricResultTotal tickets30,000Unique ticket IDs30,000Resolved tickets16,510Unresolved tickets13,490Escalated tickets3,455Priority levels4Support categories6Automated tests passed5 / 5Ticket PrioritiesP1-Critical: Highest urgency.P2-High: High-priority customer issues.P3-Medium: Standard-priority issues.P4-Low: Lower-urgency issues.Ticket StatusesOpenIn ProgressResolvedEscalated5. Database SchemaThe primary analytical table is support_tickets. Refer to sql/schema.sql for the exact database definitions and data types.ColumnPurposeticket_idUnique ticket identifierpriorityTicket prioritystatusCurrent ticket statuscategorySupport issue categoryresolved_atResolution timestamp; null for unresolved ticketsresolution_minutesTime taken to resolve a ticketsla_target_minutesTarget resolution timeescalatedIndicates whether a ticket was escalated(Note: The daily volume export also contains ticket_date, tickets_created, resolved_tickets_from_cohort, and breached_tickets_from_cohort.)6. Key Business Questions and AnswersQ1. How many support tickets were generated?Answer: 30,000 tickets were generated, with 30,000 unique ticket IDs. This confirms that the dataset contains no duplicate ticket identifiers according to the validation performed.Q2. Which priority has the lowest SLA compliance?Answer: P1-Critical has the lowest observed SLA compliance at 17.99%. Only 817 critical tickets were resolved, and the reported compliance rate indicates a significant service-level concern. Critical-ticket workflows should be investigated first.Q3. How does SLA compliance differ by priority?PriorityResolved TicketsSLA ComplianceP1-Critical81717.99%P2-High3,33467.19%P3-Medium7,46398.89%P4-Low4,89699.92%Business interpretation: SLA compliance improves substantially for lower-priority tickets in this dataset. The critical and high-priority queues require investigation.Q4. How many tickets remain unresolved?Answer: 13,490 tickets remain unresolved. These tickets include Open, In Progress, and Escalated statuses. Backlog analysis helps managers understand workload distribution and identify areas requiring additional attention.Q5. Which support category has the most escalations?CategoryEscalated TicketsHardware627Account Access583Login582Application565Payment552Network546Answer: Hardware has the highest escalation count, with 627 tickets. Support leaders could investigate recurring hardware issues, troubleshooting procedures, and opportunities to improve first-contact resolution.Q6. How can daily ticket volume help support managers?The daily ticket volume dataset contains 181 rows. A time-series chart helps identify increases and decreases in ticket creation. Managers can use this information to plan staffing, monitor workload patterns, and investigate unusual spikes.7. SLA CalculationThe reported SLA compliance metric is calculated for resolved tickets by priority:SQLSELECT
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
The denominator contains resolved tickets only. Unresolved tickets are analyzed separately as backlog and should not be interpreted as completed SLA successes.8. Dashboard ScreenshotsCustomer Support SLA and Escalation Dashboard OverviewSLA Compliance by PriorityBacklog by Priority and StatusEscalations by CategoryDaily Ticket Volume9. Project StructurePlaintextproject_2_support/
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
10. How to Run the ProjectPrerequisitesPython 3.13 or a compatible Python version.Docker Desktop.Git.Tableau Desktop for opening and exploring the workbook.Step 1: Start PostgreSQLFrom the project directory:Bashdocker compose up -d
docker compose ps
(Wait until the PostgreSQL container reports a healthy status.)Step 2: Install Python DependenciesBashpython -m pip install -r requirements.txt
Step 3: Generate the Synthetic DatasetBashpython log_generator.py
Step 4: Load Data into PostgreSQLBashpython load_data.py
Step 5: Run Automated TestsBashpython -m pytest tests -v
(The recorded test run completed with five passing tests.)Step 6: Export Analytical MetricsBashpython export_metrics.py
(This generates four CSV files in the exports/ directory for use in Tableau.)Step 7: Explore the Tableau dashboardOpen support_sla_dashboard.twbx in Tableau Desktop.11. Testing and Data QualityFive automated tests passed:Expected ticket count.Unique ticket IDs.Missing resolution values for unresolved tickets.SLA targets matching ticket priority.Reproducible data generation.Additional database checks confirmed 30,000 records and 30,000 unique ticket IDs.12. Key FindingsCritical tickets have the lowest reported SLA compliance.High-priority tickets also show substantial SLA compliance gaps.The unresolved backlog contains 13,490 tickets.Hardware has the largest escalation count among the six categories.Daily ticket volume can help support teams plan workload and staffing.13. Limitations and Future ImprovementsThe dataset is synthetic rather than real customer data.SLA compliance currently evaluates resolved tickets only.The project could be extended with aging analysis for unresolved tickets.Additional metrics could include median resolution time, percentile resolution times, and SLA breach counts.Tableau filters could be added for priority, category, and date.Future versions could introduce scheduled data refreshes and automated data-quality monitoring.14. Skills DemonstratedPython data generation, PostgreSQL, analytical SQL, Docker Compose, data validation, automated testing, CSV pipeline design, Tableau dashboard development, Git, and GitHub documentation.