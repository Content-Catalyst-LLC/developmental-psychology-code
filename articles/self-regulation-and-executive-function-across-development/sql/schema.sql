DROP TABLE IF EXISTS regulation_development_panel;

CREATE TABLE regulation_development_panel (
    child_id INTEGER NOT NULL,
    school_id INTEGER NOT NULL,
    time INTEGER NOT NULL,
    baseline_ef REAL,
    caregiving_support REAL,
    classroom_structure REAL,
    sleep_quality REAL,
    chronic_stress INTEGER,
    temperament_reactivity REAL,
    disability_support_need INTEGER,
    school_climate REAL,
    regulation_scaffolding REAL,
    disability_accommodation REAL,
    transition_predictability REAL,
    current_support REAL,
    current_structure REAL,
    current_sleep REAL,
    acute_stress REAL,
    intervention_exposure INTEGER,
    regulatory_support_context REAL,
    regulation_score REAL,
    regulation_profile TEXT,
    PRIMARY KEY (child_id, time)
);

CREATE INDEX idx_reg_school ON regulation_development_panel (school_id);
CREATE INDEX idx_reg_time ON regulation_development_panel (time);
CREATE INDEX idx_reg_profile ON regulation_development_panel (regulation_profile);
CREATE INDEX idx_reg_stress ON regulation_development_panel (chronic_stress);
