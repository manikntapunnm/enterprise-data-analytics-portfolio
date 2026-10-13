============================================================
-- Project 2: Customer Support SLA & Escalation Tracker
-- Database: PostgreSQL
-- ============================================================

-- 1. Resolution SLA performance by priority
-- Denominator: resolved tickets only.

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
        AS avg_resolution_minutes,

    PERCENTILE_CONT(0.5) WITHIN GROUP (
        ORDER BY resolution_minutes
    ) AS median_resolution_minutes

FROM support_tickets
WHERE resolved_at IS NOT NULL
GROUP BY priority
ORDER BY CASE priority
    WHEN 'P1-Critical' THEN 1
    WHEN 'P2-High' THEN 2
    WHEN 'P3-Medium' THEN 3
    WHEN 'P4-Low' THEN 4
END;


-- 2. Current unresolved backlog by priority
-- An aging threshold is not automatically a confirmed SLA breach.

SELECT
    priority,
    status,
    COUNT(*) AS backlog_count,

    ROUND(
        AVG(
            EXTRACT(
                EPOCH FROM (
                    CURRENT_TIMESTAMP - created_at
                )
            ) / 60
        ),
        2
    ) AS avg_age_minutes,

    COUNT(*) FILTER (
        WHERE CURRENT_TIMESTAMP >
              created_at
              + sla_target_minutes * INTERVAL '1 minute'
    ) AS tickets_older_than_sla_target

FROM support_tickets
WHERE resolved_at IS NULL
GROUP BY priority, status
ORDER BY CASE priority
    WHEN 'P1-Critical' THEN 1
    WHEN 'P2-High' THEN 2
    WHEN 'P3-Medium' THEN 3
    WHEN 'P4-Low' THEN 4
END, status;


-- 3. Escalation analysis by issue category

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
ORDER BY escalation_rate_pct DESC;


-- 4. Daily ticket volume and resolved SLA breaches

SELECT
    created_at::date AS ticket_date,
    COUNT(*) AS tickets_created,

    COUNT(*) FILTER (
        WHERE resolved_at IS NOT NULL
    ) AS tickets_resolved_from_cohort,

    COUNT(*) FILTER (
        WHERE resolved_at IS NOT NULL
          AND resolution_minutes > sla_target_minutes
    ) AS breached_tickets_from_cohort

FROM support_tickets
GROUP BY created_at::date
ORDER BY ticket_date;

-- 5. Escalation rates by category

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
ORDER BY escalation_rate_pct DESC, category;