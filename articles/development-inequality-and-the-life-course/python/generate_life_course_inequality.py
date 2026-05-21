#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
OUTPUTS_DIR = ROOT / "outputs"
DATA_DIR.mkdir(parents=True, exist_ok=True)
OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)

def generate_panel(n_people: int = 900, n_periods: int = 10, n_contexts: int = 36, seed: int = 2026) -> pd.DataFrame:
    rng = np.random.default_rng(seed)

    people = pd.DataFrame({
        "person_id": np.arange(1, n_people + 1),
        "context_id": rng.integers(1, n_contexts + 1, n_people),
        "baseline_resources": rng.normal(0, 1, n_people),
        "baseline_burden": rng.normal(0, 1, n_people),
        "support_buffer": rng.normal(0, 1, n_people),
        "baseline_health": rng.normal(0, 1, n_people),
        "person_resilience": rng.normal(0, 0.7, n_people),
    })

    contexts = pd.DataFrame({
        "context_id": np.arange(1, n_contexts + 1),
        "community_opportunity": rng.normal(0, 0.6, n_contexts),
        "institutional_support": rng.normal(0, 0.6, n_contexts),
        "environmental_safety": rng.normal(0, 0.6, n_contexts),
    })

    panel = people.loc[people.index.repeat(n_periods)].copy()
    panel["time"] = np.tile(np.arange(n_periods), n_people)
    panel["early_timing_weight"] = np.exp(-0.16 * panel["time"])
    panel["transition_weight"] = np.exp(-((panel["time"] - 6) ** 2) / (2 * 1.8**2))
    panel = panel.merge(contexts, on="context_id", how="left")

    panel["current_resources"] = rng.normal(
        panel["baseline_resources"] + 0.25 * panel["community_opportunity"] + 0.15 * panel["institutional_support"],
        0.60,
    )
    panel["current_burden"] = rng.normal(
        panel["baseline_burden"] - 0.20 * panel["environmental_safety"],
        0.70,
    )
    panel["current_support"] = rng.normal(
        panel["support_buffer"] + 0.25 * panel["institutional_support"],
        0.60,
    )
    panel["health_status"] = rng.normal(
        panel["baseline_health"] + 0.20 * panel["environmental_safety"],
        0.50,
    )

    panel = panel.sort_values(["person_id", "time"]).reset_index(drop=True)
    panel["weighted_resources"] = panel["current_resources"] * panel["early_timing_weight"]
    panel["weighted_burden"] = panel["current_burden"] * panel["early_timing_weight"]
    panel["transition_support"] = panel["current_support"] * panel["transition_weight"]
    panel["cumulative_resources"] = panel.groupby("person_id")["weighted_resources"].cumsum()
    panel["cumulative_burden"] = panel.groupby("person_id")["weighted_burden"].cumsum()
    panel["development_score"] = np.nan

    for _, rows in panel.groupby("person_id", sort=False):
        previous = 50 + rng.normal(0, 3)
        for idx in rows.index:
            current = (
                0.68 * previous
                + 0.20 * panel.at[idx, "time"]
                + 1.00 * panel.at[idx, "current_resources"] * panel.at[idx, "early_timing_weight"]
                - 1.15 * panel.at[idx, "current_burden"] * panel.at[idx, "early_timing_weight"]
                + 0.95 * panel.at[idx, "current_support"]
                + 0.85 * panel.at[idx, "transition_support"]
                + 0.75 * panel.at[idx, "health_status"]
                + 0.85 * panel.at[idx, "community_opportunity"]
                + 0.70 * panel.at[idx, "institutional_support"]
                + 0.55 * panel.at[idx, "environmental_safety"]
                + 0.55 * panel.at[idx, "person_resilience"]
                + rng.normal(0, 2.2)
            )
            panel.at[idx, "development_score"] = current
            previous = current

    person_summary = panel.groupby("person_id", as_index=False).agg(
        average_resources=("current_resources", "mean"),
        average_burden=("current_burden", "mean"),
        final_score=("development_score", "last"),
    )

    conditions = [
        (person_summary["average_resources"] >= 0) & (person_summary["average_burden"] < 0),
        (person_summary["average_resources"] >= 0) & (person_summary["average_burden"] >= 0),
        (person_summary["average_resources"] < 0) & (person_summary["average_burden"] < 0),
    ]
    labels = [
        "higher_resources_lower_burden",
        "higher_resources_higher_burden",
        "lower_resources_lower_burden",
    ]
    person_summary["inequality_profile"] = np.select(conditions, labels, default="lower_resources_higher_burden")
    panel = panel.merge(person_summary[["person_id", "inequality_profile"]], on="person_id", how="left")

    contexts.to_csv(DATA_DIR / "context_metadata.csv", index=False)
    person_summary.to_csv(DATA_DIR / "person_inequality_profiles.csv", index=False)
    return panel

def main() -> None:
    panel = generate_panel()
    panel.to_csv(DATA_DIR / "life_course_inequality_panel.csv", index=False)

    trajectory = panel.groupby("time", as_index=False).agg(
        average_development=("development_score", "mean"),
        average_resources=("current_resources", "mean"),
        average_burden=("current_burden", "mean"),
        average_support=("current_support", "mean"),
        average_health=("health_status", "mean"),
    )
    trajectory.to_csv(OUTPUTS_DIR / "generated_life_course_trajectory.csv", index=False)

    print("Wrote data/life_course_inequality_panel.csv")
    print(f"Rows: {len(panel):,}")
    print(f"People: {panel['person_id'].nunique():,}")
    print(f"Contexts: {panel['context_id'].nunique():,}")

if __name__ == "__main__":
    main()
