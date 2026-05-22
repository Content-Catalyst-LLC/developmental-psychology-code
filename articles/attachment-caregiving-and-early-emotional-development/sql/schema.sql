DROP TABLE IF EXISTS attachment_development_panel;

CREATE TABLE attachment_development_panel (
    child_id INTEGER NOT NULL,
    context_id INTEGER NOT NULL,
    time INTEGER NOT NULL,
    baseline_regulation REAL,
    caregiving_quality REAL,
    repair_capacity REAL,
    caregiver_support REAL,
    temperament_reactivity REAL,
    disability_support_need INTEGER,
    chronic_stress INTEGER,
    childcare_continuity REAL,
    neighborhood_safety REAL,
    family_service_access REAL,
    caregiving_ecology_support REAL,
    current_care REAL,
    current_repair REAL,
    current_caregiver_support REAL,
    current_stress REAL,
    caregiving_support_context REAL,
    regulation_score REAL,
    attachment_profile TEXT,
    PRIMARY KEY (child_id, time)
);

CREATE INDEX idx_attachment_context ON attachment_development_panel (context_id);
CREATE INDEX idx_attachment_time ON attachment_development_panel (time);
CREATE INDEX idx_attachment_profile ON attachment_development_panel (attachment_profile);
CREATE INDEX idx_attachment_stress ON attachment_development_panel (chronic_stress);
