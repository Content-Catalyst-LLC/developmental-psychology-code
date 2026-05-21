DROP TABLE IF EXISTS life_course_inequality_panel;

CREATE TABLE life_course_inequality_panel (
    person_id INTEGER NOT NULL,
    context_id INTEGER NOT NULL,
    time INTEGER NOT NULL,
    current_resources REAL,
    current_burden REAL,
    current_support REAL,
    health_status REAL,
    community_opportunity REAL,
    institutional_support REAL,
    environmental_safety REAL,
    cumulative_resources REAL,
    cumulative_burden REAL,
    development_score REAL,
    inequality_profile TEXT,
    PRIMARY KEY (person_id, time)
);

CREATE INDEX idx_life_course_context ON life_course_inequality_panel (context_id);
CREATE INDEX idx_life_course_time ON life_course_inequality_panel (time);
CREATE INDEX idx_life_course_profile ON life_course_inequality_panel (inequality_profile);
