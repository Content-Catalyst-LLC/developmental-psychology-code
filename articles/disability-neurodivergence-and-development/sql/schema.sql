DROP TABLE IF EXISTS disability_neurodivergence_panel;

CREATE TABLE disability_neurodivergence_panel (
    child_id INTEGER NOT NULL,
    setting_id INTEGER NOT NULL,
    time INTEGER NOT NULL,
    neuro_profile REAL,
    support_quality REAL,
    accessibility REAL,
    barrier_burden REAL,
    caregiver_advocacy REAL,
    communication_access REAL,
    inclusion_climate REAL,
    service_access REAL,
    sensory_flexibility REAL,
    current_support REAL,
    current_access REAL,
    current_barrier REAL,
    current_communication REAL,
    current_advocacy REAL,
    participation_score REAL,
    development_score REAL,
    access_condition TEXT,
    PRIMARY KEY (child_id, time)
);

CREATE INDEX idx_accessibility_setting ON disability_neurodivergence_panel (setting_id);
CREATE INDEX idx_accessibility_time ON disability_neurodivergence_panel (time);
CREATE INDEX idx_accessibility_condition ON disability_neurodivergence_panel (access_condition);
