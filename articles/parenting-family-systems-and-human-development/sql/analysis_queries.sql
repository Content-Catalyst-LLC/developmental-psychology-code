-- Average development and family support trajectories by wave.
SELECT
    time,
    AVG(development_score) AS average_development,
    AVG(family_support_index) AS average_family_support,
    AVG(current_parenting) AS average_parenting,
    AVG(current_family) AS average_family_climate,
    AVG(current_stress) AS average_stress
FROM family_systems_panel
GROUP BY time
ORDER BY time;

-- Caregiver-support group trajectory.
SELECT
    time,
    caregiver_support,
    AVG(development_score) AS average_development,
    AVG(family_support_index) AS average_family_support,
    COUNT(*) AS observations
FROM family_systems_panel
GROUP BY time, caregiver_support
ORDER BY time, caregiver_support;

-- Family-support profile summary.
SELECT
    family_support_profile,
    COUNT(DISTINCT child_id) AS children,
    AVG(development_score) AS average_development,
    AVG(family_support_index) AS average_family_support,
    AVG(current_parenting) AS average_parenting,
    AVG(current_family) AS average_family_climate,
    AVG(current_stress) AS average_stress
FROM family_systems_panel
GROUP BY family_support_profile
ORDER BY average_development DESC;

-- Household-level support summary.
SELECT
    household_id,
    COUNT(DISTINCT child_id) AS children,
    AVG(household_stability) AS household_stability,
    AVG(kin_support) AS kin_support,
    AVG(economic_security) AS economic_security,
    AVG(development_score) AS average_development,
    AVG(family_support_index) AS average_family_support
FROM family_systems_panel
GROUP BY household_id
ORDER BY average_family_support DESC;

-- Final-wave developmental endpoint summary.
WITH final_wave AS (
    SELECT MAX(time) AS max_time FROM family_systems_panel
)
SELECT
    family_support_profile,
    caregiver_support,
    COUNT(*) AS children,
    AVG(development_score) AS final_average_development,
    AVG(family_support_index) AS final_average_family_support
FROM family_systems_panel p
JOIN final_wave f ON p.time = f.max_time
GROUP BY family_support_profile, caregiver_support
ORDER BY final_average_development DESC;
