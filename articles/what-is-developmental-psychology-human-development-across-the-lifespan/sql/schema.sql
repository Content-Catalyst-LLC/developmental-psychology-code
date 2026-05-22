DROP TABLE IF EXISTS developmental_lifespan_panel;

CREATE TABLE developmental_lifespan_panel (
    child_id INTEGER NOT NULL,
    school_id INTEGER NOT NULL,
    time INTEGER NOT NULL,
    baseline_regulation REAL,
    caregiver_support REAL,
    family_support REAL,
    school_support REAL,
    disability_support_need INTEGER,
    structural_risk INTEGER,
    school_climate REAL,
    disability_accommodation REAL,
    counseling_access REAL,
    language_access REAL,
    community_resource_index REAL,
    acute_stress REAL,
    current_support REAL,
    intervention INTEGER,
    protective_context REAL,
    development_score REAL,
    development_profile TEXT,
    PRIMARY KEY (child_id, time)
);

CREATE INDEX idx_dev_life_school ON developmental_lifespan_panel (school_id);
CREATE INDEX idx_dev_life_time ON developmental_lifespan_panel (time);
CREATE INDEX idx_dev_life_profile ON developmental_lifespan_panel (development_profile);
CREATE INDEX idx_dev_life_risk ON developmental_lifespan_panel (structural_risk);
