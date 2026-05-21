-- Schema for synthetic developmental research design panel data.

DROP TABLE IF EXISTS developmental_design_panel;

CREATE TABLE developmental_design_panel (
    person_id INTEGER NOT NULL,
    context_id INTEGER NOT NULL,
    birth_cohort INTEGER NOT NULL,
    study_wave INTEGER NOT NULL,
    period INTEGER NOT NULL,
    age REAL NOT NULL,
    baseline_trait REAL,
    support REAL,
    risk REAL,
    context_quality REAL,
    cohort_effect REAL,
    period_effect REAL,
    development_score REAL,
    observed INTEGER,
    PRIMARY KEY (person_id, study_wave)
);

CREATE INDEX idx_design_panel_context
ON developmental_design_panel (context_id);

CREATE INDEX idx_design_panel_cohort
ON developmental_design_panel (birth_cohort);

CREATE INDEX idx_design_panel_age
ON developmental_design_panel (age);

CREATE INDEX idx_design_panel_period
ON developmental_design_panel (period);
