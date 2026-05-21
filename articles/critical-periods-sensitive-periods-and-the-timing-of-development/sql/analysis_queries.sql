-- Analytical queries for synthetic critical-period and sensitive-period data.

-- Average timing weights by developmental time.
SELECT
    time,
    AVG(critical_weight) AS critical_weight,
    AVG(early_sensitive_weight) AS early_sensitive_weight,
    AVG(adolescent_sensitive_weight) AS adolescent_sensitive_weight,
    AVG(residual_plasticity_weight) AS residual_plasticity_weight
FROM developmental_timing_panel
GROUP BY time
ORDER BY time;

-- Average outcomes by developmental time.
SELECT
    time,
    AVG(critical_outcome) AS average_critical_outcome,
    AVG(sensitive_outcome) AS average_sensitive_outcome,
    AVG(multi_window_outcome) AS average_multi_window_outcome,
    AVG(recovery_outcome) AS average_recovery_outcome
FROM developmental_timing_panel
GROUP BY time
ORDER BY time;

-- High-exposure comparison within the critical window.
SELECT
    CASE
        WHEN experience >= 0 THEN 'higher_experience'
        ELSE 'lower_experience'
    END AS experience_group,
    COUNT(*) AS observations,
    AVG(critical_outcome) AS average_critical_outcome,
    AVG(sensitive_outcome) AS average_sensitive_outcome
FROM developmental_timing_panel
WHERE critical_weight = 1
GROUP BY experience_group;

-- Later intervention and residual plasticity.
SELECT
    CASE
        WHEN late_intervention >= 0.5 THEN 'higher_late_intervention'
        ELSE 'lower_late_intervention'
    END AS late_intervention_group,
    COUNT(*) AS observations,
    AVG(recovery_outcome) AS average_recovery_outcome
FROM developmental_timing_panel
WHERE time >= 9
GROUP BY late_intervention_group;
