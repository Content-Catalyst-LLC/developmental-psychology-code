DROP TABLE IF EXISTS developmental_systems_panel;

CREATE TABLE developmental_systems_panel (
    child_id INTEGER NOT NULL,
    school_id INTEGER NOT NULL,
    neighborhood_id INTEGER NOT NULL,
    time INTEGER NOT NULL,
    biological_sensitivity REAL,
    family_support REAL,
    peer_belonging REAL,
    intervention_exposure INTEGER,
    school_climate REAL,
    curriculum_opportunity REAL,
    neighborhood_safety REAL,
    service_access REAL,
    material_security REAL,
    current_family REAL,
    current_peer REAL,
    ecological_support REAL,
    ecological_stress REAL,
    development_score REAL,
    ecological_support_profile TEXT,
    PRIMARY KEY (child_id, time)
);

CREATE INDEX idx_systems_school ON developmental_systems_panel (school_id);
CREATE INDEX idx_systems_neighborhood ON developmental_systems_panel (neighborhood_id);
CREATE INDEX idx_systems_time ON developmental_systems_panel (time);
CREATE INDEX idx_systems_profile ON developmental_systems_panel (ecological_support_profile);
CREATE INDEX idx_systems_intervention ON developmental_systems_panel (intervention_exposure);
