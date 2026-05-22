-- Social-self trajectory by chronic exclusion group.
SELECT
    time,
    chronic_exclusion,
    AVG(social_self_score) AS average_social_self,
    AVG(social_support_context) AS average_social_support_context,
    AVG(current_exclusion) AS average_exclusion,
    AVG(bullying_exposure) AS average_bullying,
    AVG(digital_comparison_stress) AS average_digital_comparison
FROM social_development_panel
GROUP BY time, chronic_exclusion
ORDER BY time, chronic_exclusion;

-- Social profile summary.
SELECT
    social_profile,
    COUNT(DISTINCT child_id) AS children,
    AVG(social_self_score) AS average_social_self,
    AVG(social_support_context) AS average_social_support_context,
    AVG(current_exclusion) AS average_exclusion,
    AVG(bullying_exposure) AS average_bullying,
    AVG(digital_comparison_stress) AS average_digital_comparison,
    AVG(chronic_exclusion) AS chronic_exclusion_rate
FROM social_development_panel
GROUP BY social_profile
ORDER BY average_social_self DESC;

-- School social context summary.
SELECT
    school_id,
    COUNT(DISTINCT child_id) AS children,
    AVG(school_connectedness) AS school_connectedness,
    AVG(teacher_support) AS teacher_support,
    AVG(anti_bullying_climate) AS anti_bullying_climate,
    AVG(inclusion_climate) AS inclusion_climate,
    AVG(restorative_practice_access) AS restorative_practice_access,
    AVG(social_self_score) AS average_social_self,
    AVG(social_support_context) AS average_social_support_context,
    AVG(current_exclusion) AS average_exclusion,
    AVG(bullying_exposure) AS average_bullying
FROM social_development_panel
GROUP BY school_id
ORDER BY average_social_self DESC;

-- Final-wave endpoint by profile.
WITH final_wave AS (
    SELECT MAX(time) AS max_time FROM social_development_panel
)
SELECT
    social_profile,
    chronic_exclusion,
    COUNT(*) AS observations,
    AVG(social_self_score) AS final_average_social_self,
    AVG(social_support_context) AS final_average_social_context,
    AVG(current_exclusion) AS final_average_exclusion,
    AVG(bullying_exposure) AS final_average_bullying,
    AVG(digital_comparison_stress) AS final_average_digital_comparison
FROM social_development_panel p
JOIN final_wave f ON p.time = f.max_time
GROUP BY social_profile, chronic_exclusion
ORDER BY final_average_social_self DESC;
