#!/usr/bin/env python3
"""Generate synthetic lifespan developmental psychology panel data.

The data represent a teaching/research scaffold for modeling Baltesian lifespan
development as lifelong, multidirectional, plastic, historically embedded, and
shaped by gains, losses, contextual support, compensation, and SOC adaptation.
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
    n_people: int = 950,
    n_periods: int = 12,
    n_cohorts: int = 6,
    seed: int = 2026,
) -> pd.DataFrame:
    rng = np.random.default_rng(seed)

    people = pd.DataFrame({
        "id": np.arange(1, n_people + 1),
        "cohort_id": rng.integers(1, n_cohorts + 1, n_people),
        "baseline_dev": rng.normal(50, 8, n_people),
        "plasticity": rng.normal(0, 1, n_people),
        "context_support": rng.normal(0, 1, n_people),
        "comp_capacity": rng.normal(0, 1, n_people),
        "health_resource": rng.normal(0, 0.8, n_people),
    })

    cohorts = pd.DataFrame({
        "cohort_id": np.arange(1, n_cohorts + 1),
        "historical_support": rng.normal(0, 0.6, n_cohorts),
        "institutional_security": rng.normal(0, 0.6, n_cohorts),
    })

    panel = people.loc[people.index.repeat(n_periods)].copy()
    panel["time"] = np.tile(np.arange(n_periods), n_people)
    panel = panel.merge(cohorts, on="cohort_id", how="left")

    panel["gains"] = rng.normal(0.90 - 0.05 * panel["time"], 0.50)
    panel["losses"] = rng.normal(0.20 + 0.07 * panel["time"], 0.50)
    panel["current_support"] = rng.normal(panel["context_support"], 0.70)
    panel["current_comp"] = rng.normal(panel["comp_capacity"], 0.70)
    panel["selection"] = rng.normal(0.30 + 0.04 * panel["time"], 0.50)
    panel["optimization"] = rng.normal(0.50, 0.50, len(panel))
    panel["compensation"] = rng.normal(panel["comp_capacity"] + 0.05 * panel["time"], 0.50)

    panel["soc_index"] = (
        0.35 * panel["selection"]
        + 0.35 * panel["optimization"]
        + 0.30 * panel["compensation"]
    )

    panel = panel.sort_values(["id", "time"]).reset_index(drop=True)
    panel["development_score"] = np.nan

    for _, rows in panel.groupby("id", sort=False):
        previous_score = rows["baseline_dev"].iloc[0] + rng.normal(0, 2)

        for idx in rows.index:
            time = panel.at[idx, "time"]
            gains = panel.at[idx, "gains"]
            losses = panel.at[idx, "losses"]
            plasticity = panel.at[idx, "plasticity"]
            support = panel.at[idx, "current_support"]
            comp = panel.at[idx, "current_comp"]
            health = panel.at[idx, "health_resource"]
            historical = panel.at[idx, "historical_support"]
            institutional = panel.at[idx, "institutional_security"]
            soc = panel.at[idx, "soc_index"]
            compensation = panel.at[idx, "compensation"]

            current_score = (
                0.70 * previous_score
                + 0.20 * time
                + 1.05 * gains
                - 1.00 * losses
                + 0.90 * plasticity
                + 0.95 * support
                + 0.80 * comp
                + 0.65 * health
                + 0.75 * historical
                + 0.70 * institutional
                + 0.90 * soc
                + 0.35 * plasticity * support
                - 0.30 * losses * compensation
                + rng.normal(0, 2.5)
            )

            panel.at[idx, "development_score"] = current_score
            previous_score = current_score

    person_summary = panel.groupby("id", as_index=False).agg(
        average_gains=("gains", "mean"),
        average_losses=("losses", "mean"),
        average_support=("current_support", "mean"),
        average_soc=("soc_index", "mean"),
        final_development=("development_score", "last"),
    )

    person_summary["adaptation_profile"] = np.select(
        [
            (person_summary["average_support"] >= 0) & (person_summary["average_losses"] < person_summary["average_losses"].median()),
            (person_summary["average_support"] >= 0) & (person_summary["average_losses"] >= person_summary["average_losses"].median()),
            (person_summary["average_support"] < 0) & (person_summary["average_losses"] < person_summary["average_losses"].median()),
        ],
        [
            "higher_support_lower_loss",
            "higher_support_higher_loss",
            "lower_support_lower_loss",
        ],
        default="lower_support_higher_loss",
    )

    panel = panel.merge(
        person_summary[["id", "adaptation_profile"]],
        on="id",
        how="left",
    )

    cohorts.to_csv(DATA_DIR / "cohort_metadata.csv", index=False)
    person_summary.to_csv(DATA_DIR / "person_lifespan_profiles.csv", index=False)
    return panel


def main() -> None:
    panel = generate_panel()
    panel_path = DATA_DIR / "lifespan_baltes_panel.csv"
    panel.to_csv(panel_path, index=False)

    trajectory = panel.groupby("time", as_index=False).agg(
        average_development=("development_score", "mean"),
        average_gains=("gains", "mean"),
        average_losses=("losses", "mean"),
        average_soc=("soc_index", "mean"),
        average_support=("current_support", "mean"),
    )
    trajectory.to_csv(OUTPUTS_DIR / "generated_lifespan_baltes_trajectory.csv", index=False)

    print(f"Wrote {panel_path}")
    print(f"Rows: {len(panel):,}")
    print(f"People: {panel['id'].nunique():,}")
    print(f"Cohorts: {panel['cohort_id'].nunique():,}")


if __name__ == "__main__":
    main()
