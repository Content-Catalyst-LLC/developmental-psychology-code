DROP TABLE IF EXISTS schooling_development_panel;

CREATE TABLE schooling_development_panel (
    student_id INTEGER NOT NULL,
    school_id INTEGER NOT NULL,
    time INTEGER NOT NULL,
    baseline_teacher_support REAL,
    baseline_peer_belonging REAL,
    baseline_school_stress REAL,
    family_support REAL,
    academic_confidence REAL,
    intervention INTEGER,
    school_climate REAL,
    curriculum_opportunity REAL,
    restorative_practice REAL,
    resource_capacity REAL,
    current_teacher REAL,
    current_peer REAL,
    current_stress REAL,
    current_family REAL,
    current_confidence REAL,
    connectedness_score REAL,
    development_score REAL,
    school_support_profile TEXT,
    PRIMARY KEY (student_id, time)
);

CREATE INDEX idx_schooling_school ON schooling_development_panel (school_id);
CREATE INDEX idx_schooling_time ON schooling_development_panel (time);
CREATE INDEX idx_schooling_profile ON schooling_development_panel (school_support_profile);
CREATE INDEX idx_schooling_intervention ON schooling_development_panel (intervention);
