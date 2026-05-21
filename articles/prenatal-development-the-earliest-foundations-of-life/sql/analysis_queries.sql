-- Prenatal profile summary.
SELECT
    prenatal_profile,
    COUNT(*) AS cases,
    AVG(early_outcome) AS average_early_outcome,
    AVG(effective_care) AS average_effective_care,
    AVG(developmental_risk) AS average_developmental_risk,
    AVG(gestational_weeks) AS average_gestation,
    AVG(maternal_health) AS average_maternal_health,
    AVG(nutrition_support) AS average_nutrition,
    AVG(social_support) AS average_social_support
FROM prenatal_development_foundations_panel
GROUP BY prenatal_profile
ORDER BY average_early_outcome DESC;

-- Neighborhood context summary.
SELECT
    neighborhood_context,
    COUNT(*) AS cases,
    AVG(early_outcome) AS average_early_outcome,
    AVG(healthcare_access) AS average_healthcare_access,
    AVG(environmental_burden) AS average_environmental_burden,
    AVG(economic_security) AS average_economic_security,
    AVG(effective_care) AS average_effective_care,
    AVG(developmental_risk) AS average_developmental_risk
FROM prenatal_development_foundations_panel
GROUP BY neighborhood_context
ORDER BY average_early_outcome DESC;

-- High-risk / lower-care cases for synthetic audit.
SELECT
    prenatal_profile,
    COUNT(*) AS cases,
    AVG(early_outcome) AS average_early_outcome,
    AVG(chronic_stress) AS average_chronic_stress,
    AVG(toxic_exposure) AS average_toxic_exposure,
    AVG(environmental_burden) AS average_environmental_burden,
    AVG(prenatal_care) AS average_prenatal_care
FROM prenatal_development_foundations_panel
WHERE developmental_risk > 0 AND effective_care < 0
GROUP BY prenatal_profile
ORDER BY cases DESC;

-- Gestational timing summary.
SELECT
    CASE
        WHEN gestational_weeks < 37 THEN 'earlier_than_37_weeks'
        WHEN gestational_weeks BETWEEN 37 AND 41 THEN '37_to_41_weeks'
        ELSE 'later_than_41_weeks'
    END AS gestational_group,
    COUNT(*) AS cases,
    AVG(early_outcome) AS average_early_outcome,
    AVG(effective_care) AS average_effective_care,
    AVG(developmental_risk) AS average_developmental_risk
FROM prenatal_development_foundations_panel
GROUP BY gestational_group
ORDER BY gestational_group;
