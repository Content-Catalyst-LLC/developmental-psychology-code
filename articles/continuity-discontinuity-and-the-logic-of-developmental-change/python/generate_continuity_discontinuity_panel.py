#!/usr/bin/env python3
"""Generate synthetic continuity/discontinuity developmental-change panel data.

The data represent a teaching/research scaffold for modeling development as a
combination of continuous growth, nonlinear curvature, threshold-sensitive
transition, logistic transition, context support, chronic stress, intervention
exposure, institutional rupture, and transition readiness.
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


def logistic(x: np.ndarray, k: float = 1.35) -> np.ndarray:
    return 1.0 / (1.0 + np.exp(-k * x))


def generate_panel(
    n_people: int = 950,
    n_periods: int = 10,
    n_contexts: int = 36,
    seed: int = 2026,
) -> pd.DataFrame:
    rng = np.random.default_rng(seed)

    people = pd.DataFrame({
        "person_id": np.arange(1, n_people + 1),
        "context_id": rng.integers(1, n_contexts + 1, n_people),
        "baseline_functioning": rng.normal(45, 7, n_people),
        "growth_rate": rng.normal(1.80, 0.50, n_people),
        "curvature": rng.normal(0.03, 0.04, n_people),
        "support_context": rng.normal(0, 1, n_people),
        "chronic_stress": rng.binomial(1, 0.30, n_people),
        "institutional_rupture": rng.binomial(1, 0.18, n_people),
        "intervention_exposure": rng.binomial(1, 0.35, n_people),
        "threshold_time": rng.integers(4, 8, n_people),
        "threshold_sensitive": rng.binomial(1, 0.45, n_people),
    })

    contexts = pd.DataFrame({
        "context_id": np.arange(1, n_contexts + 1),
        "school_support": rng.normal(0, 0.6, n_contexts),
        "resource_stability": rng.normal(0, 0.5, n_contexts),
    })

    panel = people.loc[people.index.repeat(n_periods)].copy()
    panel["time"] = np.tile(np.arange(n_periods), n_people)
    panel = panel.merge(contexts, on="context_id", how="left")

    panel["current_support"] = rng.normal(panel["support_context"], 0.70)
    panel["threshold_on"] = (panel["time"] >= panel["threshold_time"]).astype(int)
    panel["logistic_transition"] = logistic(panel["time"] - panel["threshold_time"])

    panel["transition_readiness"] = (
        panel["current_support"]
        + panel["school_support"]
        + panel["resource_stability"]
        + 0.85 * panel["intervention_exposure"]
        - 0.75 * panel["chronic_stress"]
        - 0.80 * panel["institutional_rupture"]
    )

    panel = panel.sort_values(["person_id", "time"]).reset_index(drop=True)
    panel["development_score"] = np.nan

    for _, rows in panel.groupby("person_id", sort=False):
        previous_score = rows["baseline_functioning"].iloc[0]

        for idx in rows.index:
            time = panel.at[idx, "time"]
            baseline = panel.at[idx, "baseline_functioning"]
            growth_rate = panel.at[idx, "growth_rate"]
            curvature = panel.at[idx, "curvature"]
            support = panel.at[idx, "current_support"]
            stress = panel.at[idx, "chronic_stress"]
            rupture = panel.at[idx, "institutional_rupture"]
            intervention = panel.at[idx, "intervention_exposure"]
            school_support = panel.at[idx, "school_support"]
            stability = panel.at[idx, "resource_stability"]
            threshold_on = panel.at[idx, "threshold_on"]
            logistic_transition = panel.at[idx, "logistic_transition"]
            threshold_sensitive = panel.at[idx, "threshold_sensitive"]
            readiness = panel.at[idx, "transition_readiness"]

            continuous_component = baseline + growth_rate * time + curvature * (time ** 2)

            current_score = (
                0.58 * previous_score
                + 0.42 * continuous_component
                + 1.25 * support
                + 0.90 * school_support
                + 0.70 * stability
                + 1.30 * intervention
                - 2.00 * stress
                - 2.40 * rupture
                + 3.10 * threshold_on * threshold_sensitive
                + 2.10 * logistic_transition * threshold_sensitive
                + 0.75 * threshold_on * threshold_sensitive * readiness
                + rng.normal(0, 2.6)
            )

            panel.at[idx, "development_score"] = current_score
            previous_score = current_score

    profile = panel.groupby("person_id", as_index=False).agg(
        average_transition_readiness=("transition_readiness", "mean"),
        average_score=("development_score", "mean"),
        final_score=("development_score", "last"),
        threshold_sensitive=("threshold_sensitive", "first"),
        threshold_time=("threshold_time", "first"),
        chronic_stress=("chronic_stress", "first"),
        institutional_rupture=("institutional_rupture", "first"),
        intervention_exposure=("intervention_exposure", "first"),
    )

    readiness_median = profile["average_transition_readiness"].median()
    profile["change_profile"] = np.select(
        [
            (profile["threshold_sensitive"] == 1) & (profile["average_transition_readiness"] >= readiness_median),
            (profile["threshold_sensitive"] == 1) & (profile["average_transition_readiness"] < readiness_median),
            (profile["threshold_sensitive"] == 0) & (profile["average_transition_readiness"] >= readiness_median),
        ],
        [
            "threshold_sensitive_higher_readiness",
            "threshold_sensitive_lower_readiness",
            "continuous_higher_readiness",
        ],
        default="continuous_lower_readiness",
    )

    panel = panel.merge(profile[["person_id", "change_profile"]], on="person_id", how="left")

    contexts.to_csv(DATA_DIR / "context_metadata.csv", index=False)
    profile.to_csv(DATA_DIR / "developmental_change_profiles.csv", index=False)
    return panel


def main() -> None:
    panel = generate_panel()
    panel_path = DATA_DIR / "continuity_discontinuity_panel.csv"
    panel.to_csv(panel_path, index=False)

    trajectory = panel.groupby(["time", "threshold_sensitive"], as_index=False).agg(
        average_score=("development_score", "mean"),
        average_readiness=("transition_readiness", "mean"),
        average_support=("current_support", "mean"),
        average_logistic_transition=("logistic_transition", "mean"),
        average_stress=("chronic_stress", "mean"),
        average_rupture=("institutional_rupture", "mean"),
        average_intervention=("intervention_exposure", "mean"),
    )
    trajectory.to_csv(OUTPUTS_DIR / "generated_continuity_discontinuity_trajectory.csv", index=False)

    print(f"Wrote {panel_path}")
    print(f"Rows: {len(panel):,}")
    print(f"Individuals: {panel['person_id'].nunique():,}")
    print(f"Contexts: {panel['context_id'].nunique():,}")


if __name__ == "__main__":
    main()
