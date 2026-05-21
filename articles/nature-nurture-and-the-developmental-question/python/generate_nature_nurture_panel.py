#!/usr/bin/env python3
"""Generate synthetic nature-nurture developmental panel data.

The data represent a teaching/research scaffold for modeling development as an
interaction among biological sensitivity, structural risk, caregiver support,
acute stress, institutional support, disability support, resource stability,
intervention exposure, and protective context.
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


def generate_panel(
    n_children: int = 900,
    n_periods: int = 10,
    n_schools: int = 36,
    seed: int = 2026,
) -> pd.DataFrame:
    rng = np.random.default_rng(seed)

    children = pd.DataFrame({
        "child_id": np.arange(1, n_children + 1),
        "school_id": rng.integers(1, n_schools + 1, n_children),
        "biological_sensitivity": rng.normal(0, 1, n_children),
        "baseline_functioning": rng.normal(50, 7, n_children),
        "structural_risk": rng.binomial(1, 0.35, n_children),
        "chronic_adversity": rng.binomial(1, 0.32, n_children),
        "family_support_context": rng.normal(0, 1, n_children),
    })

    schools = pd.DataFrame({
        "school_id": np.arange(1, n_schools + 1),
        "institutional_support": rng.normal(0, 0.7, n_schools),
        "disability_support": rng.normal(0, 0.6, n_schools),
        "resource_stability": rng.normal(0, 0.5, n_schools),
    })

    panel = children.loc[children.index.repeat(n_periods)].copy()
    panel["time"] = np.tile(np.arange(n_periods), n_children)
    panel = panel.merge(schools, on="school_id", how="left")

    panel["caregiver_support"] = rng.normal(
        loc=0.4 + panel["family_support_context"] - 0.5 * panel["structural_risk"],
        scale=0.9,
    )

    panel["acute_stress"] = rng.normal(
        loc=0.3 * panel["structural_risk"] + 0.35 * panel["chronic_adversity"],
        scale=0.8,
    )

    panel["intervention"] = (
        (panel["time"] >= 5) & (rng.uniform(size=len(panel)) < 0.28)
    ).astype(int)

    panel["protective_context"] = (
        panel["caregiver_support"]
        + panel["institutional_support"]
        + panel["disability_support"]
        + panel["resource_stability"]
        + panel["intervention"]
    )

    panel = panel.sort_values(["child_id", "time"]).reset_index(drop=True)
    panel["development_score"] = np.nan

    for _, rows in panel.groupby("child_id", sort=False):
        previous_score = rows["baseline_functioning"].iloc[0]

        for idx in rows.index:
            bio = panel.at[idx, "biological_sensitivity"]
            support = panel.at[idx, "caregiver_support"]
            stress = panel.at[idx, "acute_stress"]
            risk = panel.at[idx, "structural_risk"]
            adversity = panel.at[idx, "chronic_adversity"]
            institution = panel.at[idx, "institutional_support"]
            disability_support = panel.at[idx, "disability_support"]
            resource_stability = panel.at[idx, "resource_stability"]
            intervention = panel.at[idx, "intervention"]
            protective_context = panel.at[idx, "protective_context"]
            time = panel.at[idx, "time"]

            current_score = (
                0.70 * previous_score
                + 0.90 * time
                + 1.20 * support
                - 1.40 * stress
                - 2.20 * risk
                - 1.80 * adversity
                + 0.95 * institution
                + 0.85 * disability_support
                + 0.70 * resource_stability
                + 1.60 * intervention
                + 1.00 * bio * support
                - 0.90 * bio * stress
                + 0.65 * bio * protective_context
                + rng.normal(0, 2.6)
            )

            panel.at[idx, "development_score"] = current_score
            previous_score = current_score

    profile = panel.groupby("child_id", as_index=False).agg(
        average_protective_context=("protective_context", "mean"),
        average_stress=("acute_stress", "mean"),
        average_development=("development_score", "mean"),
        final_development=("development_score", "last"),
        biological_sensitivity=("biological_sensitivity", "first"),
        structural_risk=("structural_risk", "first"),
        chronic_adversity=("chronic_adversity", "first"),
    )

    sensitivity_median = profile["biological_sensitivity"].median()
    protection_median = profile["average_protective_context"].median()

    profile["sensitivity_profile"] = np.select(
        [
            (profile["biological_sensitivity"] >= sensitivity_median) & (profile["average_protective_context"] >= protection_median),
            (profile["biological_sensitivity"] >= sensitivity_median) & (profile["average_protective_context"] < protection_median),
            (profile["biological_sensitivity"] < sensitivity_median) & (profile["average_protective_context"] >= protection_median),
        ],
        [
            "higher_sensitivity_higher_protection",
            "higher_sensitivity_lower_protection",
            "lower_sensitivity_higher_protection",
        ],
        default="lower_sensitivity_lower_protection",
    )

    panel = panel.merge(profile[["child_id", "sensitivity_profile"]], on="child_id", how="left")

    schools.to_csv(DATA_DIR / "school_context_metadata.csv", index=False)
    profile.to_csv(DATA_DIR / "nature_nurture_child_profiles.csv", index=False)
    return panel


def main() -> None:
    panel = generate_panel()
    panel_path = DATA_DIR / "nature_nurture_development_panel.csv"
    panel.to_csv(panel_path, index=False)

    trajectory = panel.groupby(["time", "structural_risk"], as_index=False).agg(
        average_development=("development_score", "mean"),
        average_support=("caregiver_support", "mean"),
        average_stress=("acute_stress", "mean"),
        average_protective_context=("protective_context", "mean"),
        average_intervention=("intervention", "mean"),
    )
    trajectory.to_csv(OUTPUTS_DIR / "generated_nature_nurture_trajectory.csv", index=False)

    print(f"Wrote {panel_path}")
    print(f"Rows: {len(panel):,}")
    print(f"Children: {panel['child_id'].nunique():,}")
    print(f"Schools: {panel['school_id'].nunique():,}")


if __name__ == "__main__":
    main()
