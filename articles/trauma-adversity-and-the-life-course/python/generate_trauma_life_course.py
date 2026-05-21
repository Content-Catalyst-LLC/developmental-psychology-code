#!/usr/bin/env python3
"""Generate synthetic trauma/adversity life-course panel data.

The dataset demonstrates timing-weighted adversity, cumulative risk,
caregiver support, contextual stability, community buffering, institutional
safety, service access, and dynamic adaptation. It does not represent real
children, families, schools, clinics, or communities.
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
    n_contexts: int = 36,
    seed: int = 2026,
) -> pd.DataFrame:
    rng = np.random.default_rng(seed)

    children = pd.DataFrame(
        {
            "child_id": np.arange(1, n_children + 1),
            "context_id": rng.integers(1, n_contexts + 1, n_children),
            "adversity_burden": rng.normal(0, 1, n_children),
            "caregiver_support": rng.normal(0, 1, n_children),
            "contextual_stability": rng.normal(0, 1, n_children),
            "baseline_health": rng.normal(0, 1, n_children),
            "child_resilience": rng.normal(0, 0.7, n_children),
        }
    )

    contexts = pd.DataFrame(
        {
            "context_id": np.arange(1, n_contexts + 1),
            "community_buffer": rng.normal(0, 0.6, n_contexts),
            "institutional_safety": rng.normal(0, 0.6, n_contexts),
            "service_access": rng.normal(0, 0.5, n_contexts),
        }
    )

    panel = children.loc[children.index.repeat(n_periods)].copy()
    panel["time"] = np.tile(np.arange(n_periods), n_children)
    panel["early_timing_weight"] = np.exp(-0.18 * panel["time"])
    panel["transition_weight"] = np.exp(-((panel["time"] - 6) ** 2) / (2 * 1.8**2))
    panel = panel.merge(contexts, on="context_id", how="left")

    panel["current_adversity"] = rng.normal(panel["adversity_burden"], 0.70)
    panel["current_support"] = rng.normal(
        panel["caregiver_support"] + 0.15 * panel["service_access"],
        0.60,
    )
    panel["current_stability"] = rng.normal(
        panel["contextual_stability"] + 0.15 * panel["institutional_safety"],
        0.60,
    )
    panel["current_health"] = rng.normal(panel["baseline_health"], 0.50)

    panel = panel.sort_values(["child_id", "time"]).reset_index(drop=True)
    panel["weighted_adversity"] = (
        panel["current_adversity"] * panel["early_timing_weight"]
    )
    panel["transition_support"] = panel["current_support"] * panel["transition_weight"]
    panel["cumulative_adversity"] = panel.groupby("child_id")[
        "weighted_adversity"
    ].cumsum()
    panel["cumulative_support"] = panel.groupby("child_id")[
        "current_support"
    ].cumsum()

    panel["adaptation_score"] = np.nan

    for _, rows in panel.groupby("child_id", sort=False):
        previous_score = 50 + rng.normal(0, 3)

        for idx in rows.index:
            current_score = (
                0.70 * previous_score
                + 0.18 * panel.at[idx, "time"]
                - 0.70 * panel.at[idx, "cumulative_adversity"]
                - 1.05 * panel.at[idx, "current_adversity"] * panel.at[idx, "early_timing_weight"]
                + 1.05 * panel.at[idx, "current_support"]
                + 0.95 * panel.at[idx, "current_stability"]
                + 0.85 * panel.at[idx, "community_buffer"]
                + 0.75 * panel.at[idx, "institutional_safety"]
                + 0.65 * panel.at[idx, "service_access"]
                + 0.70 * panel.at[idx, "transition_support"]
                + 0.60 * panel.at[idx, "current_health"]
                + 0.55 * panel.at[idx, "child_resilience"]
                + 0.75 * panel.at[idx, "current_support"] * panel.at[idx, "current_stability"]
                + rng.normal(0, 2.3)
            )
            panel.at[idx, "adaptation_score"] = current_score
            previous_score = current_score

    child_summary = panel.groupby("child_id", as_index=False).agg(
        average_adversity=("current_adversity", "mean"),
        average_support=("current_support", "mean"),
        average_stability=("current_stability", "mean"),
        final_score=("adaptation_score", "last"),
    )

    conditions = [
        (child_summary["average_adversity"] < 0)
        & (child_summary["average_support"] >= 0),
        (child_summary["average_adversity"] >= 0)
        & (child_summary["average_support"] >= 0),
        (child_summary["average_adversity"] < 0)
        & (child_summary["average_support"] < 0),
    ]

    labels = [
        "lower_adversity_higher_support",
        "higher_adversity_higher_support",
        "lower_adversity_lower_support",
    ]

    child_summary["adversity_support_profile"] = np.select(
        conditions,
        labels,
        default="higher_adversity_lower_support",
    )

    panel = panel.merge(
        child_summary[["child_id", "adversity_support_profile"]],
        on="child_id",
        how="left",
    )

    contexts.to_csv(DATA_DIR / "context_metadata.csv", index=False)
    child_summary.to_csv(DATA_DIR / "child_adversity_profiles.csv", index=False)
    return panel


def main() -> None:
    panel = generate_panel()
    panel_path = DATA_DIR / "trauma_life_course_panel.csv"
    panel.to_csv(panel_path, index=False)

    trajectory = panel.groupby("time", as_index=False).agg(
        average_adaptation=("adaptation_score", "mean"),
        average_adversity=("current_adversity", "mean"),
        average_support=("current_support", "mean"),
        average_stability=("current_stability", "mean"),
        average_cumulative_adversity=("cumulative_adversity", "mean"),
    )
    trajectory.to_csv(OUTPUTS_DIR / "generated_adaptation_trajectory.csv", index=False)

    profile_summary = panel.groupby("adversity_support_profile", as_index=False).agg(
        children=("child_id", "nunique"),
        average_adaptation=("adaptation_score", "mean"),
        average_adversity=("current_adversity", "mean"),
        average_support=("current_support", "mean"),
        average_stability=("current_stability", "mean"),
    )
    profile_summary.to_csv(DATA_DIR / "adversity_support_profile_summary.csv", index=False)

    print(f"Wrote synthetic panel dataset: {panel_path}")
    print(f"Rows: {len(panel):,}")
    print(f"Children: {panel['child_id'].nunique():,}")
    print(f"Contexts: {panel['context_id'].nunique():,}")
    print(f"Profiles: {panel['adversity_support_profile'].nunique():,}")


if __name__ == "__main__":
    main()
