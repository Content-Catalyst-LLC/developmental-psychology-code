DROP TABLE IF EXISTS nature_nurture_development_panel;

CREATE TABLE nature_nurture_development_panel (
    child_id INTEGER NOT NULL,
    school_id INTEGER NOT NULL,
    time INTEGER NOT NULL,
    biological_sensitivity REAL,
    baseline_functioning REAL,
    structural_risk INTEGER,
    chronic_adversity INTEGER,
    family_support_context REAL,
    institutional_support REAL,
    disability_support REAL,
    resource_stability REAL,
    caregiver_support REAL,
    acute_stress REAL,
    intervention INTEGER,
    protective_context REAL,
    development_score REAL,
    sensitivity_profile TEXT,
    PRIMARY KEY (child_id, time)
);

CREATE INDEX idx_nature_nurture_school ON nature_nurture_development_panel (school_id);
CREATE INDEX idx_nature_nurture_time ON nature_nurture_development_panel (time);
CREATE INDEX idx_nature_nurture_profile ON nature_nurture_development_panel (sensitivity_profile);
CREATE INDEX idx_nature_nurture_risk ON nature_nurture_development_panel (structural_risk);
