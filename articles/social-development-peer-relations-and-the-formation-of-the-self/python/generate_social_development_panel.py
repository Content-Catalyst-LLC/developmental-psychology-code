#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
OUT = ROOT / "outputs"
DATA.mkdir(exist_ok=True)
OUT.mkdir(exist_ok=True)

def main(seed: int = 2026) -> None:
    rng = np.random.default_rng(seed)
    n_children, n_periods, n_schools = 950, 10, 38

    children = pd.DataFrame({
        "child_id": np.arange(1, n_children + 1),
        "school_id": rng.integers(1, n_schools + 1, n_children),
        "baseline_social": rng.normal(50, 8, n_children),
        "peer_support_base": rng.normal(0, 1, n_children),
        "friendship_quality_base": rng.normal(0, 1, n_children),
        "family_support_base": rng.normal(0, 1, n_children),
        "social_interpretation_skill": rng.normal(0, 1, n_children),
        "chronic_exclusion": rng.binomial(1, 0.22, n_children),
    })

    schools = pd.DataFrame({
        "school_id": np.arange(1, n_schools + 1),
        "school_connectedness": rng.normal(0, 0.6, n_schools),
        "teacher_support": rng.normal(0, 0.6, n_schools),
        "anti_bullying_climate": rng.normal(0, 0.6, n_schools),
        "inclusion_climate": rng.normal(0, 0.6, n_schools),
        "restorative_practice_access": rng.normal(0, 0.5, n_schools),
    })

    panel = children.loc[children.index.repeat(n_periods)].copy()
    panel["time"] = np.tile(np.arange(n_periods), n_children)
    panel = panel.merge(schools, on="school_id", how="left")

    panel["current_peer_support"] = rng.normal(panel["peer_support_base"], 0.70)
    panel["current_friendship_quality"] = rng.normal(panel["friendship_quality_base"], 0.70)
    panel["current_family_support"] = rng.normal(panel["family_support_base"], 0.70)
    panel["current_social_interpretation"] = rng.normal(panel["social_interpretation_skill"], 0.50)

    panel["current_exclusion"] = rng.normal(
        0.45 * panel["chronic_exclusion"]
        - 0.25 * panel["anti_bullying_climate"]
        - 0.20 * panel["inclusion_climate"],
        0.70,
    )

    panel["bullying_exposure"] = rng.normal(
        0.35 * panel["chronic_exclusion"]
        + 0.25 * panel["current_exclusion"]
        - 0.30 * panel["anti_bullying_climate"],
        0.70,
    )

    panel["digital_comparison_stress"] = rng.normal(
        0.25 * panel["current_exclusion"]
        - 0.15 * panel["current_friendship_quality"],
        0.70,
    )

    panel["social_support_context"] = (
        panel["current_peer_support"]
        + panel["current_friendship_quality"]
        + panel["current_family_support"]
        + panel["current_social_interpretation"]
        + panel["school_connectedness"]
        + panel["teacher_support"]
        + panel["anti_bullying_climate"]
        + panel["inclusion_climate"]
        + panel["restorative_practice_access"]
    )

    panel = panel.sort_values(["child_id", "time"]).reset_index(drop=True)
    panel["social_self_score"] = np.nan

    for _, rows in panel.groupby("child_id", sort=False):
        previous_score = rows["baseline_social"].iloc[0]
        for idx in rows.index:
            row = panel.loc[idx]
            current_score = (
                0.70 * previous_score
                + 0.85 * row.time
                + 1.10 * row.current_peer_support
                + 1.00 * row.current_friendship_quality
                + 0.95 * row.current_family_support
                + 0.85 * row.current_social_interpretation
                + 0.90 * row.school_connectedness
                + 0.75 * row.teacher_support
                + 0.80 * row.anti_bullying_climate
                + 0.80 * row.inclusion_climate
                + 0.60 * row.restorative_practice_access
                - 1.20 * row.current_exclusion
                - 1.10 * row.bullying_exposure
                - 0.75 * row.digital_comparison_stress
                - 0.90 * row.chronic_exclusion
                + 0.25 * row.social_support_context
                + rng.normal(0, 2.5)
            )
            panel.at[idx, "social_self_score"] = current_score
            previous_score = current_score

    profiles = panel.groupby("child_id", as_index=False).agg(
        average_social_support_context=("social_support_context", "mean"),
        average_exclusion=("current_exclusion", "mean"),
        average_bullying=("bullying_exposure", "mean"),
        average_digital_comparison=("digital_comparison_stress", "mean"),
        average_social_self=("social_self_score", "mean"),
        final_social_self=("social_self_score", "last"),
        chronic_exclusion=("chronic_exclusion", "first"),
    )

    support_median = profiles.average_social_support_context.median()
    bullying_median = profiles.average_bullying.median()
    profiles["social_profile"] = np.select(
        [
            (profiles.chronic_exclusion == 1) & (profiles.average_social_support_context >= support_median),
            (profiles.chronic_exclusion == 1) & (profiles.average_social_support_context < support_median),
            (profiles.average_bullying >= bullying_median) & (profiles.average_social_support_context >= support_median),
            (profiles.average_bullying >= bullying_median) & (profiles.average_social_support_context < support_median),
        ],
        [
            "higher_exclusion_higher_social_support",
            "higher_exclusion_lower_social_support",
            "higher_bullying_higher_social_support",
            "higher_bullying_lower_social_support",
        ],
        default="lower_exclusion_or_bullying",
    )

    panel = panel.merge(profiles[["child_id", "social_profile"]], on="child_id", how="left")

    panel.to_csv(DATA / "social_development_panel.csv", index=False)
    schools.to_csv(DATA / "school_social_context_metadata.csv", index=False)
    profiles.to_csv(DATA / "social_development_profiles.csv", index=False)

    panel.groupby(["time", "chronic_exclusion"], as_index=False).agg(
        average_social_self=("social_self_score", "mean"),
        average_social_context=("social_support_context", "mean"),
        average_exclusion=("current_exclusion", "mean"),
        average_bullying=("bullying_exposure", "mean"),
        average_digital_comparison=("digital_comparison_stress", "mean"),
    ).to_csv(OUT / "generated_social_development_trajectory.csv", index=False)

    print(f"Wrote {DATA / 'social_development_panel.csv'} with {len(panel):,} rows")

if __name__ == "__main__":
    main()
