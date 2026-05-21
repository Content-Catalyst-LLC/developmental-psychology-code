DROP TABLE IF EXISTS stage_theory_development_panel;

CREATE TABLE stage_theory_development_panel (
    child_id INTEGER NOT NULL,
    context_id INTEGER NOT NULL,
    time INTEGER NOT NULL,
    baseline_functioning REAL,
    growth_rate REAL,
    support_context REAL,
    chronic_stress INTEGER,
    threshold_time INTEGER,
    stage_pattern INTEGER,
    school_support REAL,
    resource_stability REAL,
    current_support REAL,
    threshold_on INTEGER,
    logistic_transition REAL,
    transition_readiness REAL,
    development_score REAL,
    stage_profile TEXT,
    PRIMARY KEY (child_id, time)
);

CREATE INDEX idx_stage_context ON stage_theory_development_panel (context_id);
CREATE INDEX idx_stage_time ON stage_theory_development_panel (time);
CREATE INDEX idx_stage_profile ON stage_theory_development_panel (stage_profile);
CREATE INDEX idx_stage_pattern ON stage_theory_development_panel (stage_pattern);
