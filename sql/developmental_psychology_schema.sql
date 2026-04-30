-- Root schema for developmental psychology longitudinal and lifespan data.

CREATE TABLE IF NOT EXISTS participants (
    participant_id TEXT PRIMARY KEY,
    birth_cohort INTEGER,
    age_years REAL,
    language_background TEXT,
    developmental_context TEXT,
    notes TEXT
);

CREATE TABLE IF NOT EXISTS studies (
    study_id TEXT PRIMARY KEY,
    study_name TEXT NOT NULL,
    article_slug TEXT NOT NULL,
    description TEXT
);

CREATE TABLE IF NOT EXISTS repeated_observations (
    observation_id INTEGER PRIMARY KEY,
    participant_id TEXT NOT NULL,
    study_id TEXT NOT NULL,
    wave INTEGER NOT NULL,
    age_years REAL,
    caregiving_support REAL,
    educational_opportunity REAL,
    self_regulation REAL,
    resilience_support REAL,
    cumulative_risk REAL,
    developmental_functioning REAL,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);
