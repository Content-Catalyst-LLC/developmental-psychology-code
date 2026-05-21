-- Analytical queries for synthetic trauma/adversity life-course data.

-- Average adaptation trajectory by wave.
SELECT
    time,
    AVG(adaptation_score) AS average_adaptation_score,
    AVG(current_adversity) AS average_adversity,
    AVG(current_support) AS average_support,
    AVG(current_stability) AS average_stability,
    AVG(cumulative_adversity) AS average_cumulative_adversity
FROM trauma_life_course_panel
GROUP BY time
ORDER BY time;

-- Adversity-support profile summary.
SELECT
    adversity_support_profile,
    COUNT(DISTINCT child_id) AS children,
    AVG(current_adversity) AS average_adversity,
    AVG(current_support) AS average_support,
    AVG(current_stability) AS average_stability,
    AVG(adaptation_score) AS average_adaptation_score
FROM trauma_life_course_panel
GROUP BY adversity_support_profile
ORDER BY average_adaptation_score DESC;

-- Context-level trauma-informed system summary.
SELECT
    context_id,
    COUNT(DISTINCT child_id) AS children,
    AVG(community_buffer) AS community_buffer,
    AVG(institutional_safety) AS institutional_safety,
    AVG(service_access) AS service_access,
    AVG(adaptation_score) AS average_adaptation_score
FROM trauma_life_course_panel
GROUP BY context_id
ORDER BY average_adaptation_score DESC;

-- Buffering interaction proxy.
SELECT
    CASE
        WHEN current_adversity < 0 AND current_support >= 0 THEN 'lower_adversity_higher_support'
        WHEN current_adversity >= 0 AND current_support >= 0 THEN 'higher_adversity_higher_support'
        WHEN current_adversity < 0 AND current_support < 0 THEN 'lower_adversity_lower_support'
        ELSE 'higher_adversity_lower_support'
    END AS adversity_support_group,
    COUNT(*) AS observations,
    AVG(adaptation_score) AS average_adaptation_score
FROM trauma_life_course_panel
GROUP BY adversity_support_group
ORDER BY average_adaptation_score DESC;
