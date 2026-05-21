DROP TABLE IF EXISTS gender_sexual_development_panel;

CREATE TABLE gender_sexual_development_panel (
    id INTEGER NOT NULL,
    school_id INTEGER NOT NULL,
    time INTEGER NOT NULL,
    baseline_adjustment REAL,
    family_support REAL,
    social_recognition REAL,
    consent_knowledge REAL,
    school_connectedness REAL,
    chronic_stigma INTEGER,
    school_climate REAL,
    health_education_quality REAL,
    anti_harassment_support REAL,
    pubertal_progress REAL,
    current_family_support REAL,
    current_recognition REAL,
    current_consent_knowledge REAL,
    current_connectedness REAL,
    current_stigma REAL,
    protective_context REAL,
    adjustment_score REAL,
    development_profile TEXT,
    PRIMARY KEY (id, time)
);

CREATE INDEX idx_gender_sexual_school ON gender_sexual_development_panel (school_id);
CREATE INDEX idx_gender_sexual_time ON gender_sexual_development_panel (time);
CREATE INDEX idx_gender_sexual_profile ON gender_sexual_development_panel (development_profile);
CREATE INDEX idx_gender_sexual_stigma ON gender_sexual_development_panel (chronic_stigma);
