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
    n_children, n_periods, n_schools = 920, 10, 36

    children = pd.DataFrame({
        "child_id": np.arange(1, n_children + 1),
        "school_id": rng.integers(1, n_schools + 1, n_children),
        "baseline_ef": rng.normal(50, 8, n_children),
        "caregiving_support": rng.normal(0, 1, n_children),
        "classroom_structure": rng.normal(0, 1, n_children),
        "sleep_quality": rng.normal(0, 1, n_children),
        "chronic_stress": rng.binomial(1, 0.30, n_children),
        "temperament_reactivity": rng.normal(0, 1, n_children),
        "disability_support_need": rng.binomial(1, 0.18, n_children),
    })

    schools = pd.DataFrame({
        "school_id": np.arange(1, n_schools + 1),
        "school_climate": rng.normal(0, 0.6, n_schools),
        "regulation_scaffolding": rng.normal(0, 0.6, n_schools),
        "disability_accommodation": rng.normal(0, 0.6, n_schools),
        "transition_predictability": rng.normal(0, 0.5, n_schools),
    })

    panel = children.loc[children.index.repeat(n_periods)].copy()
    panel["time"] = np.tile(np.arange(n_periods), n_children)
    panel = panel.merge(schools, on="school_id", how="left")

    panel["current_support"] = rng.normal(panel["caregiving_support"], 0.70)
    panel["current_structure"] = rng.normal(panel["classroom_structure"], 0.70)
    panel["current_sleep"] = rng.normal(panel["sleep_quality"], 0.50)
    panel["acute_stress"] = rng.normal(0.35 * panel["chronic_stress"], 0.80)
    panel["intervention_exposure"] = (
        (panel["time"] >= 5) &
        (rng.uniform(size=len(panel)) < 0.35)
    ).astype(int)

    panel["regulatory_support_context"] = (
        panel["current_support"]
        + panel["current_structure"]
        + panel["current_sleep"]
        + panel["school_climate"]
        + panel["regulation_scaffolding"]
        + panel["transition_predictability"]
        + panel["disability_accommodation"] * panel["disability_support_need"]
    )

    panel = panel.sort_values(["child_id", "time"]).reset_index(drop=True)
    panel["regulation_score"] = np.nan

    for _, rows in panel.groupby("child_id", sort=False):
        previous_score = rows["baseline_ef"].iloc[0]
        for idx in rows.index:
            row = panel.loc[idx]
            current_score = (
                0.70 * previous_score
                + 0.90 * row.time
                + 1.15 * row.current_support
                + 1.05 * row.current_structure
                + 0.90 * row.current_sleep
                + 0.80 * row.school_climate
                + 0.95 * row.regulation_scaffolding
                + 0.80 * row.transition_predictability
                + 0.90 * row.disability_accommodation * row.disability_support_need
                + 1.10 * row.intervention_exposure
                - 1.25 * row.acute_stress
                - 0.90 * row.chronic_stress
                + 0.75 * row.temperament_reactivity * row.current_support
                - 0.80 * row.temperament_reactivity * row.acute_stress
                + 0.25 * row.regulatory_support_context
                + rng.normal(0, 2.5)
            )
            panel.at[idx, "regulation_score"] = current_score
            previous_score = current_score

    profiles = panel.groupby("child_id", as_index=False).agg(
        average_regulatory_support_context=("regulatory_support_context", "mean"),
        average_stress=("acute_stress", "mean"),
        average_sleep=("current_sleep", "mean"),
        average_regulation=("regulation_score", "mean"),
        final_regulation=("regulation_score", "last"),
        chronic_stress=("chronic_stress", "first"),
        disability_support_need=("disability_support_need", "first"),
    )

    support_median = profiles.average_regulatory_support_context.median()
    profiles["regulation_profile"] = np.select(
        [
            (profiles.chronic_stress == 1) & (profiles.average_regulatory_support_context >= support_median),
            (profiles.chronic_stress == 1) & (profiles.average_regulatory_support_context < support_median),
            (profiles.disability_support_need == 1) & (profiles.average_regulatory_support_context >= support_median),
            (profiles.disability_support_need == 1) & (profiles.average_regulatory_support_context < support_median),
        ],
        [
            "higher_stress_higher_support",
            "higher_stress_lower_support",
            "support_need_higher_support",
            "support_need_lower_support",
        ],
        default="lower_stress_or_lower_support_need",
    )

    panel = panel.merge(profiles[["child_id", "regulation_profile"]], on="child_id", how="left")

    panel.to_csv(DATA / "regulation_development_panel.csv", index=False)
    schools.to_csv(DATA / "school_regulation_context_metadata.csv", index=False)
    profiles.to_csv(DATA / "regulation_development_profiles.csv", index=False)

    panel.groupby(["time", "chronic_stress"], as_index=False).agg(
        average_regulation=("regulation_score", "mean"),
        average_regulatory_context=("regulatory_support_context", "mean"),
        average_support=("current_support", "mean"),
        average_structure=("current_structure", "mean"),
        average_sleep=("current_sleep", "mean"),
        average_stress=("acute_stress", "mean"),
        intervention_rate=("intervention_exposure", "mean"),
    ).to_csv(OUT / "generated_regulation_trajectory.csv", index=False)

    print(f"Wrote {DATA / 'regulation_development_panel.csv'} with {len(panel):,} rows")

if __name__ == "__main__":
    main()
