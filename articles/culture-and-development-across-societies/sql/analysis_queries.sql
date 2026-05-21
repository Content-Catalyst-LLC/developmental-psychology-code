-- Analytical queries for synthetic culture and development data.

-- Average developmental trajectory by wave.
SELECT
    time,
    AVG(development_score) AS average_development_score,
    AVG(current_family) AS average_family_support,
    AVG(current_fit) AS average_institutional_fit,
    AVG(current_mismatch) AS average_cross_context_mismatch,
    AVG(current_support) AS average_social_support
FROM cultural_development_panel
GROUP BY time
ORDER BY time;

-- Cultural condition summary.
SELECT
    cultural_condition,
    COUNT(DISTINCT child_id) AS children,
    AVG(current_mismatch) AS average_mismatch,
    AVG(current_support) AS average_support,
    AVG(current_fit) AS average_institutional_fit,
    AVG(development_score) AS average_development_score
FROM cultural_development_panel
GROUP BY cultural_condition
ORDER BY average_development_score DESC;

-- Society-level summary.
SELECT
    society_id,
    COUNT(DISTINCT child_id) AS children,
    AVG(society_climate) AS society_climate,
    AVG(institutional_inclusion) AS institutional_inclusion,
    AVG(linguistic_support) AS linguistic_support,
    AVG(pluralism_index) AS pluralism_index,
    AVG(development_score) AS average_development_score
FROM cultural_development_panel
GROUP BY society_id
ORDER BY average_development_score DESC;

-- Mismatch/support contrast.
SELECT
    CASE
        WHEN current_mismatch < 0 AND current_support >= 0 THEN 'lower_mismatch_higher_support'
        WHEN current_mismatch >= 0 AND current_support >= 0 THEN 'higher_mismatch_higher_support'
        WHEN current_mismatch < 0 AND current_support < 0 THEN 'lower_mismatch_lower_support'
        ELSE 'higher_mismatch_lower_support'
    END AS mismatch_support_group,
    COUNT(*) AS observations,
    AVG(development_score) AS average_development_score
FROM cultural_development_panel
GROUP BY mismatch_support_group
ORDER BY average_development_score DESC;
