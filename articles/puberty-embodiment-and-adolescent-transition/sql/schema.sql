DROP TABLE IF EXISTS puberty_embodiment_panel;

CREATE TABLE puberty_embodiment_panel (
    adolescent_id INTEGER NOT NULL,
    school_id INTEGER NOT NULL,
    time INTEGER NOT NULL,
    baseline_adjustment REAL,
    timing_deviation REAL,
    family_support_base REAL,
    peer_comparison_base REAL,
    body_image_vulnerability REAL,
    chronic_stigma INTEGER,
    school_support REAL,
    health_education_quality REAL,
    privacy_protection REAL,
    menstrual_support REAL,
    disability_accommodation REAL,
    anti_harassment_climate REAL,
    digital_safety REAL,
    pubertal_progress REAL,
    current_family_support REAL,
    current_peer_comparison REAL,
    current_body_concern REAL,
    current_stigma REAL,
    digital_visibility_stress REAL,
    protective_context REAL,
    adjustment_score REAL,
    puberty_profile TEXT,
    PRIMARY KEY (adolescent_id, time)
);

CREATE INDEX idx_puberty_school ON puberty_embodiment_panel (school_id);
CREATE INDEX idx_puberty_time ON puberty_embodiment_panel (time);
CREATE INDEX idx_puberty_profile ON puberty_embodiment_panel (puberty_profile);
CREATE INDEX idx_puberty_stigma ON puberty_embodiment_panel (chronic_stigma);
