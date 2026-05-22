-- Development trajectory by chronic stress group.
SELECT
    time,
    chronic_stress,
    AVG(development_score) AS average_development,
    AVG(current_pretend) AS average_pretend,
    AVG(current_social_play) AS average_social_play,
    AVG(current_constructive) AS average_constructive,
    AVG(current_outdoor) AS average_outdoor,
    AVG(current_stress) AS average_stress,
    AVG(play_restriction) AS average_play_restriction,
    AVG(peer_inclusion) AS average_peer_inclusion,
    AVG(play_support_context) AS average_play_support_context
FROM play_development_panel
GROUP BY time, chronic_stress
ORDER BY time, chronic_stress;

-- Play profile summary.
SELECT
    play_profile,
    COUNT(DISTINCT child_id) AS children,
    AVG(development_score) AS average_development,
    AVG(play_support_context) AS average_play_support_context,
    AVG(play_restriction) AS average_play_restriction,
    AVG(current_stress) AS average_stress,
    AVG(peer_inclusion) AS average_peer_inclusion,
    AVG(chronic_stress) AS chronic_stress_rate
FROM play_development_panel
GROUP BY play_profile
ORDER BY average_development DESC;

-- Context-level play ecology summary.
SELECT
    context_id,
    COUNT(DISTINCT child_id) AS children,
    AVG(play_space_quality) AS play_space_quality,
    AVG(adult_responsiveness) AS adult_responsiveness,
    AVG(inclusion_climate) AS inclusion_climate,
    AVG(outdoor_safety) AS outdoor_safety,
    AVG(play_material_access) AS play_material_access,
    AVG(development_score) AS average_development,
    AVG(play_support_context) AS average_play_support_context,
    AVG(play_restriction) AS average_play_restriction,
    AVG(peer_inclusion) AS average_peer_inclusion
FROM play_development_panel
GROUP BY context_id
ORDER BY average_development DESC;

-- Final-wave endpoint by profile.
WITH final_wave AS (
    SELECT MAX(time) AS max_time FROM play_development_panel
)
SELECT
    play_profile,
    chronic_stress,
    COUNT(*) AS observations,
    AVG(development_score) AS final_average_development,
    AVG(play_support_context) AS final_average_play_support_context,
    AVG(play_restriction) AS final_average_play_restriction,
    AVG(peer_inclusion) AS final_average_peer_inclusion
FROM play_development_panel p
JOIN final_wave f ON p.time = f.max_time
GROUP BY play_profile, chronic_stress
ORDER BY final_average_development DESC;
