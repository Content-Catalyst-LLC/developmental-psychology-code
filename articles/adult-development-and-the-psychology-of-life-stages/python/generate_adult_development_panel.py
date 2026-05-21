#!/usr/bin/env python3
"""Generate synthetic adult development and life stages panel data.

The data represent a teaching/research scaffold for modeling adult development
as path-dependent change shaped by relational support, work integration,
health burden, adaptive resources, role burden, institutional support,
community stability, and life-stage context.
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
    n_adults: int = 950,
    n_periods: int = 10,
    n_contexts: int = 36,
    seed: int = 2026,
) -> pd.DataFrame:
    rng = np.random.default_rng(seed)

    adults = pd.DataFrame({
        "id": np.arange(1, n_adults + 1),
        "context_id": rng.integers(1, n_contexts + 1, n_adults),
        "baseline_adjustment": rng.normal(50, 8, n_adults),
        "relational_support": rng.normal(0, 1, n_adults),
        "work_integration": rng.normal(0, 1, n_adults),
        "health_burden": rng.normal(0, 1, n_adults),
        "adaptive_resources": rng.normal(0, 1, n_adults),
        "role_burden": rng.normal(0, 1, n_adults),
        "life_stage": rng.choice(
            ["young_adulthood", "midlife", "later_adulthood"],
            size=n_adults,
            p=[0.35, 0.35, 0.30],
        ),
    })

    contexts = pd.DataFrame({
        "context_id": np.arange(1, n_contexts + 1),
        "institutional_support": rng.normal(0, 0.6, n_contexts),
        "community_stability": rng.normal(0, 0.5, n_contexts),
    })

    panel = adults.loc[adults.index.repeat(n_periods)].copy()
    panel["time"] = np.tile(np.arange(n_periods), n_adults)
    panel = panel.merge(contexts, on="context_id", how="left")

    panel["current_relational_support"] = rng.normal(panel["relational_support"], 0.70)
    panel["current_work_integration"] = rng.normal(panel["work_integration"], 0.70)
    panel["current_health_burden"] = rng.normal(
        panel["health_burden"] + 0.03 * panel["time"],
        0.70,
    )
    panel["current_adaptive_resources"] = rng.normal(panel["adaptive_resources"], 0.70)
    panel["current_role_burden"] = rng.normal(panel["role_burden"], 0.70)

    panel["young_stage"] = (panel["life_stage"] == "young_adulthood").astype(int)
    panel["midlife_stage"] = (panel["life_stage"] == "midlife").astype(int)
    panel["later_stage"] = (panel["life_stage"] == "later_adulthood").astype(int)

    panel = panel.sort_values(["id", "time"]).reset_index(drop=True)
    panel["adjustment_score"] = np.nan

    for _, rows in panel.groupby("id", sort=False):
        previous_score = rows["baseline_adjustment"].iloc[0] + rng.normal(0, 2)

        for idx in rows.index:
            time = panel.at[idx, "time"]
            support = panel.at[idx, "current_relational_support"]
            work = panel.at[idx, "current_work_integration"]
            health = panel.at[idx, "current_health_burden"]
            resources = panel.at[idx, "current_adaptive_resources"]
            burden = panel.at[idx, "current_role_burden"]
            institutional = panel.at[idx, "institutional_support"]
            community = panel.at[idx, "community_stability"]
            young = panel.at[idx, "young_stage"]
            midlife = panel.at[idx, "midlife_stage"]
            later = panel.at[idx, "later_stage"]

            current_score = (
                0.70 * previous_score
                + 0.55 * time
                + 1.15 * support
                + 1.05 * work
                + 0.95 * resources
                + 0.70 * institutional
                + 0.55 * community
                - 1.20 * health
                - 0.80 * burden
                + 0.75 * young
                + 0.55 * midlife
                + 0.35 * later
                + 0.25 * support * resources
                + rng.normal(0, 2.5)
            )

            panel.at[idx, "adjustment_score"] = current_score
            previous_score = current_score

    person_summary = panel.groupby("id", as_index=False).agg(
        average_support=("current_relational_support", "mean"),
        average_work=("current_work_integration", "mean"),
        average_health=("current_health_burden", "mean"),
        average_resources=("current_adaptive_resources", "mean"),
        average_role_burden=("current_role_burden", "mean"),
        final_adjustment=("adjustment_score", "last"),
    )

    support_median = person_summary["average_support"].median()
    burden_median = person_summary["average_role_burden"].median()

    person_summary["adult_development_profile"] = np.select(
        [
            (person_summary["average_support"] >= support_median) & (person_summary["average_role_burden"] < burden_median),
            (person_summary["average_support"] >= support_median) & (person_summary["average_role_burden"] >= burden_median),
            (person_summary["average_support"] < support_median) & (person_summary["average_role_burden"] < burden_median),
        ],
        [
            "higher_support_lower_role_burden",
            "higher_support_higher_role_burden",
            "lower_support_lower_role_burden",
        ],
        default="lower_support_higher_role_burden",
    )

    panel = panel.merge(
        person_summary[["id", "adult_development_profile"]],
        on="id",
        how="left",
    )

    contexts.to_csv(DATA_DIR / "context_metadata.csv", index=False)
    person_summary.to_csv(DATA_DIR / "person_adult_development_profiles.csv", index=False)
    return panel


def main() -> None:
    panel = generate_panel()
    panel_path = DATA_DIR / "adult_development_life_stages_panel.csv"
    panel.to_csv(panel_path, index=False)

    trajectory = panel.groupby(["time", "life_stage"], as_index=False).agg(
        average_adjustment=("adjustment_score", "mean"),
        average_support=("current_relational_support", "mean"),
        average_work=("current_work_integration", "mean"),
        average_health=("current_health_burden", "mean"),
        average_resources=("current_adaptive_resources", "mean"),
        average_role_burden=("current_role_burden", "mean"),
    )
    trajectory.to_csv(OUTPUTS_DIR / "generated_adult_development_trajectory.csv", index=False)

    print(f"Wrote {panel_path}")
    print(f"Rows: {len(panel):,}")
    print(f"Adults: {panel['id'].nunique():,}")
    print(f"Contexts: {panel['context_id'].nunique():,}")


if __name__ == "__main__":
    main()
