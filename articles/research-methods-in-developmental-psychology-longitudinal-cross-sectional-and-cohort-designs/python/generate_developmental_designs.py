#!/usr/bin/env python3
"""Generate synthetic data for developmental research design comparisons.

The generated data demonstrate cross-sectional, longitudinal, cohort, and
cohort-sequential design logic. The data are synthetic and do not represent
real people, schools, clinics, or populations.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
OUTPUTS_DIR = ROOT / "outputs"

DATA_DIR.mkdir(parents=True, exist_ok=True)
OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)


def generate_design_panel(
    n_people: int = 1200,
    n_waves: int = 6,
    n_contexts: int = 30,
    seed: int = 2026,
) -> pd.DataFrame:
    rng = np.random.default_rng(seed)

    cohort_groups = np.array([2006, 2009, 2012, 2015])
    cohort_start_age = {2006: 14, 2009: 11, 2012: 8, 2015: 5}

    people = pd.DataFrame(
        {
            "person_id": np.arange(1, n_people + 1),
            "context_id": rng.integers(1, n_contexts + 1, n_people),
            "birth_cohort": rng.choice(cohort_groups, size=n_people),
            "baseline_trait": rng.normal(0, 1, n_people),
            "baseline_support": rng.normal(0, 1, n_people),
            "baseline_risk": rng.normal(0, 1, n_people),
        }
    )

    contexts = pd.DataFrame(
        {
            "context_id": np.arange(1, n_contexts + 1),
            "context_quality": rng.normal(0, 0.65, n_contexts),
        }
    )

    people["start_age"] = people["birth_cohort"].map(cohort_start_age)

    panel = people.loc[people.index.repeat(n_waves)].copy()
    panel["study_wave"] = np.tile(np.arange(n_waves), n_people)
    panel["period"] = 2026 + panel["study_wave"]
    panel["age"] = panel["start_age"] + panel["study_wave"]
    panel = panel.merge(contexts, on="context_id", how="left")

    cohort_effect_map = {
        2006: 0.40,
        2009: 0.10,
        2012: -0.10,
        2015: -0.30,
    }
    panel["cohort_effect"] = panel["birth_cohort"].map(cohort_effect_map)
    panel["period_effect"] = 0.08 * (panel["period"] - panel["period"].min())

    panel["support"] = rng.normal(
        panel["baseline_support"] + 0.25 * panel["context_quality"],
        0.65,
    )
    panel["risk"] = rng.normal(panel["baseline_risk"], 0.70)

    centered_age = panel["age"] - panel["age"].mean()
    developmental_curve = (
        0.95 * centered_age
        - 0.035 * centered_age**2
    )

    panel["development_score"] = (
        50
        + developmental_curve
        + 1.15 * panel["support"]
        - 1.20 * panel["risk"]
        + 1.00 * panel["baseline_trait"]
        + 0.90 * panel["context_quality"]
        + 1.25 * panel["cohort_effect"]
        + 0.75 * panel["period_effect"]
        + rng.normal(0, 2.2, len(panel))
    )

    # Attrition / missingness is more likely under higher risk and later waves.
    attrition_logit = (
        -2.0
        + 0.22 * panel["study_wave"]
        + 0.25 * panel["risk"]
        - 0.20 * panel["support"]
    )
    attrition_probability = 1 / (1 + np.exp(-attrition_logit))
    panel["observed"] = (rng.random(len(panel)) > attrition_probability).astype(int)

    panel = panel.sort_values(["person_id", "study_wave"]).reset_index(drop=True)
    return panel


def main() -> None:
    panel = generate_design_panel()

    panel_path = DATA_DIR / "developmental_design_panel.csv"
    panel.to_csv(panel_path, index=False)

    # Cross-sectional sample from first study period.
    cross_section = panel.loc[panel["period"] == panel["period"].min()].copy()
    cross_section.to_csv(DATA_DIR / "cross_sectional_sample.csv", index=False)

    cohort_summary = panel.groupby(["birth_cohort", "study_wave"], as_index=False).agg(
        mean_age=("age", "mean"),
        mean_development_score=("development_score", "mean"),
        observation_rate=("observed", "mean"),
        people=("person_id", "nunique"),
    )
    cohort_summary.to_csv(DATA_DIR / "cohort_summary.csv", index=False)

    missingness = panel.groupby("study_wave", as_index=False).agg(
        observation_rate=("observed", "mean"),
        observations=("observed", "sum"),
        possible_observations=("observed", "count"),
    )
    missingness.to_csv(OUTPUTS_DIR / "generated_missingness_by_wave.csv", index=False)

    print(f"Wrote {panel_path}")
    print(f"Rows: {len(panel):,}")
    print(f"People: {panel['person_id'].nunique():,}")
    print(f"Cohorts: {panel['birth_cohort'].nunique():,}")
    print(f"Contexts: {panel['context_id'].nunique():,}")


if __name__ == "__main__":
    main()
