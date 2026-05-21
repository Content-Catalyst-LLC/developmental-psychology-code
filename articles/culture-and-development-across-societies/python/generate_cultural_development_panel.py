#!/usr/bin/env python3
"""Generate synthetic cultural-development panel data.

The dataset demonstrates nested cultural-development processes, institutional
fit, cross-context mismatch, family support, society-level inclusion, linguistic
support, and dynamic developmental trajectories.
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
    n_societies: int = 30,
    seed: int = 2026,
) -> pd.DataFrame:
    rng = np.random.default_rng(seed)

    children = pd.DataFrame(
        {
            "child_id": np.arange(1, n_children + 1),
            "society_id": rng.integers(1, n_societies + 1, n_children),
            "family_orientation": rng.normal(0, 1, n_children),
            "institutional_fit": rng.normal(0, 1, n_children),
            "cross_context_mismatch": rng.normal(0, 1, n_children),
            "social_support": rng.normal(0, 1, n_children),
            "bicultural_flexibility": rng.normal(0, 0.7, n_children),
            "child_resilience": rng.normal(0, 0.6, n_children),
        }
    )

    societies = pd.DataFrame(
        {
            "society_id": np.arange(1, n_societies + 1),
            "society_climate": rng.normal(0, 0.6, n_societies),
            "institutional_inclusion": rng.normal(0, 0.6, n_societies),
            "linguistic_support": rng.normal(0, 0.5, n_societies),
            "pluralism_index": rng.normal(0, 0.55, n_societies),
        }
    )

    panel = children.loc[children.index.repeat(n_periods)].copy()
    panel["time"] = np.tile(np.arange(n_periods), n_children)
    panel = panel.merge(societies, on="society_id", how="left")

    panel["current_family"] = rng.normal(panel["family_orientation"], 0.6)
    panel["current_fit"] = rng.normal(
        panel["institutional_fit"] + 0.20 * panel["institutional_inclusion"],
        0.6,
    )
    panel["current_mismatch"] = rng.normal(
        panel["cross_context_mismatch"] - 0.20 * panel["pluralism_index"],
        0.7,
    )
    panel["current_support"] = rng.normal(
        panel["social_support"] + 0.20 * panel["society_climate"],
        0.6,
    )
    panel["current_flexibility"] = rng.normal(
        panel["bicultural_flexibility"] + 0.15 * panel["linguistic_support"],
        0.5,
    )

    panel = panel.sort_values(["child_id", "time"]).reset_index(drop=True)
    panel["development_score"] = np.nan

    for _, child_rows in panel.groupby("child_id", sort=False):
        previous_score = 50 + rng.normal(0, 3)

        for idx in child_rows.index:
            current_score = (
                0.70 * previous_score
                + 0.18 * panel.at[idx, "time"]
                + 1.00 * panel.at[idx, "current_family"]
                + 0.95 * panel.at[idx, "current_fit"]
                + 0.90 * panel.at[idx, "current_support"]
                + 0.80 * panel.at[idx, "current_flexibility"]
                + 0.75 * panel.at[idx, "society_climate"]
                + 0.70 * panel.at[idx, "institutional_inclusion"]
                + 0.50 * panel.at[idx, "linguistic_support"]
                + 0.45 * panel.at[idx, "pluralism_index"]
                + 0.55 * panel.at[idx, "child_resilience"]
                - 1.00 * panel.at[idx, "current_mismatch"]
                + rng.normal(0, 2.3)
            )
            panel.at[idx, "development_score"] = current_score
            previous_score = current_score

    child_summary = panel.groupby("child_id", as_index=False).agg(
        average_mismatch=("current_mismatch", "mean"),
        average_support=("current_support", "mean"),
        final_score=("development_score", "last"),
    )

    conditions = [
        (child_summary["average_mismatch"] < 0)
        & (child_summary["average_support"] >= 0),
        (child_summary["average_mismatch"] >= 0)
        & (child_summary["average_support"] >= 0),
        (child_summary["average_mismatch"] < 0)
        & (child_summary["average_support"] < 0),
    ]

    labels = [
        "lower_mismatch_higher_support",
        "higher_mismatch_higher_support",
        "lower_mismatch_lower_support",
    ]

    child_summary["cultural_condition"] = np.select(
        conditions,
        labels,
        default="higher_mismatch_lower_support",
    )

    panel = panel.merge(
        child_summary[["child_id", "cultural_condition"]],
        on="child_id",
        how="left",
    )

    societies.to_csv(DATA_DIR / "society_metadata.csv", index=False)
    child_summary.to_csv(DATA_DIR / "child_cultural_conditions.csv", index=False)
    return panel


def main() -> None:
    panel = generate_panel()
    panel_path = DATA_DIR / "cultural_development_panel.csv"
    panel.to_csv(panel_path, index=False)

    trajectory = panel.groupby("time", as_index=False).agg(
        average_development=("development_score", "mean"),
        average_family=("current_family", "mean"),
        average_fit=("current_fit", "mean"),
        average_mismatch=("current_mismatch", "mean"),
        average_support=("current_support", "mean"),
    )
    trajectory.to_csv(OUTPUTS_DIR / "generated_culture_trajectory.csv", index=False)

    condition_summary = panel.groupby("cultural_condition", as_index=False).agg(
        children=("child_id", "nunique"),
        average_development=("development_score", "mean"),
        average_mismatch=("current_mismatch", "mean"),
        average_support=("current_support", "mean"),
        average_fit=("current_fit", "mean"),
    )
    condition_summary.to_csv(DATA_DIR / "cultural_condition_summary.csv", index=False)

    print(f"Wrote synthetic panel dataset: {panel_path}")
    print(f"Rows: {len(panel):,}")
    print(f"Children: {panel['child_id'].nunique():,}")
    print(f"Societies: {panel['society_id'].nunique():,}")
    print(f"Cultural conditions: {panel['cultural_condition'].nunique():,}")


if __name__ == "__main__":
    main()
