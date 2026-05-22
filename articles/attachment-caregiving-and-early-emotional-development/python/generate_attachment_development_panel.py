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
    n_children, n_periods, n_contexts = 900, 10, 36

    children = pd.DataFrame({
        "child_id": np.arange(1, n_children + 1),
        "context_id": rng.integers(1, n_contexts + 1, n_children),
        "baseline_regulation": rng.normal(50, 8, n_children),
        "caregiving_quality": rng.normal(0, 1, n_children),
        "repair_capacity": rng.normal(0, 1, n_children),
        "caregiver_support": rng.normal(0, 1, n_children),
        "temperament_reactivity": rng.normal(0, 1, n_children),
        "disability_support_need": rng.binomial(1, 0.16, n_children),
        "chronic_stress": rng.binomial(1, 0.30, n_children),
    })

    contexts = pd.DataFrame({
        "context_id": np.arange(1, n_contexts + 1),
        "childcare_continuity": rng.normal(0, 0.6, n_contexts),
        "neighborhood_safety": rng.normal(0, 0.6, n_contexts),
        "family_service_access": rng.normal(0, 0.6, n_contexts),
        "caregiving_ecology_support": rng.normal(0, 0.6, n_contexts),
    })

    panel = children.loc[children.index.repeat(n_periods)].copy()
    panel["time"] = np.tile(np.arange(n_periods), n_children)
    panel = panel.merge(contexts, on="context_id", how="left")

    panel["current_care"] = rng.normal(panel["caregiving_quality"], 0.70)
    panel["current_repair"] = rng.normal(panel["repair_capacity"], 0.70)
    panel["current_caregiver_support"] = rng.normal(panel["caregiver_support"], 0.70)
    panel["current_stress"] = rng.normal(0.35 * panel["chronic_stress"], 0.80)

    panel["caregiving_support_context"] = (
        panel["current_care"]
        + panel["current_repair"]
        + panel["current_caregiver_support"]
        + panel["childcare_continuity"]
        + panel["neighborhood_safety"]
        + panel["family_service_access"]
        + panel["caregiving_ecology_support"]
    )

    panel = panel.sort_values(["child_id", "time"]).reset_index(drop=True)
    panel["regulation_score"] = np.nan

    for _, rows in panel.groupby("child_id", sort=False):
        previous_score = rows["baseline_regulation"].iloc[0]
        for idx in rows.index:
            row = panel.loc[idx]
            current_score = (
                0.70 * previous_score
                + 0.90 * row.time
                + 1.35 * row.current_care
                + 1.10 * row.current_repair
                + 1.00 * row.current_caregiver_support
                + 0.80 * row.childcare_continuity
                + 0.75 * row.neighborhood_safety
                + 0.80 * row.family_service_access
                + 0.75 * row.caregiving_ecology_support
                - 1.30 * row.current_stress
                - 0.95 * row.chronic_stress
                + 0.75 * row.temperament_reactivity * row.current_care
                - 0.85 * row.temperament_reactivity * row.current_stress
                + 0.70 * row.disability_support_need * row.family_service_access
                + 0.25 * row.caregiving_support_context
                + rng.normal(0, 2.5)
            )
            panel.at[idx, "regulation_score"] = current_score
            previous_score = current_score

    profiles = panel.groupby("child_id", as_index=False).agg(
        average_caregiving_support_context=("caregiving_support_context", "mean"),
        average_care=("current_care", "mean"),
        average_repair=("current_repair", "mean"),
        average_stress=("current_stress", "mean"),
        average_regulation=("regulation_score", "mean"),
        final_regulation=("regulation_score", "last"),
        chronic_stress=("chronic_stress", "first"),
        disability_support_need=("disability_support_need", "first"),
    )

    support_median = profiles.average_caregiving_support_context.median()
    stress_median = profiles.average_stress.median()

    profiles["attachment_profile"] = np.select(
        [
            (profiles.chronic_stress == 1) & (profiles.average_caregiving_support_context >= support_median),
            (profiles.chronic_stress == 1) & (profiles.average_caregiving_support_context < support_median),
            (profiles.disability_support_need == 1) & (profiles.average_caregiving_support_context >= support_median),
            (profiles.disability_support_need == 1) & (profiles.average_caregiving_support_context < support_median),
            (profiles.average_stress >= stress_median) & (profiles.average_caregiving_support_context < support_median),
        ],
        [
            "higher_stress_higher_caregiving_support",
            "higher_stress_lower_caregiving_support",
            "support_need_higher_caregiving_support",
            "support_need_lower_caregiving_support",
            "higher_stress_contextual_strain",
        ],
        default="lower_stress_or_higher_support",
    )

    panel = panel.merge(profiles[["child_id", "attachment_profile"]], on="child_id", how="left")

    panel.to_csv(DATA / "attachment_development_panel.csv", index=False)
    contexts.to_csv(DATA / "attachment_context_metadata.csv", index=False)
    profiles.to_csv(DATA / "attachment_development_profiles.csv", index=False)

    panel.groupby(["time", "chronic_stress"], as_index=False).agg(
        average_regulation=("regulation_score", "mean"),
        average_care=("current_care", "mean"),
        average_repair=("current_repair", "mean"),
        average_caregiver_support=("current_caregiver_support", "mean"),
        average_stress=("current_stress", "mean"),
        average_support_context=("caregiving_support_context", "mean"),
    ).to_csv(OUT / "generated_attachment_trajectory.csv", index=False)

    print(f"Wrote {DATA / 'attachment_development_panel.csv'} with {len(panel):,} rows")

if __name__ == "__main__":
    main()
