-- Average development and embedded exposure trajectories by wave.
SELECT
    time,
    AVG(development_score) AS average_development,
    AVG(embedded_stress) AS average_embedded_stress,
    AVG(embedded_support) AS average_embedded_support,
    AVG(current_care) AS average_care,
    AVG(current_stress) AS average_stress
FROM genes_environment_plasticity_panel
GROUP BY time
ORDER BY time;

-- Early exposure group trajectory.
SELECT
    time,
    early_exposure,
    AVG(development_score) AS average_development,
    AVG(embedded_stress) AS average_embedded_stress,
    AVG(embedded_support) AS average_embedded_support,
    COUNT(*) AS observations
FROM genes_environment_plasticity_panel
GROUP BY time, early_exposure
ORDER BY time, early_exposure;

-- Sensitivity-stress profile summary.
SELECT
    sensitivity_stress_profile,
    COUNT(DISTINCT child_id) AS children,
    AVG(development_score) AS average_development,
    AVG(bio_sensitivity) AS average_bio_sensitivity,
    AVG(current_stress) AS average_stress,
    AVG(current_care) AS average_care,
    AVG(embedded_stress) AS average_embedded_stress,
    AVG(embedded_support) AS average_embedded_support
FROM genes_environment_plasticity_panel
GROUP BY sensitivity_stress_profile
ORDER BY average_development DESC;

-- Context-level support summary.
SELECT
    context_id,
    COUNT(DISTINCT child_id) AS children,
    AVG(school_support) AS school_support,
    AVG(neighborhood_safety) AS neighborhood_safety,
    AVG(service_access) AS service_access,
    AVG(development_score) AS average_development,
    AVG(embedded_support) AS average_embedded_support
FROM genes_environment_plasticity_panel
GROUP BY context_id
ORDER BY average_development DESC;

-- Final-wave developmental endpoint summary.
WITH final_wave AS (
    SELECT MAX(time) AS max_time FROM genes_environment_plasticity_panel
)
SELECT
    sensitivity_stress_profile,
    early_exposure,
    intervention_support,
    COUNT(*) AS children,
    AVG(development_score) AS final_average_development,
    AVG(embedded_stress) AS final_average_embedded_stress,
    AVG(embedded_support) AS final_average_embedded_support
FROM genes_environment_plasticity_panel p
JOIN final_wave f ON p.time = f.max_time
GROUP BY sensitivity_stress_profile, early_exposure, intervention_support
ORDER BY final_average_development DESC;
