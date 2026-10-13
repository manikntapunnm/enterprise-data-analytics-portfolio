CREATE TABLE IF NOT EXISTS support_tickets (
    ticket_id VARCHAR(20) PRIMARY KEY,
    customer_id VARCHAR(20) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL,
    resolved_at TIMESTAMPTZ,
    priority VARCHAR(20) NOT NULL CHECK (
        priority IN ('P1-Critical', 'P2-High', 'P3-Medium', 'P4-Low')
    ),
    status VARCHAR(20) NOT NULL CHECK (
        status IN ('Open', 'In Progress', 'Escalated', 'Resolved')
    ),
    category VARCHAR(40) NOT NULL,
    assigned_team VARCHAR(50) NOT NULL,
    first_response_minutes INTEGER NOT NULL CHECK (
        first_response_minutes > 0
    ),
    resolution_minutes INTEGER CHECK (
        resolution_minutes > 0
    ),
    sla_target_minutes INTEGER NOT NULL CHECK (
        sla_target_minutes > 0
    ),
    escalated BOOLEAN NOT NULL,

    CHECK (
        (resolved_at IS NULL AND resolution_minutes IS NULL)
        OR
        (resolved_at IS NOT NULL AND resolution_minutes IS NOT NULL)
    ),
    CHECK (
        resolved_at IS NULL OR resolved_at >= created_at
    ),
    CHECK (
        (priority = 'P1-Critical' AND sla_target_minutes = 60)
        OR (priority = 'P2-High' AND sla_target_minutes = 240)
        OR (priority = 'P3-Medium' AND sla_target_minutes = 1440)
        OR (priority = 'P4-Low' AND sla_target_minutes = 2880)
    )
);

CREATE INDEX IF NOT EXISTS idx_support_created_at
    ON support_tickets (created_at);

CREATE INDEX IF NOT EXISTS idx_support_priority_status
    ON support_tickets (priority, status);

CREATE INDEX IF NOT EXISTS idx_support_customer
    ON support_tickets (customer_id);