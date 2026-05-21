#!/usr/bin/env python3
"""Generate synthetic aging, adaptation, and later-life development panel data.

The data represent a teaching/research scaffold for modeling later-life
development as path-dependent adaptation shaped by functional ability, social
support, health burden, adaptive strategy, meaning orientation, environmental
accessibility, dignity support, service access, and care context.
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
    n_older_adults: int = 900,
    n_periods: int = 10,
    n_contexts: int = 32,
    seed: int = 2026,
) -> pd.DataFrame:
    rng = np.random.default_rng(seed)

    older_adults = pd.DataFrame({
        "id": np.arange(1, n_older_adults + 1),
        "care_context_id": rng.integers(1, n_contexts + 1, n_older_adults),
        "baseline_adjustment": rng.normal(50, 8, n_older_adults),
        "functional_ability": rng.normal(0, 1, n_older_adults),
        "social_support": rng.normal(0, 1, n_older_adults),
        "health_burden": rng.normal(0, 1, n_older_adults),
        "adaptive_strategy": rng.normal(0, 1, n_older_adults),
        "meaning_orientation": rng.normal(0, 0.8, n_older_adults),
    })

    care_contexts = pd.DataFrame({
        "care_context_id": np.arange(1, n_contexts + 1),
        "environmental_accessibility": rng.normal(0, 0.6, n_contexts),
        "dignity_support": rng.normal(0, 0.6, n_contexts),
        "service_access": rng.normal(0, 0.5, n_contexts),
    })

    panel = older_adults.loc[older_adults.index.repeat(n_periods)].copy()
    panel["time"] = np.tile(np.arange(n_periods), n_older_adults)
    panel = panel.merge(care_contexts, on="care_context_id", how="left")

    panel["current_function"] = rng.normal(
        panel["functional_ability"] - 0.04 * panel["time"],
        0.70,
    )
    panel["current_support"] = rng.normal(panel["social_support"], 0.70)
    panel["current_health"] = rng.normal(
        panel["health_burden"] + 0.05 * panel["time"],
        0.70,
    )
    panel["current_adaptation"] = rng.normal(
        panel["adaptive_strategy"] + 0.03 * panel["time"],
        0.70,
    )
    panel["current_meaning"] = rng.normal(panel["meaning_orientation"], 0.55)

    panel["functional_fit"] = (
        panel["current_function"]
        + panel["environmental_accessibility"]
        + 0.35 * panel["current_function"] * panel["environmental_accessibility"]
    )

    panel = panel.sort_values(["id", "time"]).reset_index(drop=True)
    panel["adjustment_score"] = np.nan

    for _, rows in panel.groupby("id", sort=False):
        previous_score = rows["baseline_adjustment"].iloc[0] + rng.normal(0, 2)

        for idx in rows.index:
            time = panel.at[idx, "time"]
            functional_fit = panel.at[idx, "functional_fit"]
            support = panel.at[idx, "current_support"]
            health = panel.at[idx, "current_health"]
            adaptation = panel.at[idx, "current_adaptation"]
            meaning = panel.at[idx, "current_meaning"]
            dignity = panel.at[idx, "dignity_support"]
            services = panel.at[idx, "service_access"]

            current_score = (
                0.70 * previous_score
                + 0.35 * time
                + 1.15 * functional_fit
                + 1.05 * support
                + 0.95 * adaptation
                + 0.80 * meaning
                + 0.75 * dignity
                + 0.60 * services
                - 1.30 * health
                + rng.normal(0, 2.5)
            )

            panel.at[idx, "adjustment_score"] = current_score
            previous_score = current_score

    person_summary = panel.groupby("id", as_index=False).agg(
        average_functional_fit=("functional_fit", "mean"),
        average_support=("current_support", "mean"),
        average_health=("current_health", "mean"),
        average_adaptation=("current_adaptation", "mean"),
        final_adjustment=("adjustment_score", "last"),
    )

    health_median = person_summary["average_health"].median()
    fit_median = person_summary["average_functional_fit"].median()

    person_summary["adaptation_profile"] = np.select(
        [
            (person_summary["average_functional_fit"] >= fit_median) & (person_summary["average_health"] < health_median),
            (person_summary["average_functional_fit"] >= fit_median) & (person_summary["average_health"] >= health_median),
            (person_summary["average_functional_fit"] < fit_median) & (person_summary["average_health"] < health_median),
        ],
        [
            "higher_fit_lower_health_burden",
            "higher_fit_higher_health_burden",
            "lower_fit_lower_health_burden",
        ],
        default="lower_fit_higher_health_burden",
    )

    panel = panel.merge(
        person_summary[["id", "adaptation_profile"]],
        on="id",
        how="left",
    )

    care_contexts.to_csv(DATA_DIR / "care_context_metadata.csv", index=False)
    person_summary.to_csv(DATA_DIR / "person_aging_adaptation_profiles.csv", index=False)
    return panel


def main() -> None:
    panel = generate_panel()
    panel_path = DATA_DIR / "aging_adaptation_later_life_panel.csv"
    panel.to_csv(panel_path, index=False)

    trajectory = panel.groupby("time", as_index=False).agg(
        average_adjustment=("adjustment_score", "mean"),
        average_functional_fit=("functional_fit", "mean"),
        average_function=("current_function", "mean"),
        average_support=("current_support", "mean"),
        average_health=("current_health", "mean"),
        average_adaptation=("current_adaptation", "mean"),
        average_meaning=("current_meaning", "mean"),
    )
    trajectory.to_csv(OUTPUTS_DIR / "generated_aging_adaptation_trajectory.csv", index=False)

    print(f"Wrote {panel_path}")
    print(f"Rows: {len(panel):,}")
    print(f"Older adults: {panel['id'].nunique():,}")
    print(f"Care contexts: {panel['care_context_id'].nunique():,}")


if __name__ == "__main__":
    main()
