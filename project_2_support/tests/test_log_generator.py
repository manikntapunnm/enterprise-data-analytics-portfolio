from datetime import datetime, timezone

from log_generator import generate_tickets, validate_tickets


def test_generates_expected_number_of_tickets():
    tickets = generate_tickets(
        count=100,
        now=datetime(2026, 10, 13, tzinfo=timezone.utc),
    )
    assert len(tickets) == 100


def test_ticket_ids_are_unique():
    tickets = generate_tickets(
        count=100,
        now=datetime(2026, 10, 13, tzinfo=timezone.utc),
    )
    assert len({t["ticket_id"] for t in tickets}) == 100


def test_unresolved_tickets_have_no_resolution():
    tickets = generate_tickets(
        count=100,
        now=datetime(2026, 10, 13, tzinfo=timezone.utc),
    )
    for ticket in tickets:
        if ticket["resolved_at"] == "":
            assert ticket["resolution_minutes"] == ""


def test_sla_targets_match_priority():
    tickets = generate_tickets(
        count=100,
        now=datetime(2026, 10, 13, tzinfo=timezone.utc),
    )
    validate_tickets(tickets)
    targets = {
        "P1-Critical": 60,
        "P2-High": 240,
        "P3-Medium": 1440,
        "P4-Low": 2880,
    }
    for ticket in tickets:
        assert ticket["sla_target_minutes"] == targets[ticket["priority"]]


def test_generation_is_reproducible():
    fixed_now = datetime(2026, 10, 13, tzinfo=timezone.utc)
    first = generate_tickets(20, seed=42, now=fixed_now)
    second = generate_tickets(20, seed=42, now=fixed_now)
    assert first == second

