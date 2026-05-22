SELECT
    time,
    chronic_stigma,
    AVG(adjustment_score) AS average_adjustment,
    AVG(protective_context) AS average_protective_context,
    AVG(current_peer_comparison) AS average_peer_comparison,
    AVG(current_body_concern) AS average_body_concern,
    AVG(current_stigma) AS average_stigma,
    AVG(digital_visibility_stress) AS average_digital_visibility_stress
FROM puberty_embodiment_panel
GROUP BY time, chronic_stigma
ORDER BY time, chronic_stigma;

SELECT
    puberty_profile,
    COUNT(DISTINCT adolescent_id) AS adolescents,
    AVG(adjustment_score) AS average_adjustment,
    AVG(protective_context) AS average_protective_context,
    AVG(current_stigma) AS average_stigma,
    AVG(current_body_concern) AS average_body_concern,
    AVG(digital_visibility_stress) AS average_digital_visibility_stress,
    AVG(ABS(timing_deviation)) AS average_abs_timing_deviation
FROM puberty_embodiment_panel
GROUP BY puberty_profile
ORDER BY average_adjustment DESC;

SELECT
    school_id,
    COUNT(DISTINCT adolescent_id) AS adolescents,
    AVG(school_support) AS school_support,
    AVG(health_education_quality) AS health_education_quality,
    AVG(privacy_protection) AS privacy_protection,
    AVG(menstrual_support) AS menstrual_support,
    AVG(disability_accommodation) AS disability_accommodation,
    AVG(anti_harassment_climate) AS anti_harassment_climate,
    AVG(digital_safety) AS digital_safety,
    AVG(adjustment_score) AS average_adjustment
FROM puberty_embodiment_panel
GROUP BY school_id
ORDER BY average_adjustment DESC;
