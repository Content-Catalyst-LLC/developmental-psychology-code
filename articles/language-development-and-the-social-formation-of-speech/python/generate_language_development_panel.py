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
        "baseline_language": rng.normal(48, 8, n_children),
        "responsive_interaction": rng.normal(0, 1, n_children),
        "shared_reading": rng.normal(0, 1, n_children),
        "joint_attention": rng.normal(0, 1, n_children),
        "conversational_turns": rng.normal(0, 1, n_children),
        "hearing_support": rng.normal(0, 1, n_children),
        "multilingual_exposure": rng.binomial(1, 0.32, n_children),
        "chronic_stress": rng.binomial(1, 0.28, n_children),
    })

    contexts = pd.DataFrame({
        "context_id": np.arange(1, n_contexts + 1),
        "language_ecology_support": rng.normal(0, 0.6, n_contexts),
        "book_access": rng.normal(0, 0.6, n_contexts),
        "early_education_quality": rng.normal(0, 0.6, n_contexts),
        "home_language_recognition": rng.normal(0, 0.6, n_contexts),
    })

    panel = children.loc[children.index.repeat(n_periods)].copy()
    panel["time"] = np.tile(np.arange(n_periods), n_children)
    panel = panel.merge(contexts, on="context_id", how="left")

    panel["current_interaction"] = rng.normal(panel["responsive_interaction"], 0.70)
    panel["current_reading"] = rng.normal(panel["shared_reading"], 0.70)
    panel["current_joint_attention"] = rng.normal(panel["joint_attention"], 0.70)
    panel["current_turn_taking"] = rng.normal(panel["conversational_turns"], 0.70)
    panel["current_stress"] = rng.normal(0.30 * panel["chronic_stress"], 0.80)

    panel["language_support_context"] = (
        panel["current_interaction"]
        + panel["current_reading"]
        + panel["current_joint_attention"]
        + panel["current_turn_taking"]
        + panel["hearing_support"]
        + panel["language_ecology_support"]
        + panel["book_access"]
        + panel["early_education_quality"]
        + panel["home_language_recognition"]
    )

    panel = panel.sort_values(["child_id", "time"]).reset_index(drop=True)
    panel["language_score"] = np.nan

    for _, rows in panel.groupby("child_id", sort=False):
        previous_score = rows["baseline_language"].iloc[0]
        for idx in rows.index:
            row = panel.loc[idx]
            current_score = (
                0.70 * previous_score
                + 0.95 * row.time
                - 0.015 * (row.time ** 2)
                + 1.30 * row.current_interaction
                + 1.10 * row.current_reading
                + 1.05 * row.current_joint_attention
                + 1.00 * row.current_turn_taking
                + 0.95 * row.hearing_support
                + 0.70 * row.language_ecology_support
                + 0.70 * row.book_access
                + 0.75 * row.early_education_quality
                + 0.65 * row.home_language_recognition
                + 0.50 * row.multilingual_exposure * row.home_language_recognition
                - 1.20 * row.current_stress
                - 0.90 * row.chronic_stress
                + 0.25 * row.language_support_context
                + rng.normal(0, 2.5)
            )
            panel.at[idx, "language_score"] = current_score
            previous_score = current_score

    profiles = panel.groupby("child_id", as_index=False).agg(
        average_language_support_context=("language_support_context", "mean"),
        average_interaction=("current_interaction", "mean"),
        average_reading=("current_reading", "mean"),
        average_joint_attention=("current_joint_attention", "mean"),
        average_turn_taking=("current_turn_taking", "mean"),
        average_stress=("current_stress", "mean"),
        average_language=("language_score", "mean"),
        final_language=("language_score", "last"),
        chronic_stress=("chronic_stress", "first"),
        multilingual_exposure=("multilingual_exposure", "first"),
    )

    support_median = profiles.average_language_support_context.median()
    stress_median = profiles.average_stress.median()

    profiles["language_profile"] = np.select(
        [
            (profiles.chronic_stress == 1) & (profiles.average_language_support_context >= support_median),
            (profiles.chronic_stress == 1) & (profiles.average_language_support_context < support_median),
            (profiles.multilingual_exposure == 1) & (profiles.average_language_support_context >= support_median),
            (profiles.multilingual_exposure == 1) & (profiles.average_language_support_context < support_median),
            (profiles.average_stress >= stress_median) & (profiles.average_language_support_context < support_median),
        ],
        [
            "higher_stress_higher_language_support",
            "higher_stress_lower_language_support",
            "multilingual_higher_recognition_support",
            "multilingual_lower_recognition_support",
            "higher_stress_contextual_strain",
        ],
        default="lower_stress_or_higher_support",
    )

    panel = panel.merge(profiles[["child_id", "language_profile"]], on="child_id", how="left")

    panel.to_csv(DATA / "language_development_panel.csv", index=False)
    contexts.to_csv(DATA / "language_context_metadata.csv", index=False)
    profiles.to_csv(DATA / "language_development_profiles.csv", index=False)

    panel.groupby(["time", "chronic_stress"], as_index=False).agg(
        average_language=("language_score", "mean"),
        average_interaction=("current_interaction", "mean"),
        average_reading=("current_reading", "mean"),
        average_joint_attention=("current_joint_attention", "mean"),
        average_turn_taking=("current_turn_taking", "mean"),
        average_stress=("current_stress", "mean"),
        average_language_support=("language_support_context", "mean"),
    ).to_csv(OUT / "generated_language_trajectory.csv", index=False)

    print(f"Wrote {DATA / 'language_development_panel.csv'} with {len(panel):,} rows")

if __name__ == "__main__":
    main()
