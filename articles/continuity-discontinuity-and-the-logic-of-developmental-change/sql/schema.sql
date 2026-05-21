DROP TABLE IF EXISTS continuity_discontinuity_panel;

CREATE TABLE continuity_discontinuity_panel (
    person_id INTEGER NOT NULL,
    context_id INTEGER NOT NULL,
    time INTEGER NOT NULL,
    baseline_functioning REAL,
    growth_rate REAL,
    curvature REAL,
    support_context REAL,
    chronic_stress INTEGER,
    institutional_rupture INTEGER,
    intervention_exposure INTEGER,
    threshold_time INTEGER,
    threshold_sensitive INTEGER,
    school_support REAL,
    resource_stability REAL,
    current_support REAL,
    threshold_on INTEGER,
    logistic_transition REAL,
    transition_readiness REAL,
    development_score REAL,
    change_profile TEXT,
    PRIMARY KEY (person_id, time)
);

CREATE INDEX idx_cont_disc_context ON continuity_discontinuity_panel (context_id);
CREATE INDEX idx_cont_disc_time ON continuity_discontinuity_panel (time);
CREATE INDEX idx_cont_disc_profile ON continuity_discontinuity_panel (change_profile);
CREATE INDEX idx_cont_disc_threshold ON continuity_discontinuity_panel (threshold_sensitive);
