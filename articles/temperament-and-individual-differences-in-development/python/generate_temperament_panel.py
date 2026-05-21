#!/usr/bin/env python3
"""Generate synthetic temperament and individual-differences panel data.

The data represent a teaching/research scaffold for modeling temperament as a
developmental process shaped by reactivity, inhibition, activity level,
caregiver support, classroom fit, stress exposure, accommodation, teacher
responsiveness, movement flexibility, and goodness of fit.
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
    n_classrooms: int = 36,
    seed: int = 2026,
) -> pd.DataFrame:
    rng = np.random.default_rng(seed)

    children = pd.DataFrame({
        "child_id": np.arange(1, n_children + 1),
        "classroom_id": rng.integers(1, n_classrooms + 1, n_children),
        "temperament_reactivity": rng.normal(0, 1, n_children),
        "inhibition": rng.normal(0, 1, n_children),
        "activity_level": rng.normal(0, 1, n_children),
        "baseline_adjustment": rng.normal(50, 8, n_children),
        "chronic_stress": rng.binomial(1, 0.30, n_children),
        "family_support": rng.normal(0, 1, n_children),
        "school_fit": rng.normal(0, 1, n_children),
    })

    classrooms = pd.DataFrame({
        "classroom_id": np.arange(1, n_classrooms + 1),
        "classroom_structure": rng.normal(0, 0.6, n_classrooms),
        "teacher_responsiveness": rng.normal(0, 0.6, n_classrooms),
        "movement_flexibility": rng.normal(0, 0.5, n_classrooms),
    })

    panel = children.loc[children.index.repeat(n_periods)].copy()
    panel["time"] = np.tile(np.arange(n_periods), n_children)
    panel = panel.merge(classrooms, on="classroom_id", how="left")

    panel["current_support"] = rng.normal(panel["family_support"], 0.70)
    panel["current_school_fit"] = rng.normal(panel["school_fit"], 0.70)
    panel["acute_stress"] = rng.normal(0.3 * panel["chronic_stress"], 0.80)
    panel["current_accommodation"] = rng.normal(0.40, 0.50, len(panel))

    panel["goodness_of_fit"] = (
        panel["current_school_fit"]
        + panel["teacher_responsiveness"]
        + panel["movement_flexibility"]
        - np.abs(panel["temperament_reactivity"] - panel["classroom_structure"])
        + panel["current_accommodation"]
    )

    panel = panel.sort_values(["child_id", "time"]).reset_index(drop=True)
    panel["adjustment_score"] = np.nan

    for _, rows in panel.groupby("child_id", sort=False):
        previous_score = rows["baseline_adjustment"].iloc[0] + rng.normal(0, 2)

        for idx in rows.index:
            temp = panel.at[idx, "temperament_reactivity"]
            inhibition = panel.at[idx, "inhibition"]
            activity = panel.at[idx, "activity_level"]
            support = panel.at[idx, "current_support"]
            fit = panel.at[idx, "goodness_of_fit"]
            stress = panel.at[idx, "acute_stress"]
            chronic = panel.at[idx, "chronic_stress"]
            teacher = panel.at[idx, "teacher_responsiveness"]
            time = panel.at[idx, "time"]

            current_score = (
                0.70 * previous_score
                + 0.90 * time
                + 1.30 * support
                + 1.20 * fit
                + 0.50 * teacher
                - 1.50 * stress
                - 1.10 * chronic
                - 0.25 * inhibition
                - 0.20 * activity
                + 0.95 * temp * support
                + 0.85 * temp * fit
                - 0.90 * temp * stress
                + rng.normal(0, 2.5)
            )

            panel.at[idx, "adjustment_score"] = current_score
            previous_score = current_score

    child_summary = panel.groupby("child_id", as_index=False).agg(
        average_reactivity=("temperament_reactivity", "mean"),
        average_fit=("goodness_of_fit", "mean"),
        average_support=("current_support", "mean"),
        average_stress=("acute_stress", "mean"),
        final_adjustment=("adjustment_score", "last"),
    )

    reactivity_median = child_summary["average_reactivity"].median()
    fit_median = child_summary["average_fit"].median()

    child_summary["temperament_profile"] = np.select(
        [
            (child_summary["average_reactivity"] >= reactivity_median) & (child_summary["average_fit"] >= fit_median),
            (child_summary["average_reactivity"] >= reactivity_median) & (child_summary["average_fit"] < fit_median),
            (child_summary["average_reactivity"] < reactivity_median) & (child_summary["average_fit"] >= fit_median),
        ],
        [
            "higher_reactivity_higher_fit",
            "higher_reactivity_lower_fit",
            "lower_reactivity_higher_fit",
        ],
        default="lower_reactivity_lower_fit",
    )

    panel = panel.merge(
        child_summary[["child_id", "temperament_profile"]],
        on="child_id",
        how="left",
    )

    classrooms.to_csv(DATA_DIR / "classroom_metadata.csv", index=False)
    child_summary.to_csv(DATA_DIR / "child_temperament_profiles.csv", index=False)
    return panel


def main() -> None:
    panel = generate_panel()
    panel_path = DATA_DIR / "temperament_individual_differences_panel.csv"
    panel.to_csv(panel_path, index=False)

    trajectory = panel.groupby(["time", "temperament_profile"], as_index=False).agg(
        average_adjustment=("adjustment_score", "mean"),
        average_fit=("goodness_of_fit", "mean"),
        average_support=("current_support", "mean"),
        average_stress=("acute_stress", "mean"),
        average_accommodation=("current_accommodation", "mean"),
    )
    trajectory.to_csv(OUTPUTS_DIR / "generated_temperament_trajectory.csv", index=False)

    print(f"Wrote {panel_path}")
    print(f"Rows: {len(panel):,}")
    print(f"Children: {panel['child_id'].nunique():,}")
    print(f"Classrooms: {panel['classroom_id'].nunique():,}")


if __name__ == "__main__":
    main()
