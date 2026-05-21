-- Temperament trajectory by profile.
SELECT
    time,
    temperament_profile,
    AVG(adjustment_score) AS average_adjustment,
    AVG(goodness_of_fit) AS average_fit,
    AVG(current_support) AS average_support,
    AVG(acute_stress) AS average_stress,
    AVG(current_accommodation) AS average_accommodation
FROM temperament_individual_differences_panel
GROUP BY time, temperament_profile
ORDER BY time, temperament_profile;

-- Profile summary.
SELECT
    temperament_profile,
    COUNT(DISTINCT child_id) AS children,
    AVG(adjustment_score) AS average_adjustment,
    AVG(goodness_of_fit) AS average_fit,
    AVG(current_support) AS average_support,
    AVG(acute_stress) AS average_stress,
    AVG(temperament_reactivity) AS average_reactivity,
    AVG(current_accommodation) AS average_accommodation
FROM temperament_individual_differences_panel
GROUP BY temperament_profile
ORDER BY average_adjustment DESC;

-- Classroom goodness-of-fit and adjustment.
SELECT
    classroom_id,
    COUNT(DISTINCT child_id) AS children,
    AVG(teacher_responsiveness) AS teacher_responsiveness,
    AVG(movement_flexibility) AS movement_flexibility,
    AVG(goodness_of_fit) AS average_fit,
    AVG(adjustment_score) AS average_adjustment
FROM temperament_individual_differences_panel
GROUP BY classroom_id
ORDER BY average_adjustment DESC;

-- Final-wave endpoint by temperament profile.
WITH final_wave AS (
    SELECT MAX(time) AS max_time FROM temperament_individual_differences_panel
)
SELECT
    temperament_profile,
    COUNT(*) AS children,
    AVG(adjustment_score) AS final_average_adjustment,
    AVG(goodness_of_fit) AS final_average_fit,
    AVG(current_support) AS final_average_support,
    AVG(acute_stress) AS final_average_stress
FROM temperament_individual_differences_panel p
JOIN final_wave f ON p.time = f.max_time
GROUP BY temperament_profile
ORDER BY final_average_adjustment DESC;
