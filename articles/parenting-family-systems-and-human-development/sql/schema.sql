DROP TABLE IF EXISTS family_systems_panel;

CREATE TABLE family_systems_panel (
    child_id INTEGER NOT NULL,
    household_id INTEGER NOT NULL,
    time INTEGER NOT NULL,
    parenting_responsiveness REAL,
    family_climate REAL,
    external_stress REAL,
    sibling_support REAL,
    child_regulation REAL,
    caregiver_support INTEGER,
    household_stability REAL,
    kin_support REAL,
    economic_security REAL,
    current_parenting REAL,
    current_family REAL,
    current_stress REAL,
    current_sibling REAL,
    current_regulation REAL,
    family_support_index REAL,
    development_score REAL,
    family_support_profile TEXT,
    PRIMARY KEY (child_id, time)
);

CREATE INDEX idx_family_household ON family_systems_panel (household_id);
CREATE INDEX idx_family_time ON family_systems_panel (time);
CREATE INDEX idx_family_profile ON family_systems_panel (family_support_profile);
CREATE INDEX idx_family_support ON family_systems_panel (caregiver_support);
