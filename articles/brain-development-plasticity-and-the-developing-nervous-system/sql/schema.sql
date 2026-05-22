DROP TABLE IF EXISTS brain_development_panel;

CREATE TABLE brain_development_panel (
    child_id INTEGER NOT NULL,
    context_id INTEGER NOT NULL,
    time INTEGER NOT NULL,
    baseline_neural_state REAL,
    family_support REAL,
    learning_context REAL,
    sleep_quality REAL,
    sensory_regulation_support REAL,
    chronic_stress INTEGER,
    school_support REAL,
    neighborhood_safety REAL,
    health_service_access REAL,
    environmental_risk REAL,
    current_family_support REAL,
    current_learning REAL,
    current_sleep REAL,
    current_sensory_support REAL,
    acute_stress REAL,
    developmental_support_context REAL,
    neural_state REAL,
    developmental_outcome REAL,
    neurodevelopment_profile TEXT,
    PRIMARY KEY (child_id, time)
);

CREATE INDEX idx_brain_context ON brain_development_panel (context_id);
CREATE INDEX idx_brain_time ON brain_development_panel (time);
CREATE INDEX idx_brain_profile ON brain_development_panel (neurodevelopment_profile);
CREATE INDEX idx_brain_stress ON brain_development_panel (chronic_stress);
