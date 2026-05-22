DROP TABLE IF EXISTS moral_development_panel;

CREATE TABLE moral_development_panel (
    child_id INTEGER NOT NULL,
    school_id INTEGER NOT NULL,
    time INTEGER NOT NULL,
    baseline_morality REAL,
    caregiving_guidance REAL,
    empathic_sensitivity REAL,
    peer_fairness_base REAL,
    self_regulation REAL,
    harm_recognition_base REAL,
    chronic_exclusion INTEGER,
    school_moral_climate REAL,
    restorative_practice_access REAL,
    punitive_inconsistency REAL,
    anti_bullying_climate REAL,
    digital_moral_safety REAL,
    current_guidance REAL,
    current_empathy REAL,
    current_peer_fairness REAL,
    current_self_regulation REAL,
    current_harm_recognition REAL,
    current_repair_opportunity REAL,
    current_exclusion REAL,
    digital_cruelty_exposure REAL,
    peer_pressure REAL,
    moral_support_context REAL,
    conscience_score REAL,
    moral_action_score REAL,
    moral_profile TEXT,
    PRIMARY KEY (child_id, time)
);

CREATE INDEX idx_moral_school ON moral_development_panel (school_id);
CREATE INDEX idx_moral_time ON moral_development_panel (time);
CREATE INDEX idx_moral_profile ON moral_development_panel (moral_profile);
CREATE INDEX idx_moral_exclusion ON moral_development_panel (chronic_exclusion);
