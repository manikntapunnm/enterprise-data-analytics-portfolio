"""Generate reproducible synthetic customer support tickets."""

from __future__ import annotations

import csv
import random
from datetime import datetime, timedelta, timezone
from pathlib import Path

SEED = 42
TICKET_COUNT = 30_000

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
OUTPUT_FILE = DATA_DIR / "support_tickets.csv"

SLA_TARGETS = {
    "P1-Critical": 60,
    "P2-High": 240,
    "P3-Medium": 1_440,
    "P4-Low": 2_880,
}

PRIORITIES = list(SLA_TARGETS)
PRIORITY_WEIGHTS = [5, 20, 45, 30]

CATEGORIES = [
    "Login",
    "Payment",
    "Network",
    "Application",
    "Hardware",
    "Account Access",
]

TEAMS = [
    "Technical Support",
    "Payments",
    "Infrastructure",
    "Application Support",
]

STATUSES = ["Open", "In Progress", "Escalated", "Resolved"]
STATUS_WEIGHTS = [12, 23, 10, 55]

FIELDS = [
    "ticket_id",
    "customer_id",
    "created_at",
    "resolved_at",
    "priority",
    "status",
    "category",
    "assigned_team",
    "first_response_minutes",
    "resolution_minutes",
    "sla_target_minutes",
    "escalated",
]


def generate_tickets(
    count: int = TICKET_COUNT,
    seed: int = SEED,
    now: datetime | None = None,
) -> list[dict]:
    """Generate tickets using a fixed seed and reporting cutoff."""

    if count < 1:
        raise ValueError("count must be greater than zero")

    rng = random.Random(seed)
    now = now or datetime.now(timezone.utc)

    if now.tzinfo is None:
        raise ValueError("now must be timezone-aware")

    now = now.astimezone(timezone.utc)
    start = now - timedelta(days=180)
    total_minutes = int((now - start).total_seconds() // 60)

    tickets = []

    for i in range(1, count + 1):
        created_at = start + timedelta(
            minutes=rng.randint(0, total_minutes)
        )

        priority = rng.choices(
            PRIORITIES, weights=PRIORITY_WEIGHTS, k=1
        )[0]

        status = rng.choices(
            STATUSES, weights=STATUS_WEIGHTS, k=1
        )[0]

        first_response_minutes = rng.randint(1, 180)

        # A log-normal distribution produces mostly shorter
        # resolutions with a smaller number of long-running cases.
        resolution_minutes = max(
            1, int(rng.lognormvariate(5.0, 1.0))
        )

        proposed_resolution = created_at + timedelta(
            minutes=resolution_minutes
        )

        is_resolved = (
            status == "Resolved" and proposed_resolution <= now
        )

        if status == "Resolved" and not is_resolved:
            status = "In Progress"

        resolved_at = proposed_resolution if is_resolved else None
        actual_resolution = resolution_minutes if is_resolved else None

        escalated = (
            status == "Escalated"
            or (
                priority == "P1-Critical"
                and rng.random() < 0.35
            )
        )

        tickets.append({
            "ticket_id": f"TKT-{i:06d}",
            "customer_id": f"CUST-{rng.randint(1, 8000):05d}",
            "created_at": created_at.isoformat(),
            "resolved_at": (
                resolved_at.isoformat() if resolved_at else ""
            ),
            "priority": priority,
            "status": status,
            "category": rng.choice(CATEGORIES),
            "assigned_team": rng.choice(TEAMS),
            "first_response_minutes": first_response_minutes,
            "resolution_minutes": (
                actual_resolution if actual_resolution is not None else ""
            ),
            "sla_target_minutes": SLA_TARGETS[priority],
            "escalated": str(escalated).lower(),
        })

    return tickets


def validate_tickets(tickets: list[dict]) -> None:
    """Fail fast if generated records violate core data contracts."""

    ids = set()

    for ticket in tickets:
        ticket_id = ticket["ticket_id"]

        if ticket_id in ids:
            raise ValueError(f"Duplicate ticket ID: {ticket_id}")
        ids.add(ticket_id)

        if ticket["priority"] not in SLA_TARGETS:
            raise ValueError(f"Invalid priority: {ticket['priority']}")

        created = datetime.fromisoformat(ticket["created_at"])
        if created.tzinfo is None:
            raise ValueError(f"Naive creation timestamp: {ticket_id}")

        resolved_text = ticket["resolved_at"]

        if resolved_text:
            resolved = datetime.fromisoformat(resolved_text)

            if resolved < created:
                raise ValueError(
                    f"Resolution precedes creation: {ticket_id}"
                )

            if not ticket["resolution_minutes"]:
                raise ValueError(
                    f"Missing duration for resolved ticket: {ticket_id}"
                )
        elif ticket["resolution_minutes"] != "":
            raise ValueError(
                f"Unresolved ticket has resolution duration: {ticket_id}"
            )

        if ticket["sla_target_minutes"] != SLA_TARGETS[ticket["priority"]]:
            raise ValueError(f"Incorrect SLA target: {ticket_id}")


def main() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    tickets = generate_tickets()
    validate_tickets(tickets)

    with OUTPUT_FILE.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(tickets)

    resolved_count = sum(bool(t["resolved_at"]) for t in tickets)
    escalated_count = sum(t["escalated"] == "true" for t in tickets)

    print(f"Generated: {len(tickets):,} tickets")
    print(f"Unique IDs: {len({t['ticket_id'] for t in tickets}):,}")
    print(f"Resolved: {resolved_count:,}")
    print(f"Unresolved: {len(tickets) - resolved_count:,}")
    print(f"Escalated: {escalated_count:,}")
    print(f"Validated CSV: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()