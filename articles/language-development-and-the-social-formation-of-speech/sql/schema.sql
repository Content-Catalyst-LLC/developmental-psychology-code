DROP TABLE IF EXISTS language_development_panel;

CREATE TABLE language_development_panel (
    child_id INTEGER NOT NULL,
    context_id INTEGER NOT NULL,
    time INTEGER NOT NULL,
    baseline_language REAL,
    responsive_interaction REAL,
    shared_reading REAL,
    joint_attention REAL,
    conversational_turns REAL,
    hearing_support REAL,
    multilingual_exposure INTEGER,
    chronic_stress INTEGER,
    language_ecology_support REAL,
    book_access REAL,
    early_education_quality REAL,
    home_language_recognition REAL,
    current_interaction REAL,
    current_reading REAL,
    current_joint_attention REAL,
    current_turn_taking REAL,
    current_stress REAL,
    language_support_context REAL,
    language_score REAL,
    language_profile TEXT,
    PRIMARY KEY (child_id, time)
);

CREATE INDEX idx_language_context ON language_development_panel (context_id);
CREATE INDEX idx_language_time ON language_development_panel (time);
CREATE INDEX idx_language_profile ON language_development_panel (language_profile);
CREATE INDEX idx_language_stress ON language_development_panel (chronic_stress);
CREATE INDEX idx_language_multilingual ON language_development_panel (multilingual_exposure);
