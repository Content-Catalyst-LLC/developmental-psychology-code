-- Language trajectory by chronic stress group.
SELECT
    time,
    chronic_stress,
    AVG(language_score) AS average_language,
    AVG(current_interaction) AS average_interaction,
    AVG(current_reading) AS average_reading,
    AVG(current_joint_attention) AS average_joint_attention,
    AVG(current_turn_taking) AS average_turn_taking,
    AVG(current_stress) AS average_stress,
    AVG(language_support_context) AS average_language_support_context
FROM language_development_panel
GROUP BY time, chronic_stress
ORDER BY time, chronic_stress;

-- Language profile summary.
SELECT
    language_profile,
    COUNT(DISTINCT child_id) AS children,
    AVG(language_score) AS average_language,
    AVG(language_support_context) AS average_language_support_context,
    AVG(current_interaction) AS average_interaction,
    AVG(current_reading) AS average_reading,
    AVG(current_joint_attention) AS average_joint_attention,
    AVG(current_turn_taking) AS average_turn_taking,
    AVG(current_stress) AS average_stress,
    AVG(chronic_stress) AS chronic_stress_rate,
    AVG(multilingual_exposure) AS multilingual_exposure_rate
FROM language_development_panel
GROUP BY language_profile
ORDER BY average_language DESC;

-- Context-level language ecology summary.
SELECT
    context_id,
    COUNT(DISTINCT child_id) AS children,
    AVG(language_ecology_support) AS language_ecology_support,
    AVG(book_access) AS book_access,
    AVG(early_education_quality) AS early_education_quality,
    AVG(home_language_recognition) AS home_language_recognition,
    AVG(language_score) AS average_language,
    AVG(current_stress) AS average_stress,
    AVG(language_support_context) AS average_language_support_context
FROM language_development_panel
GROUP BY context_id
ORDER BY average_language DESC;

-- Multilingual exposure and home-language recognition.
SELECT
    multilingual_exposure,
    CASE
      WHEN home_language_recognition >= 0 THEN 'higher_home_language_recognition'
      ELSE 'lower_home_language_recognition'
    END AS recognition_group,
    COUNT(DISTINCT child_id) AS children,
    AVG(language_score) AS average_language,
    AVG(language_support_context) AS average_language_support_context
FROM language_development_panel
GROUP BY multilingual_exposure, recognition_group
ORDER BY multilingual_exposure, recognition_group;

-- Final-wave endpoint by profile.
WITH final_wave AS (
    SELECT MAX(time) AS max_time FROM language_development_panel
)
SELECT
    language_profile,
    chronic_stress,
    multilingual_exposure,
    COUNT(*) AS observations,
    AVG(language_score) AS final_average_language,
    AVG(language_support_context) AS final_average_language_support_context,
    AVG(current_interaction) AS final_average_interaction,
    AVG(current_reading) AS final_average_reading,
    AVG(current_stress) AS final_average_stress
FROM language_development_panel p
JOIN final_wave f ON p.time = f.max_time
GROUP BY language_profile, chronic_stress, multilingual_exposure
ORDER BY final_average_language DESC;
