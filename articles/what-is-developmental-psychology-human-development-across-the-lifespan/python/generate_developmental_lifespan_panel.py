#!/usr/bin/env python3
"""Generate synthetic developmental psychology lifespan panel data."""

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
    n_children, n_periods, n_schools = 900, 10, 36

    children = pd.DataFrame({
        "child_id": np.arange(1, n_children + 1),
        "school_id": rng.integers(1, n_schools + 1, n_children),
        "baseline_regulation": rng.normal(50, 8, n_children),
        "caregiver_support": rng.normal(0, 1, n_children),
        "family_support": rng.normal(0, 1, n_children),
        "school_support": rng.normal(0, 1, n_children),
        "disability_support_need": rng.binomial(1, 0.18, n_children),
        "structural_risk": rng.binomial(1, 0.35, n_children),
    })

    schools = pd.DataFrame({
        "school_id": np.arange(1, n_schools + 1),
        "school_climate": rng.normal(0, 0.6, n_schools),
        "disability_accommodation": rng.normal(0, 0.6, n_schools),
        "counseling_access": rng.normal(0, 0.5, n_schools),
        "language_access": rng.normal(0, 0.5, n_schools),
        "community_resource_index": rng.normal(0, 0.7, n_schools),
    })

    panel = children.loc[children.index.repeat(n_periods)].copy()
    panel["time"] = np.tile(np.arange(n_periods), n_children)
    panel = panel.merge(schools, on="school_id", how="left")

    panel["acute_stress"] = rng.normal(
        loc=0.35 * panel["structural_risk"] - 0.15 * panel["caregiver_support"],
        scale=0.90,
        size=len(panel),
    )
    panel["current_support"] = rng.normal(
        loc=(
            panel["caregiver_support"]
            + panel["family_support"]
            + panel["school_support"]
            + panel["school_climate"]
            + panel["counseling_access"]
        ),
        scale=0.65,
        size=len(panel),
    )
    panel["intervention"] = (
        (panel["time"] >= 5)
        & (rng.uniform(size=len(panel)) < 0.32)
    ).astype(int)

    panel["protective_context"] = (
        panel["caregiver_support"]
        + panel["family_support"]
        + panel["school_support"]
        + panel["school_climate"]
        + panel["counseling_access"]
        + panel["language_access"]
        + panel["community_resource_index"]
        + panel["disability_accommodation"] * (1 + panel["disability_support_need"])
    )

    panel = panel.sort_values(["child_id", "time"]).reset_index(drop=True)
    panel["development_score"] = np.nan

    for _, rows in panel.groupby("child_id", sort=False):
        previous_score = rows["baseline_regulation"].iloc[0]
        for idx in rows.index:
            row = panel.loc[idx]
            current_score = (
                0.72 * previous_score
                + 0.90 * row.time
                + 1.10 * row.caregiver_support
                + 0.90 * row.family_support
                + 0.85 * row.school_support
                + 0.75 * row.school_climate
                + 0.65 * row.counseling_access
                + 0.55 * row.language_access
                + 0.55 * row.community_resource_index
                + 0.95 * row.disability_accommodation * row.disability_support_need
                - 2.30 * row.structural_risk
                - 1.45 * row.acute_stress
                + 1.80 * row.intervention
                + 0.70 * row.current_support
                + 0.28 * row.protective_context
                + rng.normal(0, 2.5)
            )
            panel.at[idx, "development_score"] = current_score
            previous_score = current_score

    profiles = panel.groupby("child_id", as_index=False).agg(
        average_protective_context=("protective_context", "mean"),
        average_stress=("acute_stress", "mean"),
        average_support=("current_support", "mean"),
        average_development=("development_score", "mean"),
        final_development=("development_score", "last"),
        structural_risk=("structural_risk", "first"),
        disability_support_need=("disability_support_need", "first"),
    )

    protection_median = profiles.average_protective_context.median()
    profiles["development_profile"] = np.select(
        [
            (profiles.structural_risk == 1) & (profiles.average_protective_context >= protection_median),
            (profiles.structural_risk == 1) & (profiles.average_protective_context < protection_median),
            (profiles.disability_support_need == 1) & (profiles.average_protective_context >= protection_median),
            (profiles.disability_support_need == 1) & (profiles.average_protective_context < protection_median),
        ],
        [
            "higher_risk_higher_support",
            "higher_risk_lower_support",
            "support_need_higher_support",
            "support_need_lower_support",
        ],
        default="lower_risk_or_lower_support_need",
    )

    panel = panel.merge(profiles[["child_id", "development_profile"]], on="child_id", how="left")

    panel.to_csv(DATA / "developmental_lifespan_panel.csv", index=False)
    schools.to_csv(DATA / "school_development_context_metadata.csv", index=False)
    profiles.to_csv(DATA / "developmental_profiles.csv", index=False)

    trajectory = panel.groupby(["time", "structural_risk"], as_index=False).agg(
        average_development=("development_score", "mean"),
        average_support=("current_support", "mean"),
        average_stress=("acute_stress", "mean"),
        average_protective_context=("protective_context", "mean"),
    )
    trajectory.to_csv(OUT / "generated_developmental_lifespan_trajectory.csv", index=False)

    print(f"Wrote {DATA / 'developmental_lifespan_panel.csv'} with {len(panel):,} rows")


if __name__ == "__main__":
    main()
