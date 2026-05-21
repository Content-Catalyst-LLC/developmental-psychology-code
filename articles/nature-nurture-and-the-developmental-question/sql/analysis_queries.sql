-- Trajectory by structural risk group.
SELECT
    time,
    structural_risk,
    AVG(development_score) AS average_development_score,
    AVG(caregiver_support) AS average_caregiver_support,
    AVG(acute_stress) AS average_acute_stress,
    AVG(protective_context) AS average_protective_context,
    AVG(intervention) AS average_intervention
FROM nature_nurture_development_panel
GROUP BY time, structural_risk
ORDER BY time, structural_risk;

-- Sensitivity profile summary.
SELECT
    sensitivity_profile,
    COUNT(DISTINCT child_id) AS children,
    AVG(development_score) AS average_development_score,
    AVG(biological_sensitivity) AS average_biological_sensitivity,
    AVG(protective_context) AS average_protective_context,
    AVG(acute_stress) AS average_acute_stress,
    AVG(structural_risk) AS average_structural_risk,
    AVG(chronic_adversity) AS average_chronic_adversity
FROM nature_nurture_development_panel
GROUP BY sensitivity_profile
ORDER BY average_development_score DESC;

-- School/institution context summary.
SELECT
    school_id,
    COUNT(DISTINCT child_id) AS children,
    AVG(institutional_support) AS institutional_support,
    AVG(disability_support) AS disability_support,
    AVG(resource_stability) AS resource_stability,
    AVG(development_score) AS average_development_score,
    AVG(protective_context) AS average_protective_context,
    AVG(acute_stress) AS average_acute_stress
FROM nature_nurture_development_panel
GROUP BY school_id
ORDER BY average_development_score DESC;

-- Final-wave endpoint by sensitivity profile.
WITH final_wave AS (
    SELECT MAX(time) AS max_time FROM nature_nurture_development_panel
)
SELECT
    sensitivity_profile,
    structural_risk,
    COUNT(*) AS children,
    AVG(development_score) AS final_average_development_score,
    AVG(protective_context) AS final_average_protective_context,
    AVG(acute_stress) AS final_average_acute_stress
FROM nature_nurture_development_panel p
JOIN final_wave f ON p.time = f.max_time
GROUP BY sensitivity_profile, structural_risk
ORDER BY final_average_development_score DESC;
