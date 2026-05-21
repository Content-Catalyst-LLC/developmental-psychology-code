-- Average lifespan development, gains, losses, and SOC trajectories.
SELECT
    time,
    AVG(development_score) AS average_development,
    AVG(gains) AS average_gains,
    AVG(losses) AS average_losses,
    AVG(soc_index) AS average_soc,
    AVG(current_support) AS average_context_support
FROM lifespan_baltes_panel
GROUP BY time
ORDER BY time;

-- SOC component trajectory.
SELECT
    time,
    AVG(selection) AS average_selection,
    AVG(optimization) AS average_optimization,
    AVG(compensation) AS average_compensation,
    AVG(soc_index) AS average_soc
FROM lifespan_baltes_panel
GROUP BY time
ORDER BY time;

-- Adaptation profile summary.
SELECT
    adaptation_profile,
    COUNT(DISTINCT id) AS people,
    AVG(development_score) AS average_development,
    AVG(gains) AS average_gains,
    AVG(losses) AS average_losses,
    AVG(current_support) AS average_support,
    AVG(soc_index) AS average_soc
FROM lifespan_baltes_panel
GROUP BY adaptation_profile
ORDER BY average_development DESC;

-- Cohort context summary.
SELECT
    cohort_id,
    COUNT(DISTINCT id) AS people,
    AVG(historical_support) AS historical_support,
    AVG(institutional_security) AS institutional_security,
    AVG(development_score) AS average_development,
    AVG(soc_index) AS average_soc
FROM lifespan_baltes_panel
GROUP BY cohort_id
ORDER BY average_development DESC;

-- Final-wave endpoint summary.
WITH final_wave AS (
    SELECT MAX(time) AS max_time FROM lifespan_baltes_panel
)
SELECT
    adaptation_profile,
    cohort_id,
    COUNT(*) AS people,
    AVG(development_score) AS final_average_development,
    AVG(gains) AS final_average_gains,
    AVG(losses) AS final_average_losses,
    AVG(soc_index) AS final_average_soc
FROM lifespan_baltes_panel p
JOIN final_wave f ON p.time = f.max_time
GROUP BY adaptation_profile, cohort_id
ORDER BY final_average_development DESC;
