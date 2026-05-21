-- Schema for synthetic developmental psychology panel data.
-- Intended for SQLite, PostgreSQL adaptation, DuckDB, or teaching examples.

DROP TABLE IF EXISTS developmental_panel;

CREATE TABLE developmental_panel (
    person_id INTEGER NOT NULL,
    context_id INTEGER NOT NULL,
    time INTEGER NOT NULL,
    baseline_support REAL,
    baseline_risk REAL,
    baseline_policy_access REAL,
    baseline_health REAL,
    person_resilience REAL,
    institutional_climate REAL,
    resource_level REAL,
    current_support REAL,
    current_risk REAL,
    policy_access REAL,
    health_status REAL,
    development_score REAL,
    PRIMARY KEY (person_id, time)
);

CREATE INDEX idx_developmental_panel_context
ON developmental_panel (context_id);

CREATE INDEX idx_developmental_panel_time
ON developmental_panel (time);
