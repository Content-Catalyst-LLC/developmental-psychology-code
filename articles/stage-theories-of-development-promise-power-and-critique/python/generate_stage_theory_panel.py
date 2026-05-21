#!/usr/bin/env python3
"""Generate synthetic stage-theory developmental panel data.

The data represent a teaching/research scaffold for modeling stage-like
development as continuous growth, threshold reorganization, logistic transition,
context support, chronic stress, resource stability, and transition readiness.
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


def logistic(x: np.ndarray, k: float = 1.35) -> np.ndarray:
    return 1.0 / (1.0 + np.exp(-k * x))


def generate_panel(
    n_children: int = 950,
    n_periods: int = 10,
    n_contexts: int = 36,
    seed: int = 2026,
) -> pd.DataFrame:
    rng = np.random.default_rng(seed)

    children = pd.DataFrame({
        "child_id": np.arange(1, n_children + 1),
        "context_id": rng.integers(1, n_contexts + 1, n_children),
        "baseline_functioning": rng.normal(46, 7, n_children),
        "growth_rate": rng.normal(1.70, 0.50, n_children),
        "support_context": rng.normal(0, 1, n_children),
        "chronic_stress": rng.binomial(1, 0.32, n_children),
        "threshold_time": rng.integers(4, 8, n_children),
        "stage_pattern": rng.binomial(1, 0.50, n_children),
    })

    contexts = pd.DataFrame({
        "context_id": np.arange(1, n_contexts + 1),
        "school_support": rng.normal(0, 0.6, n_contexts),
        "resource_stability": rng.normal(0, 0.5, n_contexts),
    })

    panel = children.loc[children.index.repeat(n_periods)].copy()
    panel["time"] = np.tile(np.arange(n_periods), n_children)
    panel = panel.merge(contexts, on="context_id", how="left")

    panel["current_support"] = rng.normal(panel["support_context"], 0.70)
    panel["threshold_on"] = (panel["time"] >= panel["threshold_time"]).astype(int)
    panel["logistic_transition"] = logistic(panel["time"] - panel["threshold_time"])

    panel["transition_readiness"] = (
        panel["current_support"]
        + panel["school_support"]
        + panel["resource_stability"]
        - 0.75 * panel["chronic_stress"]
    )

    panel = panel.sort_values(["child_id", "time"]).reset_index(drop=True)
    panel["development_score"] = np.nan

    for _, rows in panel.groupby("child_id", sort=False):
        previous_score = rows["baseline_functioning"].iloc[0]

        for idx in rows.index:
            time = panel.at[idx, "time"]
            growth_rate = panel.at[idx, "growth_rate"]
            support = panel.at[idx, "current_support"]
            stress = panel.at[idx, "chronic_stress"]
            school_support = panel.at[idx, "school_support"]
            stability = panel.at[idx, "resource_stability"]
            threshold_on = panel.at[idx, "threshold_on"]
            logistic_transition = panel.at[idx, "logistic_transition"]
            stage_pattern = panel.at[idx, "stage_pattern"]
            readiness = panel.at[idx, "transition_readiness"]

            current_score = (
                0.58 * previous_score
                + 0.42 * (panel.at[idx, "baseline_functioning"] + growth_rate * time)
                + 1.15 * support
                + 0.90 * school_support
                + 0.70 * stability
                - 2.00 * stress
                + 3.00 * threshold_on * stage_pattern
                + 2.20 * logistic_transition * stage_pattern
                + 0.75 * threshold_on * stage_pattern * readiness
                + rng.normal(0, 2.5)
            )

            panel.at[idx, "development_score"] = current_score
            previous_score = current_score

    profile = panel.groupby("child_id", as_index=False).agg(
        average_transition_readiness=("transition_readiness", "mean"),
        average_score=("development_score", "mean"),
        final_score=("development_score", "last"),
        stage_pattern=("stage_pattern", "first"),
        threshold_time=("threshold_time", "first"),
    )

    readiness_median = profile["average_transition_readiness"].median()
    profile["stage_profile"] = np.select(
        [
            (profile["stage_pattern"] == 1) & (profile["average_transition_readiness"] >= readiness_median),
            (profile["stage_pattern"] == 1) & (profile["average_transition_readiness"] < readiness_median),
            (profile["stage_pattern"] == 0) & (profile["average_transition_readiness"] >= readiness_median),
        ],
        [
            "stage_like_higher_readiness",
            "stage_like_lower_readiness",
            "continuous_higher_readiness",
        ],
        default="continuous_lower_readiness",
    )

    panel = panel.merge(profile[["child_id", "stage_profile"]], on="child_id", how="left")

    contexts.to_csv(DATA_DIR / "context_metadata.csv", index=False)
    profile.to_csv(DATA_DIR / "stage_theory_child_profiles.csv", index=False)
    return panel


def main() -> None:
    panel = generate_panel()
    panel_path = DATA_DIR / "stage_theory_development_panel.csv"
    panel.to_csv(panel_path, index=False)

    trajectory = panel.groupby(["time", "stage_pattern"], as_index=False).agg(
        average_score=("development_score", "mean"),
        average_readiness=("transition_readiness", "mean"),
        average_support=("current_support", "mean"),
        average_logistic_transition=("logistic_transition", "mean"),
    )
    trajectory.to_csv(OUTPUTS_DIR / "generated_stage_theory_trajectory.csv", index=False)

    print(f"Wrote {panel_path}")
    print(f"Rows: {len(panel):,}")
    print(f"Individuals: {panel['child_id'].nunique():,}")
    print(f"Contexts: {panel['context_id'].nunique():,}")


if __name__ == "__main__":
    main()
