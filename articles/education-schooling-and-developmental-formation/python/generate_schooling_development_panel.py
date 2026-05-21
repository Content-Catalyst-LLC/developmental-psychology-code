#!/usr/bin/env python3
"""Generate synthetic schooling and developmental formation panel data.

The data represent a teaching/research scaffold for modeling schooling as a
developmental institution shaped by teacher support, peer belonging, school
climate, curriculum opportunity, stress, connectedness, intervention exposure,
family support, and resources.
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
    n_students: int = 850,
    n_periods: int = 10,
    n_schools: int = 36,
    seed: int = 2026,
) -> pd.DataFrame:
    rng = np.random.default_rng(seed)

    students = pd.DataFrame({
        "student_id": np.arange(1, n_students + 1),
        "school_id": rng.integers(1, n_schools + 1, n_students),
        "baseline_teacher_support": rng.normal(0, 1, n_students),
        "baseline_peer_belonging": rng.normal(0, 1, n_students),
        "baseline_school_stress": rng.normal(0, 1, n_students),
        "family_support": rng.normal(0, 1, n_students),
        "academic_confidence": rng.normal(0, 0.8, n_students),
        "intervention": rng.binomial(1, 0.35, n_students),
    })

    schools = pd.DataFrame({
        "school_id": np.arange(1, n_schools + 1),
        "school_climate": rng.normal(0, 0.6, n_schools),
        "curriculum_opportunity": rng.normal(0, 0.6, n_schools),
        "restorative_practice": rng.normal(0, 0.5, n_schools),
        "resource_capacity": rng.normal(0, 0.5, n_schools),
    })

    panel = students.loc[students.index.repeat(n_periods)].copy()
    panel["time"] = np.tile(np.arange(n_periods), n_students)
    panel = panel.merge(schools, on="school_id", how="left")

    panel["current_teacher"] = rng.normal(panel["baseline_teacher_support"], 0.60)
    panel["current_peer"] = rng.normal(panel["baseline_peer_belonging"], 0.60)
    panel["current_stress"] = rng.normal(panel["baseline_school_stress"], 0.70)
    panel["current_family"] = rng.normal(panel["family_support"], 0.55)
    panel["current_confidence"] = rng.normal(panel["academic_confidence"], 0.55)

    panel = panel.sort_values(["student_id", "time"]).reset_index(drop=True)

    panel["connectedness_score"] = (
        45
        + 0.45 * panel["time"]
        + 1.20 * panel["current_teacher"]
        + 1.05 * panel["current_peer"]
        + 0.80 * panel["school_climate"]
        + 0.60 * panel["restorative_practice"]
        - 1.10 * panel["current_stress"]
        + rng.normal(0, 2.2, len(panel))
    )

    panel["development_score"] = np.nan

    for _, rows in panel.groupby("student_id", sort=False):
        previous_score = 50 + rng.normal(0, 3)

        for idx in rows.index:
            current_score = (
                0.70 * previous_score
                + 0.22 * panel.at[idx, "time"]
                + 1.10 * panel.at[idx, "current_teacher"]
                + 1.00 * panel.at[idx, "current_peer"]
                + 0.95 * panel.at[idx, "school_climate"]
                + 0.90 * panel.at[idx, "curriculum_opportunity"]
                + 0.75 * panel.at[idx, "current_family"]
                + 0.70 * panel.at[idx, "current_confidence"]
                + 0.65 * panel.at[idx, "resource_capacity"]
                + 0.85 * panel.at[idx, "intervention"]
                + 0.55 * panel.at[idx, "connectedness_score"] / 10
                - 1.05 * panel.at[idx, "current_stress"]
                + 0.50 * panel.at[idx, "current_teacher"] * panel.at[idx, "current_peer"]
                + rng.normal(0, 2.3)
            )
            panel.at[idx, "development_score"] = current_score
            previous_score = current_score

    student_summary = panel.groupby("student_id", as_index=False).agg(
        average_teacher=("current_teacher", "mean"),
        average_peer=("current_peer", "mean"),
        average_stress=("current_stress", "mean"),
        average_connectedness=("connectedness_score", "mean"),
        final_development=("development_score", "last"),
    )

    student_summary["school_support_profile"] = np.select(
        [
            (student_summary["average_teacher"] >= 0) & (student_summary["average_peer"] >= 0),
            (student_summary["average_teacher"] >= 0) & (student_summary["average_peer"] < 0),
            (student_summary["average_teacher"] < 0) & (student_summary["average_peer"] >= 0),
        ],
        [
            "higher_teacher_higher_peer",
            "higher_teacher_lower_peer",
            "lower_teacher_higher_peer",
        ],
        default="lower_teacher_lower_peer",
    )

    panel = panel.merge(
        student_summary[["student_id", "school_support_profile"]],
        on="student_id",
        how="left",
    )

    schools.to_csv(DATA_DIR / "school_metadata.csv", index=False)
    student_summary.to_csv(DATA_DIR / "student_school_profiles.csv", index=False)
    return panel


def main() -> None:
    panel = generate_panel()
    panel_path = DATA_DIR / "schooling_development_panel.csv"
    panel.to_csv(panel_path, index=False)

    trajectory = panel.groupby("time", as_index=False).agg(
        average_development=("development_score", "mean"),
        average_connectedness=("connectedness_score", "mean"),
        average_teacher=("current_teacher", "mean"),
        average_peer=("current_peer", "mean"),
        average_stress=("current_stress", "mean"),
    )
    trajectory.to_csv(OUTPUTS_DIR / "generated_schooling_trajectory.csv", index=False)

    print(f"Wrote {panel_path}")
    print(f"Rows: {len(panel):,}")
    print(f"Students: {panel['student_id'].nunique():,}")
    print(f"Schools: {panel['school_id'].nunique():,}")


if __name__ == "__main__":
    main()
