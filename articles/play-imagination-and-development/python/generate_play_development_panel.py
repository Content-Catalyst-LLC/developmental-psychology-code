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
        "baseline_development": rng.normal(50, 8, n_children),
        "pretend_play_base": rng.normal(0, 1, n_children),
        "social_play_base": rng.normal(0, 1, n_children),
        "constructive_play_base": rng.normal(0, 1, n_children),
        "outdoor_play_base": rng.normal(0, 1, n_children),
        "caregiver_support_base": rng.normal(0, 1, n_children),
        "chronic_stress": rng.binomial(1, 0.30, n_children),
    })

    contexts = pd.DataFrame({
        "context_id": np.arange(1, n_contexts + 1),
        "play_space_quality": rng.normal(0, 0.6, n_contexts),
        "adult_responsiveness": rng.normal(0, 0.6, n_contexts),
        "inclusion_climate": rng.normal(0, 0.6, n_contexts),
        "outdoor_safety": rng.normal(0, 0.6, n_contexts),
        "play_material_access": rng.normal(0, 0.5, n_contexts),
    })

    panel = children.loc[children.index.repeat(n_periods)].copy()
    panel["time"] = np.tile(np.arange(n_periods), n_children)
    panel = panel.merge(contexts, on="context_id", how="left")

    panel["current_pretend"] = rng.normal(panel["pretend_play_base"], 0.70)
    panel["current_social_play"] = rng.normal(panel["social_play_base"], 0.70)
    panel["current_constructive"] = rng.normal(panel["constructive_play_base"], 0.70)
    panel["current_outdoor"] = rng.normal(panel["outdoor_play_base"], 0.70)
    panel["current_support"] = rng.normal(panel["caregiver_support_base"], 0.70)
    panel["current_stress"] = rng.normal(0.35 * panel["chronic_stress"], 0.80)

    panel["play_restriction"] = rng.normal(
        0.35 * panel["chronic_stress"]
        - 0.20 * panel["play_space_quality"]
        - 0.20 * panel["outdoor_safety"],
        0.70,
    )

    panel["peer_inclusion"] = rng.normal(
        0.35 * panel["inclusion_climate"]
        + 0.25 * panel["current_social_play"]
        - 0.20 * panel["play_restriction"],
        0.70,
    )

    panel["play_support_context"] = (
        panel["current_support"]
        + panel["peer_inclusion"]
        + panel["play_space_quality"]
        + panel["adult_responsiveness"]
        + panel["inclusion_climate"]
        + panel["outdoor_safety"]
        + panel["play_material_access"]
    )

    panel = panel.sort_values(["child_id", "time"]).reset_index(drop=True)
    panel["development_score"] = np.nan

    for _, rows in panel.groupby("child_id", sort=False):
        previous_score = rows["baseline_development"].iloc[0]
        for idx in rows.index:
            row = panel.loc[idx]
            current_score = (
                0.70 * previous_score
                + 0.85 * row.time
                + 1.15 * row.current_pretend
                + 1.05 * row.current_social_play
                + 1.00 * row.current_constructive
                + 0.90 * row.current_outdoor
                + 1.00 * row.current_support
                + 0.90 * row.peer_inclusion
                + 0.75 * row.play_space_quality
                + 0.70 * row.adult_responsiveness
                + 0.65 * row.outdoor_safety
                + 0.65 * row.play_material_access
                - 1.15 * row.current_stress
                - 0.90 * row.chronic_stress
                - 0.90 * row.play_restriction
                + 0.25 * row.play_support_context
                + rng.normal(0, 2.5)
            )
            panel.at[idx, "development_score"] = current_score
            previous_score = current_score

    profiles = panel.groupby("child_id", as_index=False).agg(
        average_play_support_context=("play_support_context", "mean"),
        average_play_restriction=("play_restriction", "mean"),
        average_stress=("current_stress", "mean"),
        average_peer_inclusion=("peer_inclusion", "mean"),
        average_development=("development_score", "mean"),
        final_development=("development_score", "last"),
        chronic_stress=("chronic_stress", "first"),
    )

    support_median = profiles.average_play_support_context.median()
    restriction_median = profiles.average_play_restriction.median()
    profiles["play_profile"] = np.select(
        [
            (profiles.chronic_stress == 1) & (profiles.average_play_support_context >= support_median),
            (profiles.chronic_stress == 1) & (profiles.average_play_support_context < support_median),
            (profiles.average_play_restriction >= restriction_median) & (profiles.average_play_support_context >= support_median),
            (profiles.average_play_restriction >= restriction_median) & (profiles.average_play_support_context < support_median),
        ],
        [
            "higher_stress_higher_play_support",
            "higher_stress_lower_play_support",
            "higher_restriction_higher_play_support",
            "higher_restriction_lower_play_support",
        ],
        default="lower_stress_or_restriction",
    )

    panel = panel.merge(profiles[["child_id", "play_profile"]], on="child_id", how="left")

    panel.to_csv(DATA / "play_development_panel.csv", index=False)
    contexts.to_csv(DATA / "play_context_metadata.csv", index=False)
    profiles.to_csv(DATA / "play_development_profiles.csv", index=False)

    panel.groupby(["time", "chronic_stress"], as_index=False).agg(
        average_development=("development_score", "mean"),
        average_pretend=("current_pretend", "mean"),
        average_social_play=("current_social_play", "mean"),
        average_constructive=("current_constructive", "mean"),
        average_outdoor=("current_outdoor", "mean"),
        average_stress=("current_stress", "mean"),
        average_restriction=("play_restriction", "mean"),
        average_peer_inclusion=("peer_inclusion", "mean"),
        average_play_support_context=("play_support_context", "mean"),
    ).to_csv(OUT / "generated_play_development_trajectory.csv", index=False)

    print(f"Wrote {DATA / 'play_development_panel.csv'} with {len(panel):,} rows")

if __name__ == "__main__":
    main()
