#!/usr/bin/env python3
"""Generate synthetic wisdom, meaning, and later-life development panel data.

The data represent a teaching/research scaffold for modeling later-life meaning
as a path-dependent developmental process shaped by social connection,
reflective integration, health burden, adaptive support, legacy orientation,
dignity support, service access, community participation, and care context.
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
    n_contexts: int = 30,
    seed: int = 2026,
) -> pd.DataFrame:
    rng = np.random.default_rng(seed)

    older_adults = pd.DataFrame({
        "id": np.arange(1, n_older_adults + 1),
        "care_context_id": rng.integers(1, n_contexts + 1, n_older_adults),
        "baseline_meaning": rng.normal(50, 8, n_older_adults),
        "social_connection": rng.normal(0, 1, n_older_adults),
        "reflective_integration": rng.normal(0, 1, n_older_adults),
        "health_burden": rng.normal(0, 1, n_older_adults),
        "adaptive_support": rng.normal(0, 1, n_older_adults),
        "legacy_orientation": rng.normal(0, 0.8, n_older_adults),
    })

    care_contexts = pd.DataFrame({
        "care_context_id": np.arange(1, n_contexts + 1),
        "dignity_support": rng.normal(0, 0.6, n_contexts),
        "service_access": rng.normal(0, 0.5, n_contexts),
        "community_participation": rng.normal(0, 0.5, n_contexts),
    })

    panel = older_adults.loc[older_adults.index.repeat(n_periods)].copy()
    panel["time"] = np.tile(np.arange(n_periods), n_older_adults)
    panel = panel.merge(care_contexts, on="care_context_id", how="left")

    panel["current_connection"] = rng.normal(panel["social_connection"], 0.70)
    panel["current_reflection"] = rng.normal(panel["reflective_integration"], 0.70)
    panel["current_health"] = rng.normal(panel["health_burden"], 0.70)
    panel["current_support"] = rng.normal(panel["adaptive_support"], 0.70)
    panel["current_legacy"] = rng.normal(panel["legacy_orientation"], 0.55)

    panel["wisdom_index"] = (
        0.35 * panel["current_reflection"]
        + 0.25 * panel["current_connection"]
        + 0.20 * panel["current_legacy"]
        + 0.20 * panel["dignity_support"]
        - 0.20 * panel["current_health"]
    )

    panel = panel.sort_values(["id", "time"]).reset_index(drop=True)
    panel["meaning_score"] = np.nan

    for _, rows in panel.groupby("id", sort=False):
        previous_score = rows["baseline_meaning"].iloc[0] + rng.normal(0, 2)

        for idx in rows.index:
            time = panel.at[idx, "time"]
            connection = panel.at[idx, "current_connection"]
            reflection = panel.at[idx, "current_reflection"]
            health = panel.at[idx, "current_health"]
            support = panel.at[idx, "current_support"]
            legacy = panel.at[idx, "current_legacy"]
            dignity = panel.at[idx, "dignity_support"]
            services = panel.at[idx, "service_access"]
            community = panel.at[idx, "community_participation"]
            wisdom = panel.at[idx, "wisdom_index"]

            current_score = (
                0.70 * previous_score
                + 0.35 * time
                + 1.10 * connection
                + 1.05 * reflection
                + 0.90 * support
                + 0.75 * legacy
                + 0.75 * dignity
                + 0.60 * services
                + 0.55 * community
                - 1.15 * health
                + 0.85 * wisdom
                + rng.normal(0, 2.5)
            )

            panel.at[idx, "meaning_score"] = current_score
            previous_score = current_score

    person_summary = panel.groupby("id", as_index=False).agg(
        average_connection=("current_connection", "mean"),
        average_reflection=("current_reflection", "mean"),
        average_health=("current_health", "mean"),
        average_support=("current_support", "mean"),
        average_wisdom=("wisdom_index", "mean"),
        final_meaning=("meaning_score", "last"),
    )

    health_median = person_summary["average_health"].median()

    person_summary["meaning_profile"] = np.select(
        [
            (person_summary["average_connection"] >= 0) & (person_summary["average_health"] < health_median),
            (person_summary["average_connection"] >= 0) & (person_summary["average_health"] >= health_median),
            (person_summary["average_connection"] < 0) & (person_summary["average_health"] < health_median),
        ],
        [
            "higher_connection_lower_health_burden",
            "higher_connection_higher_health_burden",
            "lower_connection_lower_health_burden",
        ],
        default="lower_connection_higher_health_burden",
    )

    panel = panel.merge(
        person_summary[["id", "meaning_profile"]],
        on="id",
        how="left",
    )

    care_contexts.to_csv(DATA_DIR / "care_context_metadata.csv", index=False)
    person_summary.to_csv(DATA_DIR / "person_wisdom_meaning_profiles.csv", index=False)
    return panel


def main() -> None:
    panel = generate_panel()
    panel_path = DATA_DIR / "wisdom_meaning_later_life_panel.csv"
    panel.to_csv(panel_path, index=False)

    trajectory = panel.groupby("time", as_index=False).agg(
        average_meaning=("meaning_score", "mean"),
        average_wisdom=("wisdom_index", "mean"),
        average_connection=("current_connection", "mean"),
        average_reflection=("current_reflection", "mean"),
        average_health=("current_health", "mean"),
        average_support=("current_support", "mean"),
    )
    trajectory.to_csv(OUTPUTS_DIR / "generated_wisdom_meaning_trajectory.csv", index=False)

    print(f"Wrote {panel_path}")
    print(f"Rows: {len(panel):,}")
    print(f"Older adults: {panel['id'].nunique():,}")
    print(f"Care contexts: {panel['care_context_id'].nunique():,}")


if __name__ == "__main__":
    main()
