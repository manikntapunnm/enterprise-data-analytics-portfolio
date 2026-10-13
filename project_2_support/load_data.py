
import os
from pathlib import Path

import psycopg

BASE_DIR = Path(__file__).resolve().parent
CSV_FILE = BASE_DIR / "data" / "support_tickets.csv"
SCHEMA_FILE = BASE_DIR / "sql" / "schema.sql"

DATABASE_URL = (
    "postgresql://support_user:"
    f"{os.getenv('POSTGRES_PASSWORD', 'local_dev_password')}"
    "@localhost:5433/support_analytics"
)

COPY_SQL = """
COPY support_tickets (
    ticket_id, customer_id, created_at, resolved_at,
    priority, status, category, assigned_team,
    first_response_minutes, resolution_minutes,
    sla_target_minutes, escalated
)
FROM STDIN WITH (FORMAT CSV, HEADER TRUE, NULL '')
"""


def main():
    if not CSV_FILE.exists():
        raise FileNotFoundError(
            f"{CSV_FILE} not found. Run log_generator.py first."
        )

    with psycopg.connect(DATABASE_URL) as conn:
        with conn.cursor() as cur:
            cur.execute(SCHEMA_FILE.read_text(encoding="utf-8"))
            cur.execute("TRUNCATE TABLE support_tickets")

            with CSV_FILE.open("rb") as csv_file:
                with cur.copy(COPY_SQL) as copy:
                    while chunk := csv_file.read(1024 * 1024):
                        copy.write(chunk)

        # The connection context commits on success and rolls back
        # if an exception occurs.
    print("Dataset loaded successfully.")

    with psycopg.connect(DATABASE_URL) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT COUNT(*), COUNT(DISTINCT ticket_id)
                FROM support_tickets
            """)
            print("Total tickets, unique IDs:", cur.fetchone())


if __name__ == "__main__":
    main()