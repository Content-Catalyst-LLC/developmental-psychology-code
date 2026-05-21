-- Analytical queries for developmental research design data.

-- Cross-sectional age comparison from the first period.
SELECT
    age,
    COUNT(*) AS observations,
    AVG(development_score) AS average_development_score
FROM developmental_design_panel
WHERE observed = 1
  AND period = (SELECT MIN(period) FROM developmental_design_panel)
GROUP BY age
ORDER BY age;

-- Longitudinal mean trajectory by study wave.
SELECT
    study_wave,
    AVG(age) AS average_age,
    COUNT(*) AS observations,
    AVG(development_score) AS average_development_score
FROM developmental_design_panel
WHERE observed = 1
GROUP BY study_wave
ORDER BY study_wave;

-- Cohort-sequential trajectories.
SELECT
    birth_cohort,
    age,
    COUNT(*) AS observations,
    AVG(development_score) AS average_development_score
FROM developmental_design_panel
WHERE observed = 1
GROUP BY birth_cohort, age
ORDER BY birth_cohort, age;

-- Missingness / observation rate by wave.
SELECT
    study_wave,
    AVG(observed) AS observation_rate,
    SUM(observed) AS observations,
    COUNT(*) AS possible_observations
FROM developmental_design_panel
GROUP BY study_wave
ORDER BY study_wave;

-- Age-period-cohort check.
SELECT
    birth_cohort,
    period,
    age,
    COUNT(*) AS observations
FROM developmental_design_panel
GROUP BY birth_cohort, period, age
ORDER BY birth_cohort, period, age;
