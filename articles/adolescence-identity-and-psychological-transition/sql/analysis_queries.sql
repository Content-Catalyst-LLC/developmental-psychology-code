SELECT
  time,
  chronic_exclusion,
  AVG(identity_score) AS average_identity_score,
  AVG(support_context) AS average_support_context,
  AVG(current_exclusion) AS average_exclusion,
  AVG(digital_stress) AS average_digital_stress
FROM adolescence_identity_panel
GROUP BY time, chronic_exclusion
ORDER BY time, chronic_exclusion;

SELECT
  identity_profile,
  COUNT(DISTINCT adolescent_id) AS adolescents,
  AVG(identity_score) AS average_identity_score,
  AVG(support_context) AS average_support_context,
  AVG(current_exclusion) AS average_exclusion,
  AVG(digital_stress) AS average_digital_stress
FROM adolescence_identity_panel
GROUP BY identity_profile
ORDER BY average_identity_score DESC;

SELECT
  school_id,
  COUNT(DISTINCT adolescent_id) AS adolescents,
  AVG(school_climate) AS school_climate,
  AVG(counseling_access) AS counseling_access,
  AVG(extracurricular_access) AS extracurricular_access,
  AVG(identity_safety) AS identity_safety,
  AVG(digital_safety) AS digital_safety,
  AVG(identity_score) AS average_identity_score
FROM adolescence_identity_panel
GROUP BY school_id
ORDER BY average_identity_score DESC;
