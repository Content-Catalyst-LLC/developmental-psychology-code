DROP TABLE IF EXISTS adult_development_life_stages_panel;

CREATE TABLE adult_development_life_stages_panel (
    id INTEGER NOT NULL,
    context_id INTEGER NOT NULL,
    time INTEGER NOT NULL,
    baseline_adjustment REAL,
    life_stage TEXT,
    relational_support REAL,
    work_integration REAL,
    health_burden REAL,
    adaptive_resources REAL,
    role_burden REAL,
    institutional_support REAL,
    community_stability REAL,
    current_relational_support REAL,
    current_work_integration REAL,
    current_health_burden REAL,
    current_adaptive_resources REAL,
    current_role_burden REAL,
    young_stage INTEGER,
    midlife_stage INTEGER,
    later_stage INTEGER,
    adjustment_score REAL,
    adult_development_profile TEXT,
    PRIMARY KEY (id, time)
);

CREATE INDEX idx_adult_context ON adult_development_life_stages_panel (context_id);
CREATE INDEX idx_adult_time ON adult_development_life_stages_panel (time);
CREATE INDEX idx_adult_stage ON adult_development_life_stages_panel (life_stage);
CREATE INDEX idx_adult_profile ON adult_development_life_stages_panel (adult_development_profile);
