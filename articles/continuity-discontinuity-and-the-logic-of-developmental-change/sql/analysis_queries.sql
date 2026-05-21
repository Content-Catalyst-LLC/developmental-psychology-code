-- Trajectory by threshold sensitivity.
SELECT
    time,
    threshold_sensitive,
    AVG(development_score) AS average_development_score,
    AVG(transition_readiness) AS average_transition_readiness,
    AVG(current_support) AS average_current_support,
    AVG(chronic_stress) AS average_chronic_stress,
    AVG(institutional_rupture) AS average_institutional_rupture,
    AVG(intervention_exposure) AS average_intervention_exposure,
    AVG(logistic_transition) AS average_logistic_transition
FROM continuity_discontinuity_panel
GROUP BY time, threshold_sensitive
ORDER BY time, threshold_sensitive;

-- Developmental change profile summary.
SELECT
    change_profile,
    COUNT(DISTINCT person_id) AS individuals,
    AVG(development_score) AS average_development_score,
    AVG(transition_readiness) AS average_transition_readiness,
    AVG(current_support) AS average_current_support,
    AVG(chronic_stress) AS average_chronic_stress,
    AVG(institutional_rupture) AS average_institutional_rupture,
    AVG(intervention_exposure) AS average_intervention_exposure,
    AVG(threshold_time) AS average_threshold_time
FROM continuity_discontinuity_panel
GROUP BY change_profile
ORDER BY average_development_score DESC;

-- Context summary.
SELECT
    context_id,
    COUNT(DISTINCT person_id) AS individuals,
    AVG(school_support) AS average_school_support,
    AVG(resource_stability) AS average_resource_stability,
    AVG(transition_readiness) AS average_transition_readiness,
    AVG(development_score) AS average_development_score
FROM continuity_discontinuity_panel
GROUP BY context_id
ORDER BY average_development_score DESC;

-- Final-wave endpoint by profile.
WITH final_wave AS (
    SELECT MAX(time) AS max_time FROM continuity_discontinuity_panel
)
SELECT
    change_profile,
    threshold_sensitive,
    COUNT(*) AS individuals,
    AVG(development_score) AS final_average_development_score,
    AVG(transition_readiness) AS final_average_transition_readiness,
    AVG(chronic_stress) AS final_average_chronic_stress,
    AVG(institutional_rupture) AS final_average_rupture,
    AVG(intervention_exposure) AS final_average_intervention
FROM continuity_discontinuity_panel p
JOIN final_wave f ON p.time = f.max_time
GROUP BY change_profile, threshold_sensitive
ORDER BY final_average_development_score DESC;
