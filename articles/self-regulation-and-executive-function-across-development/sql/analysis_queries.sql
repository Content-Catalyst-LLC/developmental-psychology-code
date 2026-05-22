-- Regulation trajectory by chronic stress group.
SELECT
    time,
    chronic_stress,
    AVG(regulation_score) AS average_regulation,
    AVG(regulatory_support_context) AS average_regulatory_support_context,
    AVG(current_support) AS average_support,
    AVG(current_structure) AS average_structure,
    AVG(current_sleep) AS average_sleep,
    AVG(acute_stress) AS average_stress,
    AVG(intervention_exposure) AS intervention_rate
FROM regulation_development_panel
GROUP BY time, chronic_stress
ORDER BY time, chronic_stress;

-- Regulation profile summary.
SELECT
    regulation_profile,
    COUNT(DISTINCT child_id) AS children,
    AVG(regulation_score) AS average_regulation,
    AVG(regulatory_support_context) AS average_regulatory_support_context,
    AVG(acute_stress) AS average_stress,
    AVG(current_sleep) AS average_sleep,
    AVG(intervention_exposure) AS intervention_rate,
    AVG(chronic_stress) AS chronic_stress_rate,
    AVG(disability_support_need) AS disability_support_need_rate
FROM regulation_development_panel
GROUP BY regulation_profile
ORDER BY average_regulation DESC;

-- School regulation context summary.
SELECT
    school_id,
    COUNT(DISTINCT child_id) AS children,
    AVG(school_climate) AS school_climate,
    AVG(regulation_scaffolding) AS regulation_scaffolding,
    AVG(disability_accommodation) AS disability_accommodation,
    AVG(transition_predictability) AS transition_predictability,
    AVG(regulation_score) AS average_regulation,
    AVG(regulatory_support_context) AS average_regulatory_support_context,
    AVG(acute_stress) AS average_stress
FROM regulation_development_panel
GROUP BY school_id
ORDER BY average_regulation DESC;

-- Final-wave endpoint by profile.
WITH final_wave AS (
    SELECT MAX(time) AS max_time FROM regulation_development_panel
)
SELECT
    regulation_profile,
    chronic_stress,
    COUNT(*) AS observations,
    AVG(regulation_score) AS final_average_regulation,
    AVG(regulatory_support_context) AS final_average_regulatory_context,
    AVG(current_sleep) AS final_average_sleep,
    AVG(acute_stress) AS final_average_stress
FROM regulation_development_panel p
JOIN final_wave f ON p.time = f.max_time
GROUP BY regulation_profile, chronic_stress
ORDER BY final_average_regulation DESC;
