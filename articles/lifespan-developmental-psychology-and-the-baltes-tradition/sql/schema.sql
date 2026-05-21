DROP TABLE IF EXISTS lifespan_baltes_panel;

CREATE TABLE lifespan_baltes_panel (
    id INTEGER NOT NULL,
    cohort_id INTEGER NOT NULL,
    time INTEGER NOT NULL,
    baseline_dev REAL,
    plasticity REAL,
    context_support REAL,
    comp_capacity REAL,
    health_resource REAL,
    historical_support REAL,
    institutional_security REAL,
    gains REAL,
    losses REAL,
    current_support REAL,
    current_comp REAL,
    selection REAL,
    optimization REAL,
    compensation REAL,
    soc_index REAL,
    development_score REAL,
    adaptation_profile TEXT,
    PRIMARY KEY (id, time)
);

CREATE INDEX idx_lifespan_cohort ON lifespan_baltes_panel (cohort_id);
CREATE INDEX idx_lifespan_time ON lifespan_baltes_panel (time);
CREATE INDEX idx_lifespan_profile ON lifespan_baltes_panel (adaptation_profile);
