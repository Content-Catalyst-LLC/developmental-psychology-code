#!/usr/bin/env python3
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
OUT = ROOT / "outputs"
DATA.mkdir(exist_ok=True)
OUT.mkdir(exist_ok=True)

def main(seed=2026):
    rng = np.random.default_rng(seed)
    n_children, n_periods, n_contexts = 900, 10, 40

    children = pd.DataFrame({
        "child_id": np.arange(1, n_children + 1),
        "context_id": rng.integers(1, n_contexts + 1, n_children),
        "baseline_neural_state": rng.normal(50, 7, n_children),
        "family_support": rng.normal(0, 1, n_children),
        "learning_context": rng.normal(0, 1, n_children),
        "sleep_quality": rng.normal(0, 1, n_children),
        "sensory_regulation_support": rng.normal(0, 1, n_children),
        "chronic_stress": rng.binomial(1, 0.30, n_children),
    })

    contexts = pd.DataFrame({
        "context_id": np.arange(1, n_contexts + 1),
        "school_support": rng.normal(0, 0.6, n_contexts),
        "neighborhood_safety": rng.normal(0, 0.6, n_contexts),
        "health_service_access": rng.normal(0, 0.6, n_contexts),
        "environmental_risk": rng.normal(0, 0.6, n_contexts),
    })

    panel = children.loc[children.index.repeat(n_periods)].copy()
    panel["time"] = np.tile(np.arange(n_periods), n_children)
    panel = panel.merge(contexts, on="context_id", how="left")

    panel["current_family_support"] = rng.normal(panel["family_support"], 0.70)
    panel["current_learning"] = rng.normal(panel["learning_context"], 0.70)
    panel["current_sleep"] = rng.normal(panel["sleep_quality"], 0.50)
    panel["current_sensory_support"] = rng.normal(panel["sensory_regulation_support"], 0.50)
    panel["acute_stress"] = rng.normal(0.35 * panel["chronic_stress"], 0.80)

    panel["developmental_support_context"] = (
        panel["current_family_support"] + panel["current_learning"] +
        panel["current_sleep"] + panel["current_sensory_support"] +
        panel["school_support"] + panel["neighborhood_safety"] +
        panel["health_service_access"] - panel["environmental_risk"]
    )

    panel = panel.sort_values(["child_id", "time"]).reset_index(drop=True)
    panel["neural_state"] = np.nan
    panel["developmental_outcome"] = np.nan

    for _, rows in panel.groupby("child_id", sort=False):
        prev = rows["baseline_neural_state"].iloc[0]
        for idx in rows.index:
            r = panel.loc[idx]
            neural = (
                0.70 * prev + 0.85 * r.time - 0.010 * r.time**2
                + 1.15 * r.current_family_support
                + 1.20 * r.current_learning
                + 0.90 * r.current_sleep
                + 0.75 * r.current_sensory_support
                + 0.80 * r.school_support
                + 0.70 * r.neighborhood_safety
                + 0.75 * r.health_service_access
                - 1.30 * r.acute_stress
                - 0.90 * r.chronic_stress
                - 0.70 * r.environmental_risk
                + 0.25 * r.developmental_support_context
                + rng.normal(0, 2.5)
            )
            outcome = (
                0.72 * neural
                + 0.85 * r.current_family_support
                + 0.80 * r.current_learning
                + 0.70 * r.current_sleep
                + 0.65 * r.current_sensory_support
                - 0.95 * r.acute_stress
                - 0.65 * r.environmental_risk
                + rng.normal(0, 2.4)
            )
            panel.at[idx, "neural_state"] = neural
            panel.at[idx, "developmental_outcome"] = outcome
            prev = neural

    profiles = panel.groupby("child_id", as_index=False).agg(
        average_neural_state=("neural_state", "mean"),
        average_developmental_outcome=("developmental_outcome", "mean"),
        average_developmental_support_context=("developmental_support_context", "mean"),
        average_stress=("acute_stress", "mean"),
        chronic_stress=("chronic_stress", "first"),
    )

    support_median = profiles.average_developmental_support_context.median()
    stress_median = profiles.average_stress.median()
    neural_median = profiles.average_neural_state.median()

    profiles["neurodevelopment_profile"] = np.select(
        [
            (profiles.chronic_stress == 1) & (profiles.average_developmental_support_context >= support_median),
            (profiles.chronic_stress == 1) & (profiles.average_developmental_support_context < support_median),
            (profiles.average_stress >= stress_median) & (profiles.average_developmental_support_context < support_median),
            (profiles.average_neural_state >= neural_median) & (profiles.average_developmental_support_context >= support_median),
        ],
        [
            "higher_stress_higher_developmental_support",
            "higher_stress_lower_developmental_support",
            "higher_stress_contextual_strain",
            "higher_neural_state_higher_support",
        ],
        default="lower_stress_or_higher_support",
    )

    panel = panel.merge(profiles[["child_id", "neurodevelopment_profile"]], on="child_id", how="left")

    panel.to_csv(DATA / "brain_development_panel.csv", index=False)
    contexts.to_csv(DATA / "neurodevelopment_context_metadata.csv", index=False)
    profiles.to_csv(DATA / "neurodevelopment_profiles.csv", index=False)
    panel.groupby(["time", "chronic_stress"], as_index=False).agg(
        average_developmental_outcome=("developmental_outcome", "mean"),
        average_neural_state=("neural_state", "mean"),
        average_stress=("acute_stress", "mean"),
        average_support_context=("developmental_support_context", "mean"),
    ).to_csv(OUT / "generated_neurodevelopment_trajectory.csv", index=False)

    print(f"Wrote {DATA / 'brain_development_panel.csv'} with {len(panel):,} rows")

if __name__ == "__main__":
    main()
