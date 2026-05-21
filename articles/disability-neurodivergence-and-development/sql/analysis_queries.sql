-- Average development and participation trajectories by wave.
SELECT
    time,
    AVG(development_score) AS average_development,
    AVG(participation_score) AS average_participation,
    AVG(current_support) AS average_support,
    AVG(current_access) AS average_access,
    AVG(current_barrier) AS average_barrier
FROM disability_neurodivergence_panel
GROUP BY time
ORDER BY time;

-- Access-barrier condition summary.
SELECT
    access_condition,
    COUNT(DISTINCT child_id) AS children,
    AVG(development_score) AS average_development,
    AVG(participation_score) AS average_participation,
    AVG(current_access) AS average_access,
    AVG(current_barrier) AS average_barrier,
    AVG(current_support) AS average_support
FROM disability_neurodivergence_panel
GROUP BY access_condition
ORDER BY average_development DESC;

-- Setting-level inclusion and service summary.
SELECT
    setting_id,
    COUNT(DISTINCT child_id) AS children,
    AVG(inclusion_climate) AS inclusion_climate,
    AVG(service_access) AS service_access,
    AVG(sensory_flexibility) AS sensory_flexibility,
    AVG(development_score) AS average_development,
    AVG(participation_score) AS average_participation
FROM disability_neurodivergence_panel
GROUP BY setting_id
ORDER BY average_participation DESC;

-- Barrier exposure endpoint summary.
WITH final_wave AS (
    SELECT MAX(time) AS max_time FROM disability_neurodivergence_panel
)
SELECT
    access_condition,
    COUNT(*) AS children,
    AVG(development_score) AS final_average_development,
    AVG(participation_score) AS final_average_participation
FROM disability_neurodivergence_panel p
JOIN final_wave f ON p.time = f.max_time
GROUP BY access_condition
ORDER BY final_average_development DESC;
