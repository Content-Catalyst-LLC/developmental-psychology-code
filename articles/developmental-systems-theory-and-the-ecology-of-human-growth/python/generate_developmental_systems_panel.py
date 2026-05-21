#!/usr/bin/env python3
"""Generate synthetic developmental systems panel data.

The data represent a teaching/research scaffold for modeling development as
nested person-context coaction among biological sensitivity, family support,
peer belonging, school climate, curriculum opportunity, neighborhood safety,
service access, material security, ecological stress, and intervention exposure.
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
    n_children: int = 850,
    n_periods: int = 10,
    n_schools: int = 36,
    n_neighborhoods: int = 24,
    seed: int = 2026,
) -> pd.DataFrame:
    rng = np.random.default_rng(seed)

    children = pd.DataFrame({
        "child_id": np.arange(1, n_children + 1),
        "school_id": rng.integers(1, n_schools + 1, n_children),
        "neighborhood_id": rng.integers(1, n_neighborhoods + 1, n_children),
        "biological_sensitivity": rng.normal(0, 1, n_children),
        "family_support": rng.normal(0, 1, n_children),
        "peer_belonging": rng.normal(0, 0.8, n_children),
        "intervention_exposure": rng.binomial(1, 0.35, n_children),
    })

    schools = pd.DataFrame({
        "school_id": np.arange(1, n_schools + 1),
        "school_climate": rng.normal(0, 0.6, n_schools),
        "curriculum_opportunity": rng.normal(0, 0.5, n_schools),
    })

    neighborhoods = pd.DataFrame({
        "neighborhood_id": np.arange(1, n_neighborhoods + 1),
        "neighborhood_safety": rng.normal(0, 0.6, n_neighborhoods),
        "service_access": rng.normal(0, 0.5, n_neighborhoods),
        "material_security": rng.normal(0, 0.5, n_neighborhoods),
    })

    panel = children.loc[children.index.repeat(n_periods)].copy()
    panel["time"] = np.tile(np.arange(n_periods), n_children)

    panel = (
        panel
        .merge(schools, on="school_id", how="left")
        .merge(neighborhoods, on="neighborhood_id", how="left")
    )

    panel["current_family"] = rng.normal(panel["family_support"], 0.60)
    panel["current_peer"] = rng.normal(panel["peer_belonging"], 0.60)

    panel["ecological_support"] = (
        panel["current_family"]
        + panel["current_peer"]
        + panel["school_climate"]
        + panel["curriculum_opportunity"]
        + panel["neighborhood_safety"]
        + panel["service_access"]
        + panel["material_security"]
    )

    panel["ecological_stress"] = rng.normal(
        -0.25 * panel["current_family"]
        - 0.20 * panel["school_climate"]
        - 0.20 * panel["neighborhood_safety"]
        - 0.15 * panel["material_security"],
        0.70,
    )

    panel = panel.sort_values(["child_id", "time"]).reset_index(drop=True)
    panel["development_score"] = np.nan

    for _, rows in panel.groupby("child_id", sort=False):
        previous_score = 50 + rng.normal(0, 3)

        for idx in rows.index:
            bio = panel.at[idx, "biological_sensitivity"]
            family = panel.at[idx, "current_family"]
            peer = panel.at[idx, "current_peer"]
            climate = panel.at[idx, "school_climate"]
            curriculum = panel.at[idx, "curriculum_opportunity"]
            safety = panel.at[idx, "neighborhood_safety"]
            services = panel.at[idx, "service_access"]
            security = panel.at[idx, "material_security"]
            intervention = panel.at[idx, "intervention_exposure"]
            stress = panel.at[idx, "ecological_stress"]
            time = panel.at[idx, "time"]

            current_score = (
                0.70 * previous_score
                + 0.24 * time
                + 0.85 * bio
                + 1.15 * family
                + 0.95 * peer
                + 0.95 * climate
                + 0.80 * curriculum
                + 0.85 * safety
                + 0.70 * services
                + 0.65 * security
                + 0.90 * intervention
                - 1.10 * stress
                + 0.45 * bio * family
                - 0.35 * bio * stress
                + rng.normal(0, 2.3)
            )

            panel.at[idx, "development_score"] = current_score
            previous_score = current_score

    child_summary = panel.groupby("child_id", as_index=False).agg(
        average_ecological_support=("ecological_support", "mean"),
        average_ecological_stress=("ecological_stress", "mean"),
        average_family=("current_family", "mean"),
        average_peer=("current_peer", "mean"),
        final_development=("development_score", "last"),
    )

    child_summary["ecological_support_profile"] = np.select(
        [
            (child_summary["average_ecological_support"] >= 0) & (child_summary["average_ecological_stress"] < 0),
            (child_summary["average_ecological_support"] >= 0) & (child_summary["average_ecological_stress"] >= 0),
            (child_summary["average_ecological_support"] < 0) & (child_summary["average_ecological_stress"] < 0),
        ],
        [
            "higher_support_lower_stress",
            "higher_support_higher_stress",
            "lower_support_lower_stress",
        ],
        default="lower_support_higher_stress",
    )

    panel = panel.merge(
        child_summary[["child_id", "ecological_support_profile"]],
        on="child_id",
        how="left",
    )

    schools.to_csv(DATA_DIR / "school_metadata.csv", index=False)
    neighborhoods.to_csv(DATA_DIR / "neighborhood_metadata.csv", index=False)
    child_summary.to_csv(DATA_DIR / "child_systems_profiles.csv", index=False)
    return panel


def main() -> None:
    panel = generate_panel()
    panel_path = DATA_DIR / "developmental_systems_panel.csv"
    panel.to_csv(panel_path, index=False)

    trajectory = panel.groupby("time", as_index=False).agg(
        average_development=("development_score", "mean"),
        average_ecological_support=("ecological_support", "mean"),
        average_ecological_stress=("ecological_stress", "mean"),
        average_family=("current_family", "mean"),
        average_peer=("current_peer", "mean"),
    )
    trajectory.to_csv(OUTPUTS_DIR / "generated_developmental_systems_trajectory.csv", index=False)

    print(f"Wrote {panel_path}")
    print(f"Rows: {len(panel):,}")
    print(f"Children: {panel['child_id'].nunique():,}")
    print(f"Schools: {panel['school_id'].nunique():,}")
    print(f"Neighborhoods: {panel['neighborhood_id'].nunique():,}")


if __name__ == "__main__":
    main()
