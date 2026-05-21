-- Adjustment trajectory by chronic stigma group.
SELECT
    time,
    chronic_stigma,
    AVG(adjustment_score) AS average_adjustment,
    AVG(protective_context) AS average_protective_context,
    AVG(current_stigma) AS average_stigma,
    AVG(current_family_support) AS average_family_support,
    AVG(current_recognition) AS average_recognition,
    AVG(current_consent_knowledge) AS average_consent_knowledge,
    AVG(current_connectedness) AS average_connectedness
FROM gender_sexual_development_panel
GROUP BY time, chronic_stigma
ORDER BY time, chronic_stigma;

-- Development profile summary.
SELECT
    development_profile,
    COUNT(DISTINCT id) AS adolescents,
    AVG(adjustment_score) AS average_adjustment,
    AVG(protective_context) AS average_protective_context,
    AVG(current_stigma) AS average_stigma,
    AVG(current_family_support) AS average_family_support,
    AVG(current_recognition) AS average_recognition,
    AVG(current_consent_knowledge) AS average_consent_knowledge,
    AVG(current_connectedness) AS average_connectedness
FROM gender_sexual_development_panel
GROUP BY development_profile
ORDER BY average_adjustment DESC;

-- School context summary.
SELECT
    school_id,
    COUNT(DISTINCT id) AS adolescents,
    AVG(school_climate) AS school_climate,
    AVG(health_education_quality) AS health_education_quality,
    AVG(anti_harassment_support) AS anti_harassment_support,
    AVG(adjustment_score) AS average_adjustment,
    AVG(current_stigma) AS average_stigma
FROM gender_sexual_development_panel
GROUP BY school_id
ORDER BY average_adjustment DESC;

-- Final-wave endpoint by development profile.
WITH final_wave AS (
    SELECT MAX(time) AS max_time FROM gender_sexual_development_panel
)
SELECT
    development_profile,
    chronic_stigma,
    COUNT(*) AS adolescents,
    AVG(adjustment_score) AS final_average_adjustment,
    AVG(protective_context) AS final_average_protective_context,
    AVG(current_stigma) AS final_average_stigma
FROM gender_sexual_development_panel p
JOIN final_wave f ON p.time = f.max_time
GROUP BY development_profile, chronic_stigma
ORDER BY final_average_adjustment DESC;
