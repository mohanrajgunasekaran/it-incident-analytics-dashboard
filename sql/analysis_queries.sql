-- Load data/incidents.csv into a SQLite table named incidents first.
SELECT priority, COUNT(*) AS incident_count FROM incidents GROUP BY priority
ORDER BY CASE priority WHEN 'P1' THEN 1 WHEN 'P2' THEN 2 WHEN 'P3' THEN 3 ELSE 4 END;

SELECT priority, ROUND(AVG((julianday(resolved_at)-julianday(created_at))*24),2) AS mttr_hours
FROM incidents WHERE status='Resolved' AND resolved_at IS NOT NULL AND resolved_at<>'' GROUP BY priority;

WITH r AS (SELECT service, sla_target_hours, (julianday(resolved_at)-julianday(created_at))*24 AS hours
FROM incidents WHERE status='Resolved' AND resolved_at IS NOT NULL AND resolved_at<>'')
SELECT service, COUNT(*) AS resolved_count,
SUM(CASE WHEN hours>sla_target_hours THEN 1 ELSE 0 END) AS breaches,
ROUND(100.0*SUM(CASE WHEN hours>sla_target_hours THEN 1 ELSE 0 END)/COUNT(*),2) AS breach_rate_pct
FROM r GROUP BY service ORDER BY breach_rate_pct DESC;

SELECT root_cause, COUNT(*) AS incident_count FROM incidents GROUP BY root_cause ORDER BY incident_count DESC;
