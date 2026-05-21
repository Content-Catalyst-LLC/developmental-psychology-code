-- Analytical queries for developmental psychology synthetic panel data.

-- Average developmental score by wave.
SELECT
    time,
    AVG(development_score) AS average_development_score,
    AVG(current_support) AS average_support,
    AVG(current_risk) AS average_risk,
    AVG(policy_access) AS average_policy_access
FROM developmental_panel
GROUP BY time
ORDER BY time;

-- Context-level developmental outcomes.
SELECT
    context_id,
    COUNT(DISTINCT person_id) AS people,
    AVG(institutional_climate) AS institutional_climate,
    AVG(resource_level) AS resource_level,
    AVG(development_score) AS average_development_score
FROM developmental_panel
GROUP BY context_id
ORDER BY average_development_score DESC;

-- Risk/support contrast.
SELECT
    CASE
        WHEN current_support >= 0 AND current_risk < 0 THEN 'higher_support_lower_risk'
        WHEN current_support >= 0 AND current_risk >= 0 THEN 'higher_support_higher_risk'
        WHEN current_support < 0 AND current_risk < 0 THEN 'lower_support_lower_risk'
        ELSE 'lower_support_higher_risk'
    END AS developmental_condition_group,
    COUNT(*) AS observations,
    AVG(development_score) AS average_development_score
FROM developmental_panel
GROUP BY developmental_condition_group
ORDER BY average_development_score DESC;
