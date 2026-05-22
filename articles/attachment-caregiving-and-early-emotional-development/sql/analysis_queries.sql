-- Emotional regulation trajectory by chronic stress group.
SELECT
    time,
    chronic_stress,
    AVG(regulation_score) AS average_regulation,
    AVG(current_care) AS average_care,
    AVG(current_repair) AS average_repair,
    AVG(current_caregiver_support) AS average_caregiver_support,
    AVG(current_stress) AS average_stress,
    AVG(caregiving_support_context) AS average_caregiving_support_context
FROM attachment_development_panel
GROUP BY time, chronic_stress
ORDER BY time, chronic_stress;

-- Attachment-development profile summary.
SELECT
    attachment_profile,
    COUNT(DISTINCT child_id) AS children,
    AVG(regulation_score) AS average_regulation,
    AVG(caregiving_support_context) AS average_caregiving_support_context,
    AVG(current_care) AS average_care,
    AVG(current_repair) AS average_repair,
    AVG(current_stress) AS average_stress,
    AVG(chronic_stress) AS chronic_stress_rate,
    AVG(disability_support_need) AS disability_support_need_rate
FROM attachment_development_panel
GROUP BY attachment_profile
ORDER BY average_regulation DESC;

-- Context-level caregiving ecology summary.
SELECT
    context_id,
    COUNT(DISTINCT child_id) AS children,
    AVG(childcare_continuity) AS childcare_continuity,
    AVG(neighborhood_safety) AS neighborhood_safety,
    AVG(family_service_access) AS family_service_access,
    AVG(caregiving_ecology_support) AS caregiving_ecology_support,
    AVG(regulation_score) AS average_regulation,
    AVG(current_stress) AS average_stress,
    AVG(caregiving_support_context) AS average_caregiving_support_context
FROM attachment_development_panel
GROUP BY context_id
ORDER BY average_regulation DESC;

-- Final-wave endpoint by profile.
WITH final_wave AS (
    SELECT MAX(time) AS max_time FROM attachment_development_panel
)
SELECT
    attachment_profile,
    chronic_stress,
    COUNT(*) AS observations,
    AVG(regulation_score) AS final_average_regulation,
    AVG(caregiving_support_context) AS final_average_caregiving_support_context,
    AVG(current_care) AS final_average_care,
    AVG(current_repair) AS final_average_repair,
    AVG(current_stress) AS final_average_stress
FROM attachment_development_panel p
JOIN final_wave f ON p.time = f.max_time
GROUP BY attachment_profile, chronic_stress
ORDER BY final_average_regulation DESC;
