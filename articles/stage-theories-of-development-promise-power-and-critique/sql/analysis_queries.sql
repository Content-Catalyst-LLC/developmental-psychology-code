-- Trajectory by stage pattern.
SELECT
    time,
    stage_pattern,
    AVG(development_score) AS average_development_score,
    AVG(transition_readiness) AS average_transition_readiness,
    AVG(current_support) AS average_current_support,
    AVG(chronic_stress) AS average_chronic_stress,
    AVG(logistic_transition) AS average_logistic_transition
FROM stage_theory_development_panel
GROUP BY time, stage_pattern
ORDER BY time, stage_pattern;

-- Stage profile summary.
SELECT
    stage_profile,
    COUNT(DISTINCT child_id) AS individuals,
    AVG(development_score) AS average_development_score,
    AVG(transition_readiness) AS average_transition_readiness,
    AVG(current_support) AS average_current_support,
    AVG(chronic_stress) AS average_chronic_stress,
    AVG(threshold_time) AS average_threshold_time
FROM stage_theory_development_panel
GROUP BY stage_profile
ORDER BY average_development_score DESC;

-- Context summary.
SELECT
    context_id,
    COUNT(DISTINCT child_id) AS individuals,
    AVG(school_support) AS average_school_support,
    AVG(resource_stability) AS average_resource_stability,
    AVG(transition_readiness) AS average_transition_readiness,
    AVG(development_score) AS average_development_score
FROM stage_theory_development_panel
GROUP BY context_id
ORDER BY average_development_score DESC;

-- Final-wave endpoint by profile.
WITH final_wave AS (
    SELECT MAX(time) AS max_time FROM stage_theory_development_panel
)
SELECT
    stage_profile,
    stage_pattern,
    COUNT(*) AS individuals,
    AVG(development_score) AS final_average_development_score,
    AVG(transition_readiness) AS final_average_transition_readiness,
    AVG(chronic_stress) AS final_average_chronic_stress
FROM stage_theory_development_panel p
JOIN final_wave f ON p.time = f.max_time
GROUP BY stage_profile, stage_pattern
ORDER BY final_average_development_score DESC;
