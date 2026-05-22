SELECT
    time,
    chronic_exclusion,
    AVG(conscience_score) AS average_conscience,
    AVG(moral_action_score) AS average_moral_action,
    AVG(moral_support_context) AS average_moral_support_context,
    AVG(current_exclusion) AS average_exclusion,
    AVG(peer_pressure) AS average_peer_pressure
FROM moral_development_panel
GROUP BY time, chronic_exclusion
ORDER BY time, chronic_exclusion;

SELECT
    moral_profile,
    COUNT(DISTINCT child_id) AS children,
    AVG(conscience_score) AS average_conscience,
    AVG(moral_action_score) AS average_moral_action,
    AVG(moral_support_context) AS average_moral_support_context,
    AVG(current_exclusion) AS average_exclusion,
    AVG(peer_pressure) AS average_peer_pressure,
    AVG(chronic_exclusion) AS chronic_exclusion_rate
FROM moral_development_panel
GROUP BY moral_profile
ORDER BY average_conscience DESC;

SELECT
    school_id,
    COUNT(DISTINCT child_id) AS children,
    AVG(school_moral_climate) AS school_moral_climate,
    AVG(restorative_practice_access) AS restorative_practice_access,
    AVG(punitive_inconsistency) AS punitive_inconsistency,
    AVG(anti_bullying_climate) AS anti_bullying_climate,
    AVG(digital_moral_safety) AS digital_moral_safety,
    AVG(conscience_score) AS average_conscience,
    AVG(moral_action_score) AS average_moral_action,
    AVG(moral_support_context) AS average_moral_support_context
FROM moral_development_panel
GROUP BY school_id
ORDER BY average_conscience DESC;
