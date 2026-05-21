-- Schema for synthetic trauma/adversity life-course panel data.

DROP TABLE IF EXISTS trauma_life_course_panel;

CREATE TABLE trauma_life_course_panel (
    child_id INTEGER NOT NULL,
    context_id INTEGER NOT NULL,
    time INTEGER NOT NULL,
    adversity_burden REAL,
    caregiver_support REAL,
    contextual_stability REAL,
    baseline_health REAL,
    child_resilience REAL,
    community_buffer REAL,
    institutional_safety REAL,
    service_access REAL,
    current_adversity REAL,
    current_support REAL,
    current_stability REAL,
    current_health REAL,
    early_timing_weight REAL,
    transition_weight REAL,
    weighted_adversity REAL,
    transition_support REAL,
    cumulative_adversity REAL,
    cumulative_support REAL,
    adaptation_score REAL,
    adversity_support_profile TEXT,
    PRIMARY KEY (child_id, time)
);

CREATE INDEX idx_trauma_panel_context
ON trauma_life_course_panel (context_id);

CREATE INDEX idx_trauma_panel_time
ON trauma_life_course_panel (time);

CREATE INDEX idx_trauma_panel_profile
ON trauma_life_course_panel (adversity_support_profile);
