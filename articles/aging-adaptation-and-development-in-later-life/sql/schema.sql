DROP TABLE IF EXISTS aging_adaptation_later_life_panel;

CREATE TABLE aging_adaptation_later_life_panel (
    id INTEGER NOT NULL,
    care_context_id INTEGER NOT NULL,
    time INTEGER NOT NULL,
    baseline_adjustment REAL,
    functional_ability REAL,
    social_support REAL,
    health_burden REAL,
    adaptive_strategy REAL,
    meaning_orientation REAL,
    environmental_accessibility REAL,
    dignity_support REAL,
    service_access REAL,
    current_function REAL,
    current_support REAL,
    current_health REAL,
    current_adaptation REAL,
    current_meaning REAL,
    functional_fit REAL,
    adjustment_score REAL,
    adaptation_profile TEXT,
    PRIMARY KEY (id, time)
);

CREATE INDEX idx_aging_context ON aging_adaptation_later_life_panel (care_context_id);
CREATE INDEX idx_aging_time ON aging_adaptation_later_life_panel (time);
CREATE INDEX idx_aging_profile ON aging_adaptation_later_life_panel (adaptation_profile);
