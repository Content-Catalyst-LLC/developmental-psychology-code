DROP TABLE IF EXISTS prenatal_development_foundations_panel;

CREATE TABLE prenatal_development_foundations_panel (
    case_id INTEGER PRIMARY KEY,
    neighborhood_context INTEGER NOT NULL,
    gestational_weeks REAL,
    maternal_health REAL,
    prenatal_care REAL,
    chronic_stress REAL,
    toxic_exposure REAL,
    nutrition_support REAL,
    social_support REAL,
    healthcare_access REAL,
    environmental_burden REAL,
    economic_security REAL,
    effective_care REAL,
    developmental_risk REAL,
    early_outcome REAL,
    prenatal_profile TEXT
);

CREATE INDEX idx_prenatal_neighborhood ON prenatal_development_foundations_panel (neighborhood_context);
CREATE INDEX idx_prenatal_profile ON prenatal_development_foundations_panel (prenatal_profile);
CREATE INDEX idx_prenatal_care ON prenatal_development_foundations_panel (effective_care);
CREATE INDEX idx_prenatal_risk ON prenatal_development_foundations_panel (developmental_risk);
