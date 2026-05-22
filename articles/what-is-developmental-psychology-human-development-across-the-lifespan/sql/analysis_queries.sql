-- Trajectory by structural risk group.
SELECT
    time,
    structural_risk,
    AVG(development_score) AS average_development,
    AVG(current_support) AS average_support,
    AVG(acute_stress) AS average_stress,
    AVG(protective_context) AS average_protective_context,
    AVG(intervention) AS intervention_rate
FROM developmental_lifespan_panel
GROUP BY time, structural_risk
ORDER BY time, structural_risk;

-- Development profile summary.
SELECT
    development_profile,
    COUNT(DISTINCT child_id) AS children,
    AVG(development_score) AS average_development,
    AVG(protective_context) AS average_protective_context,
    AVG(current_support) AS average_support,
    AVG(acute_stress) AS average_stress,
    AVG(structural_risk) AS structural_risk_rate,
    AVG(disability_support_need) AS disability_support_need_rate
FROM developmental_lifespan_panel
GROUP BY development_profile
ORDER BY average_development DESC;

-- School/context summary.
SELECT
    school_id,
    COUNT(DISTINCT child_id) AS children,
    AVG(school_climate) AS school_climate,
    AVG(disability_accommodation) AS disability_accommodation,
    AVG(counseling_access) AS counseling_access,
    AVG(language_access) AS language_access,
    AVG(community_resource_index) AS community_resource_index,
    AVG(development_score) AS average_development,
    AVG(protective_context) AS average_protective_context,
    AVG(acute_stress) AS average_stress
FROM developmental_lifespan_panel
GROUP BY school_id
ORDER BY average_development DESC;

-- Final-wave endpoint by profile.
WITH final_wave AS (
    SELECT MAX(time) AS max_time FROM developmental_lifespan_panel
)
SELECT
    development_profile,
    structural_risk,
    COUNT(*) AS observations,
    AVG(development_score) AS final_average_development,
    AVG(protective_context) AS final_average_protective_context,
    AVG(current_support) AS final_average_support,
    AVG(acute_stress) AS final_average_stress
FROM developmental_lifespan_panel p
JOIN final_wave f ON p.time = f.max_time
GROUP BY development_profile, structural_risk
ORDER BY final_average_development DESC;
