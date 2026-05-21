-- Average pathway trajectories by wave.
SELECT
    time,
    AVG(adaptation_score) AS average_adaptation,
    AVG(internalizing_score) AS average_internalizing,
    AVG(externalizing_score) AS average_externalizing,
    AVG(current_risk) AS average_risk,
    AVG(current_support) AS average_support,
    AVG(cumulative_risk) AS average_cumulative_risk
FROM developmental_psychopathology_panel
GROUP BY time
ORDER BY time;

-- Risk-support profile summary.
SELECT
    risk_support_profile,
    COUNT(DISTINCT child_id) AS children,
    AVG(adaptation_score) AS average_adaptation,
    AVG(internalizing_score) AS average_internalizing,
    AVG(externalizing_score) AS average_externalizing,
    AVG(current_risk) AS average_risk,
    AVG(current_support) AS average_support
FROM developmental_psychopathology_panel
GROUP BY risk_support_profile
ORDER BY average_adaptation DESC;

-- Context support summary.
SELECT
    context_id,
    COUNT(DISTINCT child_id) AS children,
    AVG(community_support) AS community_support,
    AVG(school_belonging) AS school_belonging,
    AVG(service_access) AS service_access,
    AVG(adaptation_score) AS average_adaptation
FROM developmental_psychopathology_panel
GROUP BY context_id
ORDER BY average_adaptation DESC;

-- Multifinality endpoint summary.
WITH final_wave AS (
    SELECT MAX(time) AS max_time FROM developmental_psychopathology_panel
)
SELECT
    risk_support_profile,
    CASE
        WHEN internalizing_score >= externalizing_score THEN 'internalizing_dominant'
        ELSE 'externalizing_dominant'
    END AS dominant_pathway,
    COUNT(*) AS children,
    AVG(adaptation_score) AS average_adaptation
FROM developmental_psychopathology_panel p
JOIN final_wave f ON p.time = f.max_time
GROUP BY risk_support_profile, dominant_pathway
ORDER BY risk_support_profile, dominant_pathway;
