DROP TABLE IF EXISTS adolescence_identity_panel;

CREATE TABLE adolescence_identity_panel (
    adolescent_id INTEGER NOT NULL,
    school_id INTEGER NOT NULL,
    time INTEGER NOT NULL,
    baseline_identity REAL,
    peer_support_base REAL,
    family_support_base REAL,
    school_connectedness_base REAL,
    future_orientation_base REAL,
    chronic_exclusion INTEGER,
    school_climate REAL,
    counseling_access REAL,
    extracurricular_access REAL,
    identity_safety REAL,
    digital_safety REAL,
    current_peer_support REAL,
    current_family_support REAL,
    current_connectedness REAL,
    current_future_orientation REAL,
    current_exclusion REAL,
    digital_stress REAL,
    support_context REAL,
    identity_score REAL,
    identity_profile TEXT,
    PRIMARY KEY (adolescent_id, time)
);

CREATE INDEX idx_adolescence_school ON adolescence_identity_panel (school_id);
CREATE INDEX idx_adolescence_time ON adolescence_identity_panel (time);
CREATE INDEX idx_adolescence_profile ON adolescence_identity_panel (identity_profile);
CREATE INDEX idx_adolescence_exclusion ON adolescence_identity_panel (chronic_exclusion);
