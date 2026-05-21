-- Selected historical checkpoints.
SELECT
    year,
    child_study,
    behaviorist,
    cognitive_developmental,
    ecological,
    lifespan,
    developmental_systems,
    broadening_index
FROM developmental_psychology_history_panel
WHERE year IN (1900, 1930, 1950, 1975, 2000, 2025)
ORDER BY year;

-- Years with highest synthetic broadening index.
SELECT
    year,
    broadening_index,
    lifespan_index,
    ecological_systems_index,
    institutional_support,
    methodological_advantage,
    social_relevance,
    critique_index
FROM developmental_psychology_history_panel
ORDER BY broadening_index DESC
LIMIT 15;

-- Historical period summaries.
SELECT
    CASE
        WHEN year < 1930 THEN '1900-1929 early child-study consolidation'
        WHEN year < 1960 THEN '1930-1959 measurement, maturation, learning, psychoanalysis'
        WHEN year < 1980 THEN '1960-1979 cognitive, attachment, institutional expansion'
        WHEN year < 2000 THEN '1980-1999 lifespan, ecological, psychopathology broadening'
        ELSE '2000-2025 systems, neuroscience, critique, inequality'
    END AS historical_period,
    AVG(child_centered_index) AS avg_child_centered,
    AVG(lifespan_index) AS avg_lifespan,
    AVG(ecological_systems_index) AS avg_ecological_systems,
    AVG(broadening_index) AS avg_broadening,
    AVG(critique_index) AS avg_critique
FROM developmental_psychology_history_panel
GROUP BY historical_period
ORDER BY MIN(year);
