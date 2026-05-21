#!/usr/bin/env python3
"""Generate synthetic disability/neurodivergence developmental panel data.

The data represent a teaching/research scaffold for modeling disability and
neurodivergence as developmental relations among profile, support, access,
barriers, communication, participation, caregiver advocacy, and institutions.
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
    n_children: int = 820,
    n_periods: int = 10,
    n_settings: int = 35,
    seed: int = 2026,
) -> pd.DataFrame:
    rng = np.random.default_rng(seed)

    children = pd.DataFrame({
        "child_id": np.arange(1, n_children + 1),
        "setting_id": rng.integers(1, n_settings + 1, n_children),
        "neuro_profile": rng.normal(0, 1, n_children),
        "support_quality": rng.normal(0, 1, n_children),
        "accessibility": rng.normal(0, 1, n_children),
        "barrier_burden": rng.normal(0, 1, n_children),
        "caregiver_advocacy": rng.normal(0, 0.8, n_children),
        "communication_access": rng.normal(0, 0.8, n_children),
    })

    settings = pd.DataFrame({
        "setting_id": np.arange(1, n_settings + 1),
        "inclusion_climate": rng.normal(0, 0.6, n_settings),
        "service_access": rng.normal(0, 0.6, n_settings),
        "sensory_flexibility": rng.normal(0, 0.5, n_settings),
    })

    panel = children.loc[children.index.repeat(n_periods)].copy()
    panel["time"] = np.tile(np.arange(n_periods), n_children)
    panel = panel.merge(settings, on="setting_id", how="left")

    panel["current_support"] = rng.normal(panel["support_quality"], 0.60)
    panel["current_access"] = rng.normal(panel["accessibility"], 0.60)
    panel["current_barrier"] = rng.normal(panel["barrier_burden"], 0.70)
    panel["current_communication"] = rng.normal(panel["communication_access"], 0.55)
    panel["current_advocacy"] = rng.normal(panel["caregiver_advocacy"], 0.55)

    panel = panel.sort_values(["child_id", "time"]).reset_index(drop=True)

    panel["participation_score"] = (
        45
        + 0.50 * panel["time"]
        + 1.15 * panel["current_support"]
        + 1.10 * panel["current_access"]
        + 0.95 * panel["current_communication"]
        + 0.85 * panel["inclusion_climate"]
        + 0.75 * panel["sensory_flexibility"]
        + 0.65 * panel["service_access"]
        - 1.25 * panel["current_barrier"]
        + rng.normal(0, 2.2, len(panel))
    )

    panel["development_score"] = np.nan

    for _, rows in panel.groupby("child_id", sort=False):
        previous_score = 50 + rng.normal(0, 3)

        for idx in rows.index:
            current_score = (
                0.70 * previous_score
                + 0.20 * panel.at[idx, "time"]
                + 0.45 * panel.at[idx, "neuro_profile"]
                + 1.10 * panel.at[idx, "current_support"]
                + 1.05 * panel.at[idx, "current_access"]
                + 0.90 * panel.at[idx, "current_communication"]
                + 0.80 * panel.at[idx, "participation_score"] / 10
                + 0.85 * panel.at[idx, "inclusion_climate"]
                + 0.70 * panel.at[idx, "service_access"]
                + 0.65 * panel.at[idx, "sensory_flexibility"]
                + 0.55 * panel.at[idx, "current_advocacy"]
                - 1.15 * panel.at[idx, "current_barrier"]
                + 0.50 * panel.at[idx, "current_support"] * panel.at[idx, "current_access"]
                - 0.40 * panel.at[idx, "current_barrier"] * abs(panel.at[idx, "neuro_profile"])
                + rng.normal(0, 2.3)
            )
            panel.at[idx, "development_score"] = current_score
            previous_score = current_score

    child_summary = panel.groupby("child_id", as_index=False).agg(
        average_access=("current_access", "mean"),
        average_barrier=("current_barrier", "mean"),
        average_support=("current_support", "mean"),
        average_participation=("participation_score", "mean"),
        final_development=("development_score", "last"),
    )

    child_summary["access_condition"] = np.select(
        [
            (child_summary["average_access"] >= 0) & (child_summary["average_barrier"] < 0),
            (child_summary["average_access"] >= 0) & (child_summary["average_barrier"] >= 0),
            (child_summary["average_access"] < 0) & (child_summary["average_barrier"] < 0),
        ],
        [
            "higher_access_lower_barrier",
            "higher_access_higher_barrier",
            "lower_access_lower_barrier",
        ],
        default="lower_access_higher_barrier",
    )

    panel = panel.merge(child_summary[["child_id", "access_condition"]], on="child_id", how="left")

    settings.to_csv(DATA_DIR / "setting_metadata.csv", index=False)
    child_summary.to_csv(DATA_DIR / "child_access_profiles.csv", index=False)
    return panel


def main() -> None:
    panel = generate_panel()
    panel_path = DATA_DIR / "disability_neurodivergence_panel.csv"
    panel.to_csv(panel_path, index=False)

    trajectory = panel.groupby("time", as_index=False).agg(
        average_development=("development_score", "mean"),
        average_participation=("participation_score", "mean"),
        average_support=("current_support", "mean"),
        average_access=("current_access", "mean"),
        average_barrier=("current_barrier", "mean"),
    )
    trajectory.to_csv(OUTPUTS_DIR / "generated_accessibility_trajectory.csv", index=False)

    print(f"Wrote {panel_path}")
    print(f"Rows: {len(panel):,}")
    print(f"Children: {panel['child_id'].nunique():,}")
    print(f"Settings: {panel['setting_id'].nunique():,}")


if __name__ == "__main__":
    main()
