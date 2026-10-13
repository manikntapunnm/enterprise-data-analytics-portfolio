import os
from pathlib import Path

import psycopg
import csv

BASE_DIR = Path(__file__).resolve().parent
EXPORT_DIR = BASE_DIR / "exports"
EXPORT_DIR.mkdir(exist_ok=True)

DATABASE_URL = (
    "postgresql://support_user:"
    f"{os.getenv('POSTGRES_PASSWORD', 'local_dev_password')}"
    "@localhost:5433/support_analytics"
)

QUERIES = {
    "sla_by_priority": """
        SELECT
            priority,
            COUNT(*) AS resolved_tickets,
            COUNT(*) FILTER (
                WHERE resolution_minutes <= sla_target_minutes
            ) AS tickets_within_sla,
            COUNT(*) FILTER (
                WHERE resolution_minutes > sla_target_minutes
            ) AS breached_tickets,
            ROUND(
                100.0 * COUNT(*) FILTER (
                    WHERE resolution_minutes <= sla_target_minutes
                ) / NULLIF(COUNT(*), 0),
                2
            ) AS sla_compliance_pct,
            ROUND(AVG(resolution_minutes), 2)
                AS avg_resolution_minutes
        FROM support_tickets
        WHERE resolved_at IS NOT NULL
        GROUP BY priority
        ORDER BY CASE priority
            WHEN 'P1-Critical' THEN 1
            WHEN 'P2-High' THEN 2
            WHEN 'P3-Medium' THEN 3
            WHEN 'P4-Low' THEN 4
        END
    """,
    "backlog_by_priority_status": """
        SELECT
            priority,
            status,
            COUNT(*) AS backlog_count,
            ROUND(
                AVG(EXTRACT(EPOCH FROM (
                    CURRENT_TIMESTAMP - created_at
                )) / 60)::numeric,
                2
            ) AS avg_age_minutes
        FROM support_tickets
        WHERE resolved_at IS NULL
        GROUP BY priority, status
        ORDER BY priority, status
    """,
    "escalations_by_category": """
        SELECT
            category,
            COUNT(*) AS total_tickets,
            COUNT(*) FILTER (
                WHERE escalated
            ) AS escalated_tickets,
            ROUND(
                100.0 * COUNT(*) FILTER (
                    WHERE escalated
                ) / NULLIF(COUNT(*), 0),
                2
            ) AS escalation_rate_pct
        FROM support_tickets
        GROUP BY category
        ORDER BY escalation_rate_pct DESC
    """,
    "daily_ticket_volume": """
        SELECT
            created_at::date AS ticket_date,
            COUNT(*) AS tickets_created,
            COUNT(*) FILTER (
                WHERE resolved_at IS NOT NULL
            ) AS resolved_tickets_from_cohort,
            COUNT(*) FILTER (
                WHERE resolved_at IS NOT NULL
                  AND resolution_minutes > sla_target_minutes
            ) AS breached_tickets_from_cohort
        FROM support_tickets
        GROUP BY created_at::date
        ORDER BY ticket_date
    """,
}


def main():
    with psycopg.connect(DATABASE_URL) as conn:
        for name, query in QUERIES.items():
            with conn.cursor() as cur:
                cur.execute(query)
                columns = [desc.name for desc in cur.description]
                rows = cur.fetchall()

            output_file = EXPORT_DIR / f"{name}.csv"

            with output_file.open(
                "w", newline="", encoding="utf-8"
            ) as file:
                writer = csv.writer(file)
                writer.writerow(columns)
                writer.writerows(rows)

            print(f"Exported {len(rows)} rows: {output_file.name}")


if __name__ == "__main__":
    main()