-- Adult adjustment trajectory by life stage.
SELECT
    time,
    life_stage,
    AVG(adjustment_score) AS average_adjustment,
    AVG(current_relational_support) AS average_support,
    AVG(current_work_integration) AS average_work,
    AVG(current_health_burden) AS average_health_burden,
    AVG(current_role_burden) AS average_role_burden
FROM adult_development_life_stages_panel
GROUP BY time, life_stage
ORDER BY time, life_stage;

-- Adult development profile summary.
SELECT
    adult_development_profile,
    COUNT(DISTINCT id) AS adults,
    AVG(adjustment_score) AS average_adjustment,
    AVG(current_relational_support) AS average_support,
    AVG(current_work_integration) AS average_work,
    AVG(current_health_burden) AS average_health_burden,
    AVG(current_adaptive_resources) AS average_adaptive_resources,
    AVG(current_role_burden) AS average_role_burden
FROM adult_development_life_stages_panel
GROUP BY adult_development_profile
ORDER BY average_adjustment DESC;

-- Context support summary.
SELECT
    context_id,
    COUNT(DISTINCT id) AS adults,
    AVG(institutional_support) AS institutional_support,
    AVG(community_stability) AS community_stability,
    AVG(adjustment_score) AS average_adjustment,
    AVG(current_role_burden) AS average_role_burden
FROM adult_development_life_stages_panel
GROUP BY context_id
ORDER BY average_adjustment DESC;

-- Final-wave adult adjustment endpoint summary.
WITH final_wave AS (
    SELECT MAX(time) AS max_time FROM adult_development_life_stages_panel
)
SELECT
    life_stage,
    adult_development_profile,
    COUNT(*) AS adults,
    AVG(adjustment_score) AS final_average_adjustment,
    AVG(current_relational_support) AS final_average_support,
    AVG(current_health_burden) AS final_average_health_burden,
    AVG(current_role_burden) AS final_average_role_burden
FROM adult_development_life_stages_panel p
JOIN final_wave f ON p.time = f.max_time
GROUP BY life_stage, adult_development_profile
ORDER BY final_average_adjustment DESC;
