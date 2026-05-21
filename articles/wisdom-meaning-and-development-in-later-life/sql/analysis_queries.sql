-- Average meaning, wisdom, connection, reflection, health, and support trajectories.
SELECT
    time,
    AVG(meaning_score) AS average_meaning,
    AVG(wisdom_index) AS average_wisdom,
    AVG(current_connection) AS average_connection,
    AVG(current_reflection) AS average_reflection,
    AVG(current_health) AS average_health,
    AVG(current_support) AS average_support
FROM wisdom_meaning_later_life_panel
GROUP BY time
ORDER BY time;

-- Meaning-profile summary.
SELECT
    meaning_profile,
    COUNT(DISTINCT id) AS older_adults,
    AVG(meaning_score) AS average_meaning,
    AVG(wisdom_index) AS average_wisdom,
    AVG(current_connection) AS average_connection,
    AVG(current_reflection) AS average_reflection,
    AVG(current_health) AS average_health,
    AVG(current_support) AS average_support
FROM wisdom_meaning_later_life_panel
GROUP BY meaning_profile
ORDER BY average_meaning DESC;

-- Care-context dignity and meaning.
SELECT
    care_context_id,
    COUNT(DISTINCT id) AS older_adults,
    AVG(dignity_support) AS dignity_support,
    AVG(service_access) AS service_access,
    AVG(community_participation) AS community_participation,
    AVG(meaning_score) AS average_meaning,
    AVG(wisdom_index) AS average_wisdom
FROM wisdom_meaning_later_life_panel
GROUP BY care_context_id
ORDER BY average_meaning DESC;

-- Final-wave later-life meaning endpoint summary.
WITH final_wave AS (
    SELECT MAX(time) AS max_time FROM wisdom_meaning_later_life_panel
)
SELECT
    meaning_profile,
    COUNT(*) AS older_adults,
    AVG(meaning_score) AS final_average_meaning,
    AVG(wisdom_index) AS final_average_wisdom,
    AVG(current_connection) AS final_average_connection,
    AVG(current_health) AS final_average_health
FROM wisdom_meaning_later_life_panel p
JOIN final_wave f ON p.time = f.max_time
GROUP BY meaning_profile
ORDER BY final_average_meaning DESC;
