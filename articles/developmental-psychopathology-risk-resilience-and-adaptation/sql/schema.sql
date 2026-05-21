DROP TABLE IF EXISTS developmental_psychopathology_panel;

CREATE TABLE developmental_psychopathology_panel (
    child_id INTEGER NOT NULL,
    context_id INTEGER NOT NULL,
    time INTEGER NOT NULL,
    baseline_regulation REAL,
    protective_support REAL,
    accumulated_risk REAL,
    caregiver_stability REAL,
    biological_sensitivity REAL,
    community_support REAL,
    school_belonging REAL,
    service_access REAL,
    current_regulation REAL,
    current_support REAL,
    current_risk REAL,
    current_stability REAL,
    timing_weight REAL,
    transition_weight REAL,
    weighted_risk REAL,
    transition_support REAL,
    cumulative_risk REAL,
    cumulative_support REAL,
    adaptation_score REAL,
    internalizing_score REAL,
    externalizing_score REAL,
    risk_support_profile TEXT,
    PRIMARY KEY (child_id, time)
);

CREATE INDEX idx_psychopathology_context ON developmental_psychopathology_panel (context_id);
CREATE INDEX idx_psychopathology_time ON developmental_psychopathology_panel (time);
CREATE INDEX idx_psychopathology_profile ON developmental_psychopathology_panel (risk_support_profile);
