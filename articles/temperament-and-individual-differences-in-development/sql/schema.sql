DROP TABLE IF EXISTS temperament_individual_differences_panel;

CREATE TABLE temperament_individual_differences_panel (
    child_id INTEGER NOT NULL,
    classroom_id INTEGER NOT NULL,
    time INTEGER NOT NULL,
    temperament_reactivity REAL,
    inhibition REAL,
    activity_level REAL,
    baseline_adjustment REAL,
    chronic_stress INTEGER,
    family_support REAL,
    school_fit REAL,
    classroom_structure REAL,
    teacher_responsiveness REAL,
    movement_flexibility REAL,
    current_support REAL,
    current_school_fit REAL,
    acute_stress REAL,
    current_accommodation REAL,
    goodness_of_fit REAL,
    adjustment_score REAL,
    temperament_profile TEXT,
    PRIMARY KEY (child_id, time)
);

CREATE INDEX idx_temperament_classroom ON temperament_individual_differences_panel (classroom_id);
CREATE INDEX idx_temperament_time ON temperament_individual_differences_panel (time);
CREATE INDEX idx_temperament_profile ON temperament_individual_differences_panel (temperament_profile);
