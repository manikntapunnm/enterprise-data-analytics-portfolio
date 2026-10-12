-- Enterprise Support Analytics: SLA Performance & Risk Assessment Matrix
SELECT 
    issue_category,
    priority_tier,
    COUNT(ticket_id) as total_tickets_received,
    COUNT(CASE WHEN status IN ('Open', 'Escalated') THEN 1 END) as active_backlog,
    ROUND(AVG(resolution_hours), 2) as avg_hours_to_resolution,
    SUM(sla_violated_flag) as total_sla_breaches,
    ROUND((SUM(sla_violated_flag)::NUMERIC / COUNT(ticket_id)) * 100, 2) as sla_breach_rate_pct
FROM support_operations
GROUP BY issue_category, priority_tier
ORDER BY priority_tier ASC, sla_breach_rate_pct DESC;