-- Schema for synthetic culture and development panel data.

DROP TABLE IF EXISTS cultural_development_panel;

CREATE TABLE cultural_development_panel (
    child_id INTEGER NOT NULL,
    society_id INTEGER NOT NULL,
    time INTEGER NOT NULL,
    family_orientation REAL,
    institutional_fit REAL,
    cross_context_mismatch REAL,
    social_support REAL,
    bicultural_flexibility REAL,
    child_resilience REAL,
    society_climate REAL,
    institutional_inclusion REAL,
    linguistic_support REAL,
    pluralism_index REAL,
    current_family REAL,
    current_fit REAL,
    current_mismatch REAL,
    current_support REAL,
    current_flexibility REAL,
    development_score REAL,
    cultural_condition TEXT,
    PRIMARY KEY (child_id, time)
);

CREATE INDEX idx_cultural_panel_society
ON cultural_development_panel (society_id);

CREATE INDEX idx_cultural_panel_time
ON cultural_development_panel (time);

CREATE INDEX idx_cultural_panel_condition
ON cultural_development_panel (cultural_condition);
