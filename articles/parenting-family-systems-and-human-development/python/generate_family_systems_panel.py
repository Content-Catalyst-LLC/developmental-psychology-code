#!/usr/bin/env python3
"""Generate synthetic parenting and family-systems panel data.

The data represent a teaching/research scaffold for modeling family systems as
developmental ecologies shaped by parenting responsiveness, family climate,
household stability, kin support, sibling support, child regulation, caregiver
support, external stress, and economic security.
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
    n_households: int = 290,
    seed: int = 2026,
) -> pd.DataFrame:
    rng = np.random.default_rng(seed)

    children = pd.DataFrame({
        "child_id": np.arange(1, n_children + 1),
        "household_id": rng.integers(1, n_households + 1, n_children),
        "parenting_responsiveness": rng.normal(0, 1, n_children),
        "family_climate": rng.normal(0, 1, n_children),
        "external_stress": rng.normal(0, 1, n_children),
        "sibling_support": rng.normal(0, 0.8, n_children),
        "child_regulation": rng.normal(0, 0.8, n_children),
        "caregiver_support": rng.binomial(1, 0.35, n_children),
    })

    households = pd.DataFrame({
        "household_id": np.arange(1, n_households + 1),
        "household_stability": rng.normal(0, 0.6, n_households),
        "kin_support": rng.normal(0, 0.5, n_households),
        "economic_security": rng.normal(0, 0.6, n_households),
    })

    panel = children.loc[children.index.repeat(n_periods)].copy()
    panel["time"] = np.tile(np.arange(n_periods), n_children)
    panel = panel.merge(households, on="household_id", how="left")

    panel["current_parenting"] = rng.normal(panel["parenting_responsiveness"], 0.60)
    panel["current_family"] = rng.normal(panel["family_climate"], 0.60)
    panel["current_stress"] = rng.normal(panel["external_stress"], 0.70)
    panel["current_sibling"] = rng.normal(panel["sibling_support"], 0.55)
    panel["current_regulation"] = rng.normal(panel["child_regulation"], 0.55)

    panel = panel.sort_values(["child_id", "time"]).reset_index(drop=True)

    panel["family_support_index"] = (
        panel["current_parenting"]
        + panel["current_family"]
        + panel["household_stability"]
        + panel["kin_support"]
        + panel["economic_security"]
        - panel["current_stress"]
    )

    panel["development_score"] = np.nan

    for _, rows in panel.groupby("child_id", sort=False):
        previous_score = 50 + rng.normal(0, 3)

        for idx in rows.index:
            current_score = (
                0.70 * previous_score
                + 0.24 * panel.at[idx, "time"]
                + 1.15 * panel.at[idx, "current_parenting"]
                + 1.05 * panel.at[idx, "current_family"]
                + 0.90 * panel.at[idx, "household_stability"]
                + 0.80 * panel.at[idx, "kin_support"]
                + 0.75 * panel.at[idx, "economic_security"]
                + 0.70 * panel.at[idx, "current_sibling"]
                + 0.65 * panel.at[idx, "current_regulation"]
                + 0.85 * panel.at[idx, "caregiver_support"]
                - 1.10 * panel.at[idx, "current_stress"]
                + 0.45 * panel.at[idx, "current_parenting"] * panel.at[idx, "current_family"]
                + rng.normal(0, 2.3)
            )
            panel.at[idx, "development_score"] = current_score
            previous_score = current_score

    child_summary = panel.groupby("child_id", as_index=False).agg(
        average_parenting=("current_parenting", "mean"),
        average_family=("current_family", "mean"),
        average_stress=("current_stress", "mean"),
        average_support_index=("family_support_index", "mean"),
        final_development=("development_score", "last"),
    )

    child_summary["family_support_profile"] = np.select(
        [
            (child_summary["average_parenting"] >= 0) & (child_summary["average_family"] >= 0),
            (child_summary["average_parenting"] >= 0) & (child_summary["average_family"] < 0),
            (child_summary["average_parenting"] < 0) & (child_summary["average_family"] >= 0),
        ],
        [
            "higher_parenting_higher_family",
            "higher_parenting_lower_family",
            "lower_parenting_higher_family",
        ],
        default="lower_parenting_lower_family",
    )

    panel = panel.merge(
        child_summary[["child_id", "family_support_profile"]],
        on="child_id",
        how="left",
    )

    households.to_csv(DATA_DIR / "household_metadata.csv", index=False)
    child_summary.to_csv(DATA_DIR / "child_family_profiles.csv", index=False)
    return panel


def main() -> None:
    panel = generate_panel()
    panel_path = DATA_DIR / "family_systems_panel.csv"
    panel.to_csv(panel_path, index=False)

    trajectory = panel.groupby("time", as_index=False).agg(
        average_development=("development_score", "mean"),
        average_family_support=("family_support_index", "mean"),
        average_parenting=("current_parenting", "mean"),
        average_family=("current_family", "mean"),
        average_stress=("current_stress", "mean"),
    )
    trajectory.to_csv(OUTPUTS_DIR / "generated_family_systems_trajectory.csv", index=False)

    print(f"Wrote {panel_path}")
    print(f"Rows: {len(panel):,}")
    print(f"Children: {panel['child_id'].nunique():,}")
    print(f"Households: {panel['household_id'].nunique():,}")


if __name__ == "__main__":
    main()
