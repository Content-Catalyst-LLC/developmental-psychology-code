DROP TABLE IF EXISTS play_development_panel;

CREATE TABLE play_development_panel (
    child_id INTEGER NOT NULL,
    context_id INTEGER NOT NULL,
    time INTEGER NOT NULL,
    baseline_development REAL,
    pretend_play_base REAL,
    social_play_base REAL,
    constructive_play_base REAL,
    outdoor_play_base REAL,
    caregiver_support_base REAL,
    chronic_stress INTEGER,
    play_space_quality REAL,
    adult_responsiveness REAL,
    inclusion_climate REAL,
    outdoor_safety REAL,
    play_material_access REAL,
    current_pretend REAL,
    current_social_play REAL,
    current_constructive REAL,
    current_outdoor REAL,
    current_support REAL,
    current_stress REAL,
    play_restriction REAL,
    peer_inclusion REAL,
    play_support_context REAL,
    development_score REAL,
    play_profile TEXT,
    PRIMARY KEY (child_id, time)
);

CREATE INDEX idx_play_context ON play_development_panel (context_id);
CREATE INDEX idx_play_time ON play_development_panel (time);
CREATE INDEX idx_play_profile ON play_development_panel (play_profile);
CREATE INDEX idx_play_stress ON play_development_panel (chronic_stress);
