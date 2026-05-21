-- Average development and connectedness trajectories by wave.
SELECT
    time,
    AVG(development_score) AS average_development,
    AVG(connectedness_score) AS average_connectedness,
    AVG(current_teacher) AS average_teacher_support,
    AVG(current_peer) AS average_peer_belonging,
    AVG(current_stress) AS average_school_stress
FROM schooling_development_panel
GROUP BY time
ORDER BY time;

-- Intervention group trajectory.
SELECT
    time,
    intervention,
    AVG(development_score) AS average_development,
    AVG(connectedness_score) AS average_connectedness,
    COUNT(*) AS observations
FROM schooling_development_panel
GROUP BY time, intervention
ORDER BY time, intervention;

-- School-support profile summary.
SELECT
    school_support_profile,
    COUNT(DISTINCT student_id) AS students,
    AVG(development_score) AS average_development,
    AVG(connectedness_score) AS average_connectedness,
    AVG(current_teacher) AS average_teacher_support,
    AVG(current_peer) AS average_peer_belonging,
    AVG(current_stress) AS average_school_stress
FROM schooling_development_panel
GROUP BY school_support_profile
ORDER BY average_development DESC;

-- School-level climate and opportunity summary.
SELECT
    school_id,
    COUNT(DISTINCT student_id) AS students,
    AVG(school_climate) AS school_climate,
    AVG(curriculum_opportunity) AS curriculum_opportunity,
    AVG(restorative_practice) AS restorative_practice,
    AVG(resource_capacity) AS resource_capacity,
    AVG(development_score) AS average_development,
    AVG(connectedness_score) AS average_connectedness
FROM schooling_development_panel
GROUP BY school_id
ORDER BY average_connectedness DESC;

-- Final-wave developmental endpoint summary.
WITH final_wave AS (
    SELECT MAX(time) AS max_time FROM schooling_development_panel
)
SELECT
    school_support_profile,
    intervention,
    COUNT(*) AS students,
    AVG(development_score) AS final_average_development,
    AVG(connectedness_score) AS final_average_connectedness
FROM schooling_development_panel p
JOIN final_wave f ON p.time = f.max_time
GROUP BY school_support_profile, intervention
ORDER BY final_average_development DESC;
