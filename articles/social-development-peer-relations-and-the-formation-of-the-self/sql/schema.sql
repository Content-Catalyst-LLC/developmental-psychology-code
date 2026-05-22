DROP TABLE IF EXISTS social_development_panel;

CREATE TABLE social_development_panel (
    child_id INTEGER NOT NULL,
    school_id INTEGER NOT NULL,
    time INTEGER NOT NULL,
    baseline_social REAL,
    peer_support_base REAL,
    friendship_quality_base REAL,
    family_support_base REAL,
    social_interpretation_skill REAL,
    chronic_exclusion INTEGER,
    school_connectedness REAL,
    teacher_support REAL,
    anti_bullying_climate REAL,
    inclusion_climate REAL,
    restorative_practice_access REAL,
    current_peer_support REAL,
    current_friendship_quality REAL,
    current_family_support REAL,
    current_social_interpretation REAL,
    current_exclusion REAL,
    bullying_exposure REAL,
    digital_comparison_stress REAL,
    social_support_context REAL,
    social_self_score REAL,
    social_profile TEXT,
    PRIMARY KEY (child_id, time)
);

CREATE INDEX idx_social_school ON social_development_panel (school_id);
CREATE INDEX idx_social_time ON social_development_panel (time);
CREATE INDEX idx_social_profile ON social_development_panel (social_profile);
CREATE INDEX idx_social_exclusion ON social_development_panel (chronic_exclusion);
