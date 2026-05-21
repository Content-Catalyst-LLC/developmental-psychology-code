#!/usr/bin/env python3
"""Generate a synthetic longitudinal developmental psychology panel dataset.

The dataset is designed for reproducible demonstration. It does not represent
real persons, real schools, real clinics, or real communities.
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
    n_people: int = 1000,
    n_periods: int = 10,
    n_contexts: int = 36,
    seed: int = 2026,
) -> pd.DataFrame:
    """Create synthetic person-period data with contextual nesting."""

    rng = np.random.default_rng(seed)

    people = pd.DataFrame(
        {
            "person_id": np.arange(1, n_people + 1),
            "context_id": rng.integers(1, n_contexts + 1, size=n_people),
            "baseline_support": rng.normal(0, 1, n_people),
            "baseline_risk": rng.normal(0, 1, n_people),
            "baseline_policy_access": rng.normal(0, 1, n_people),
            "baseline_health": rng.normal(0, 1, n_people),
            "person_resilience": rng.normal(0, 0.7, n_people),
        }
    )

    contexts = pd.DataFrame(
        {
            "context_id": np.arange(1, n_contexts + 1),
            "institutional_climate": rng.normal(0, 0.65, n_contexts),
            "resource_level": rng.normal(0, 0.75, n_contexts),
        }
    )

    panel = people.loc[people.index.repeat(n_periods)].copy()
    panel["time"] = np.tile(np.arange(n_periods), n_people)
    panel = panel.merge(contexts, on="context_id", how="left")

    panel["current_support"] = rng.normal(panel["baseline_support"], 0.55)
    panel["current_risk"] = rng.normal(panel["baseline_risk"], 0.65)
    panel["policy_access"] = rng.normal(panel["baseline_policy_access"], 0.60)
    panel["health_status"] = rng.normal(panel["baseline_health"], 0.50)

    panel = panel.sort_values(["person_id", "time"]).reset_index(drop=True)
    panel["development_score"] = np.nan

    for person_id, group in panel.groupby("person_id", sort=False):
        previous_score = 50 + rng.normal(0, 3)

        for idx in group.index:
            time = panel.at[idx, "time"]
            support = panel.at[idx, "current_support"]
            risk = panel.at[idx, "current_risk"]
            policy = panel.at[idx, "policy_access"]
            health = panel.at[idx, "health_status"]
            climate = panel.at[idx, "institutional_climate"]
            resources = panel.at[idx, "resource_level"]
            resilience = panel.at[idx, "person_resilience"]

            current_score = (
                0.68 * previous_score
                + 0.22 * time
                + 1.15 * support
                - 1.20 * risk
                + 0.95 * policy
                + 0.80 * health
                + 0.85 * climate
                + 0.60 * resources
                + 0.70 * resilience
                + rng.normal(0, 2.1)
            )

            panel.at[idx, "development_score"] = current_score
            previous_score = current_score

    contexts.to_csv(DATA_DIR / "context_metadata.csv", index=False)
    return panel


def main() -> None:
    panel = generate_panel()
    output_path = DATA_DIR / "developmental_panel.csv"
    panel.to_csv(output_path, index=False)

    summary = panel.groupby("time", as_index=False).agg(
        average_development=("development_score", "mean"),
        average_support=("current_support", "mean"),
        average_risk=("current_risk", "mean"),
        average_policy_access=("policy_access", "mean"),
    )
    summary.to_csv(OUTPUTS_DIR / "generated_panel_summary.csv", index=False)

    print(f"Wrote synthetic panel dataset: {output_path}")
    print(f"Rows: {len(panel):,}")
    print(f"People: {panel['person_id'].nunique():,}")
    print(f"Contexts: {panel['context_id'].nunique():,}")


if __name__ == "__main__":
    main()
