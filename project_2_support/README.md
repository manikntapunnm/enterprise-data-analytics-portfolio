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