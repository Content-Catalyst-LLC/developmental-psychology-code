-- Schema for synthetic developmental timing-window panel data.

DROP TABLE IF EXISTS developmental_timing_panel;

CREATE TABLE developmental_timing_panel (
    person_id INTEGER NOT NULL,
    context_id INTEGER NOT NULL,
    time INTEGER NOT NULL,
    experience REAL,
    support REAL,
    adversity REAL,
    late_intervention REAL,
    critical_weight REAL,
    early_sensitive_weight REAL,
    adolescent_sensitive_weight REAL,
    residual_plasticity_weight REAL,
    cumulative_critical_exposure REAL,
    cumulative_sensitive_exposure REAL,
    critical_outcome REAL,
    sensitive_outcome REAL,
    multi_window_outcome REAL,
    recovery_outcome REAL,
    PRIMARY KEY (person_id, time)
);

CREATE INDEX idx_timing_panel_context
ON developmental_timing_panel (context_id);

CREATE INDEX idx_timing_panel_time
ON developmental_timing_panel (time);
