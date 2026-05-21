#!/usr/bin/env python3
"""Generate synthetic genes-environment-plasticity panel data.

The data represent a teaching/research scaffold for modeling development as
coaction among biological sensitivity, care, stress, nutrition, timing,
school/neighborhood context, service access, biological embedding, and support.
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
    n_contexts: int = 38,
    seed: int = 2026,
) -> pd.DataFrame:
    rng = np.random.default_rng(seed)

    children = pd.DataFrame({
        "child_id": np.arange(1, n_children + 1),
        "context_id": rng.integers(1, n_contexts + 1, n_children),
        "bio_sensitivity": rng.normal(0, 1, n_children),
        "caregiving_quality": rng.normal(0, 1, n_children),
        "environmental_stress": rng.normal(0, 1, n_children),
        "nutritional_support": rng.normal(0, 0.8, n_children),
        "early_exposure": rng.binomial(1, 0.40, n_children),
        "intervention_support": rng.binomial(1, 0.35, n_children),
    })

    contexts = pd.DataFrame({
        "context_id": np.arange(1, n_contexts + 1),
        "school_support": rng.normal(0, 0.6, n_contexts),
        "neighborhood_safety": rng.normal(0, 0.6, n_contexts),
        "service_access": rng.normal(0, 0.5, n_contexts),
    })

    panel = children.loc[children.index.repeat(n_periods)].copy()
    panel["time"] = np.tile(np.arange(n_periods), n_children)
    panel["timing_weight"] = np.exp(-0.30 * panel["time"])
    panel = panel.merge(contexts, on="context_id", how="left")

    panel["current_care"] = rng.normal(panel["caregiving_quality"], 0.60)
    panel["current_stress"] = rng.normal(panel["environmental_stress"], 0.65)
    panel["current_nutrition"] = rng.normal(panel["nutritional_support"], 0.50)

    panel = panel.sort_values(["child_id", "time"]).reset_index(drop=True)

    panel["weighted_stress"] = panel["current_stress"] * panel["timing_weight"]
    panel["weighted_support"] = (
        panel["current_care"] +
        panel["current_nutrition"] +
        panel["school_support"]
    ) * panel["timing_weight"]

    panel["embedded_stress"] = (
        panel.groupby("child_id")["weighted_stress"].cumsum() /
        (panel["time"] + 1)
    )

    panel["embedded_support"] = (
        panel.groupby("child_id")["weighted_support"].cumsum() /
        (panel["time"] + 1)
    )

    panel["development_score"] = np.nan

    for _, rows in panel.groupby("child_id", sort=False):
        previous_score = 50 + rng.normal(0, 3)

        for idx in rows.index:
            bio = panel.at[idx, "bio_sensitivity"]
            care = panel.at[idx, "current_care"]
            stress = panel.at[idx, "current_stress"]
            nutrition = panel.at[idx, "current_nutrition"]
            early = panel.at[idx, "early_exposure"]
            timing = panel.at[idx, "timing_weight"]
            school = panel.at[idx, "school_support"]
            safety = panel.at[idx, "neighborhood_safety"]
            services = panel.at[idx, "service_access"]
            embedded_stress = panel.at[idx, "embedded_stress"]
            embedded_support = panel.at[idx, "embedded_support"]
            intervention = panel.at[idx, "intervention_support"]
            time = panel.at[idx, "time"]

            current_score = (
                0.70 * previous_score
                + 0.22 * time
                + 0.90 * bio
                + 1.10 * care
                - 1.05 * stress
                + 0.80 * nutrition
                + 0.75 * school
                + 0.65 * safety
                + 0.60 * services
                + 0.85 * early * timing
                + 0.85 * intervention
                + 0.95 * bio * care
                - 0.90 * bio * stress
                - 0.70 * embedded_stress
                + 0.60 * embedded_support
                + rng.normal(0, 2.3)
            )

            panel.at[idx, "development_score"] = current_score
            previous_score = current_score

    child_summary = panel.groupby("child_id", as_index=False).agg(
        biological_sensitivity=("bio_sensitivity", "mean"),
        average_care=("current_care", "mean"),
        average_stress=("current_stress", "mean"),
        average_embedded_stress=("embedded_stress", "mean"),
        average_embedded_support=("embedded_support", "mean"),
        final_development=("development_score", "last"),
    )

    child_summary["sensitivity_stress_profile"] = np.select(
        [
            (child_summary["biological_sensitivity"] >= 0) & (child_summary["average_stress"] >= 0),
            (child_summary["biological_sensitivity"] >= 0) & (child_summary["average_stress"] < 0),
            (child_summary["biological_sensitivity"] < 0) & (child_summary["average_stress"] >= 0),
        ],
        [
            "higher_sensitivity_higher_stress",
            "higher_sensitivity_lower_stress",
            "lower_sensitivity_higher_stress",
        ],
        default="lower_sensitivity_lower_stress",
    )

    panel = panel.merge(
        child_summary[["child_id", "sensitivity_stress_profile"]],
        on="child_id",
        how="left",
    )

    contexts.to_csv(DATA_DIR / "context_metadata.csv", index=False)
    child_summary.to_csv(DATA_DIR / "child_plasticity_profiles.csv", index=False)
    return panel


def main() -> None:
    panel = generate_panel()
    panel_path = DATA_DIR / "genes_environment_plasticity_panel.csv"
    panel.to_csv(panel_path, index=False)

    trajectory = panel.groupby("time", as_index=False).agg(
        average_development=("development_score", "mean"),
        average_embedded_stress=("embedded_stress", "mean"),
        average_embedded_support=("embedded_support", "mean"),
        average_care=("current_care", "mean"),
        average_stress=("current_stress", "mean"),
    )
    trajectory.to_csv(OUTPUTS_DIR / "generated_plasticity_trajectory.csv", index=False)

    print(f"Wrote {panel_path}")
    print(f"Rows: {len(panel):,}")
    print(f"Children: {panel['child_id'].nunique():,}")
    print(f"Contexts: {panel['context_id'].nunique():,}")


if __name__ == "__main__":
    main()
