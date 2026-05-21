-- Average development and ecological support trajectories by wave.
SELECT
    time,
    AVG(development_score) AS average_development,
    AVG(ecological_support) AS average_ecological_support,
    AVG(ecological_stress) AS average_ecological_stress,
    AVG(current_family) AS average_family_support,
    AVG(current_peer) AS average_peer_belonging
FROM developmental_systems_panel
GROUP BY time
ORDER BY time;

-- Intervention trajectory.
SELECT
    time,
    intervention_exposure,
    AVG(development_score) AS average_development,
    AVG(ecological_support) AS average_ecological_support,
    AVG(ecological_stress) AS average_ecological_stress,
    COUNT(*) AS observations
FROM developmental_systems_panel
GROUP BY time, intervention_exposure
ORDER BY time, intervention_exposure;

-- Ecological-support profile summary.
SELECT
    ecological_support_profile,
    COUNT(DISTINCT child_id) AS children,
    AVG(development_score) AS average_development,
    AVG(ecological_support) AS average_ecological_support,
    AVG(ecological_stress) AS average_ecological_stress,
    AVG(current_family) AS average_family_support,
    AVG(current_peer) AS average_peer_belonging
FROM developmental_systems_panel
GROUP BY ecological_support_profile
ORDER BY average_development DESC;

-- School-level developmental ecology.
SELECT
    school_id,
    COUNT(DISTINCT child_id) AS children,
    AVG(school_climate) AS school_climate,
    AVG(curriculum_opportunity) AS curriculum_opportunity,
    AVG(development_score) AS average_development,
    AVG(ecological_support) AS average_ecological_support
FROM developmental_systems_panel
GROUP BY school_id
ORDER BY average_development DESC;

-- Neighborhood-level developmental ecology.
SELECT
    neighborhood_id,
    COUNT(DISTINCT child_id) AS children,
    AVG(neighborhood_safety) AS neighborhood_safety,
    AVG(service_access) AS service_access,
    AVG(material_security) AS material_security,
    AVG(development_score) AS average_development,
    AVG(ecological_stress) AS average_ecological_stress
FROM developmental_systems_panel
GROUP BY neighborhood_id
ORDER BY average_development DESC;

-- Final-wave endpoint summary.
WITH final_wave AS (
    SELECT MAX(time) AS max_time FROM developmental_systems_panel
)
SELECT
    ecological_support_profile,
    intervention_exposure,
    COUNT(*) AS children,
    AVG(development_score) AS final_average_development,
    AVG(ecological_support) AS final_average_ecological_support,
    AVG(ecological_stress) AS final_average_ecological_stress
FROM developmental_systems_panel p
JOIN final_wave f ON p.time = f.max_time
GROUP BY ecological_support_profile, intervention_exposure
ORDER BY final_average_development DESC;
