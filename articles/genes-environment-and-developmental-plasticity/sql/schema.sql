DROP TABLE IF EXISTS genes_environment_plasticity_panel;

CREATE TABLE genes_environment_plasticity_panel (
    child_id INTEGER NOT NULL,
    context_id INTEGER NOT NULL,
    time INTEGER NOT NULL,
    bio_sensitivity REAL,
    caregiving_quality REAL,
    environmental_stress REAL,
    nutritional_support REAL,
    early_exposure INTEGER,
    intervention_support INTEGER,
    school_support REAL,
    neighborhood_safety REAL,
    service_access REAL,
    timing_weight REAL,
    current_care REAL,
    current_stress REAL,
    current_nutrition REAL,
    weighted_stress REAL,
    weighted_support REAL,
    embedded_stress REAL,
    embedded_support REAL,
    development_score REAL,
    sensitivity_stress_profile TEXT,
    PRIMARY KEY (child_id, time)
);

CREATE INDEX idx_plasticity_context ON genes_environment_plasticity_panel (context_id);
CREATE INDEX idx_plasticity_time ON genes_environment_plasticity_panel (time);
CREATE INDEX idx_plasticity_profile ON genes_environment_plasticity_panel (sensitivity_stress_profile);
CREATE INDEX idx_plasticity_early ON genes_environment_plasticity_panel (early_exposure);
