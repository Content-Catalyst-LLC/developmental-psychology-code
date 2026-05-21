DROP TABLE IF EXISTS wisdom_meaning_later_life_panel;

CREATE TABLE wisdom_meaning_later_life_panel (
    id INTEGER NOT NULL,
    care_context_id INTEGER NOT NULL,
    time INTEGER NOT NULL,
    baseline_meaning REAL,
    social_connection REAL,
    reflective_integration REAL,
    health_burden REAL,
    adaptive_support REAL,
    legacy_orientation REAL,
    dignity_support REAL,
    service_access REAL,
    community_participation REAL,
    current_connection REAL,
    current_reflection REAL,
    current_health REAL,
    current_support REAL,
    current_legacy REAL,
    wisdom_index REAL,
    meaning_score REAL,
    meaning_profile TEXT,
    PRIMARY KEY (id, time)
);

CREATE INDEX idx_wisdom_context ON wisdom_meaning_later_life_panel (care_context_id);
CREATE INDEX idx_wisdom_time ON wisdom_meaning_later_life_panel (time);
CREATE INDEX idx_wisdom_profile ON wisdom_meaning_later_life_panel (meaning_profile);
