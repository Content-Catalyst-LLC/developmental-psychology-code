-- Article-level synthetic developmental psychology schema.

CREATE TABLE IF NOT EXISTS developmental_observations (
    observation_id INTEGER PRIMARY KEY,
    participant_id TEXT NOT NULL,
    wave INTEGER NOT NULL,
    age_years REAL,
    caregiving_support REAL,
    educational_opportunity REAL,
    self_regulation REAL,
    resilience_support REAL,
    cumulative_risk REAL,
    developmental_functioning REAL
);

CREATE INDEX IF NOT EXISTS idx_developmental_observations_participant
ON developmental_observations(participant_id);

CREATE INDEX IF NOT EXISTS idx_developmental_observations_wave
ON developmental_observations(wave);

CREATE INDEX IF NOT EXISTS idx_developmental_observations_age
ON developmental_observations(age_years);
