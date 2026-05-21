-- Average adjustment, functional fit, support, health burden, and adaptation trajectories.
SELECT
    time,
    AVG(adjustment_score) AS average_adjustment,
    AVG(functional_fit) AS average_functional_fit,
    AVG(current_function) AS average_function,
    AVG(current_support) AS average_support,
    AVG(current_health) AS average_health_burden,
    AVG(current_adaptation) AS average_adaptation,
    AVG(current_meaning) AS average_meaning
FROM aging_adaptation_later_life_panel
GROUP BY time
ORDER BY time;

-- Adaptation-profile summary.
SELECT
    adaptation_profile,
    COUNT(DISTINCT id) AS older_adults,
    AVG(adjustment_score) AS average_adjustment,
    AVG(functional_fit) AS average_functional_fit,
    AVG(current_support) AS average_support,
    AVG(current_health) AS average_health_burden,
    AVG(current_adaptation) AS average_adaptation
FROM aging_adaptation_later_life_panel
GROUP BY adaptation_profile
ORDER BY average_adjustment DESC;

-- Care-context accessibility and dignity.
SELECT
    care_context_id,
    COUNT(DISTINCT id) AS older_adults,
    AVG(environmental_accessibility) AS environmental_accessibility,
    AVG(dignity_support) AS dignity_support,
    AVG(service_access) AS service_access,
    AVG(adjustment_score) AS average_adjustment,
    AVG(functional_fit) AS average_functional_fit
FROM aging_adaptation_later_life_panel
GROUP BY care_context_id
ORDER BY average_adjustment DESC;

-- Final-wave later-life adjustment endpoint summary.
WITH final_wave AS (
    SELECT MAX(time) AS max_time FROM aging_adaptation_later_life_panel
)
SELECT
    adaptation_profile,
    COUNT(*) AS older_adults,
    AVG(adjustment_score) AS final_average_adjustment,
    AVG(functional_fit) AS final_average_functional_fit,
    AVG(current_health) AS final_average_health_burden,
    AVG(current_support) AS final_average_support
FROM aging_adaptation_later_life_panel p
JOIN final_wave f ON p.time = f.max_time
GROUP BY adaptation_profile
ORDER BY final_average_adjustment DESC;
