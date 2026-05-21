SELECT
    time,
    AVG(development_score) AS average_development_score,
    AVG(current_resources) AS average_resources,
    AVG(current_burden) AS average_burden,
    AVG(current_support) AS average_support
FROM life_course_inequality_panel
GROUP BY time
ORDER BY time;

SELECT
    inequality_profile,
    COUNT(DISTINCT person_id) AS people,
    AVG(current_resources) AS average_resources,
    AVG(current_burden) AS average_burden,
    AVG(current_support) AS average_support,
    AVG(development_score) AS average_development_score
FROM life_course_inequality_panel
GROUP BY inequality_profile
ORDER BY average_development_score DESC;

SELECT
    context_id,
    COUNT(DISTINCT person_id) AS people,
    AVG(community_opportunity) AS community_opportunity,
    AVG(institutional_support) AS institutional_support,
    AVG(environmental_safety) AS environmental_safety,
    AVG(development_score) AS average_development_score
FROM life_course_inequality_panel
GROUP BY context_id
ORDER BY average_development_score DESC;
