DROP TABLE IF EXISTS developmental_psychology_history_panel;

CREATE TABLE developmental_psychology_history_panel (
    year INTEGER PRIMARY KEY,
    child_study REAL,
    maturational REAL,
    psychoanalytic REAL,
    behaviorist REAL,
    cognitive_developmental REAL,
    sociocultural REAL,
    attachment_social REAL,
    ecological REAL,
    lifespan REAL,
    developmental_psychopathology REAL,
    neuroscience_genetics REAL,
    developmental_systems REAL,
    institutional_support REAL,
    methodological_advantage REAL,
    social_relevance REAL,
    critique_index REAL,
    child_centered_index REAL,
    lifespan_index REAL,
    ecological_systems_index REAL,
    broadening_index REAL
);

CREATE INDEX idx_devhist_year ON developmental_psychology_history_panel (year);
CREATE INDEX idx_devhist_broadening ON developmental_psychology_history_panel (broadening_index);
CREATE INDEX idx_devhist_lifespan ON developmental_psychology_history_panel (lifespan_index);
