SELECT time, chronic_stress,
       AVG(developmental_outcome) AS average_developmental_outcome,
       AVG(neural_state) AS average_neural_state,
       AVG(acute_stress) AS average_stress,
       AVG(developmental_support_context) AS average_developmental_support_context
FROM brain_development_panel
GROUP BY time, chronic_stress
ORDER BY time, chronic_stress;

SELECT neurodevelopment_profile,
       COUNT(DISTINCT child_id) AS children,
       AVG(neural_state) AS average_neural_state,
       AVG(developmental_outcome) AS average_developmental_outcome,
       AVG(developmental_support_context) AS average_support_context,
       AVG(acute_stress) AS average_stress,
       AVG(chronic_stress) AS chronic_stress_rate
FROM brain_development_panel
GROUP BY neurodevelopment_profile
ORDER BY average_developmental_outcome DESC;

SELECT context_id,
       COUNT(DISTINCT child_id) AS children,
       AVG(school_support) AS school_support,
       AVG(neighborhood_safety) AS neighborhood_safety,
       AVG(health_service_access) AS health_service_access,
       AVG(environmental_risk) AS environmental_risk,
       AVG(neural_state) AS average_neural_state,
       AVG(developmental_outcome) AS average_developmental_outcome,
       AVG(acute_stress) AS average_stress
FROM brain_development_panel
GROUP BY context_id
ORDER BY average_developmental_outcome DESC;
