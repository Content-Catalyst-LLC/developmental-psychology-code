#!/usr/bin/env python3
"""Generate synthetic developmental psychopathology panel data.

The data represent a teaching/research scaffold for developmental
psychopathology concepts: risk, resilience, adaptation, internalizing pathways,
externalizing pathways, cumulative exposure, protective support, and context.
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
    n_children: int = 850,
    n_periods: int = 10,
    n_contexts: int = 36,
    seed: int = 2026,
) -> pd.DataFrame:
    rng = np.random.default_rng(seed)

    children = pd.DataFrame({
        "child_id": np.arange(1, n_children + 1),
        "context_id": rng.integers(1, n_contexts + 1, n_children),
        "baseline_regulation": rng.normal(0, 1, n_children),
        "protective_support": rng.normal(0, 1, n_children),
        "accumulated_risk": rng.normal(0, 1, n_children),
        "caregiver_stability": rng.normal(0, 1, n_children),
        "biological_sensitivity": rng.normal(0, 0.7, n_children),
    })

    contexts = pd.DataFrame({
        "context_id": np.arange(1, n_contexts + 1),
        "community_support": rng.normal(0, 0.6, n_contexts),
        "school_belonging": rng.normal(0, 0.6, n_contexts),
        "service_access": rng.normal(0, 0.5, n_contexts),
    })

    panel = children.loc[children.index.repeat(n_periods)].copy()
    panel["time"] = np.tile(np.arange(n_periods), n_children)
    panel["timing_weight"] = np.exp(-0.16 * panel["time"])
    panel["transition_weight"] = np.exp(-((panel["time"] - 6) ** 2) / (2 * 1.8**2))
    panel = panel.merge(contexts, on="context_id", how="left")

    panel["current_support"] = rng.normal(
        panel["protective_support"] + 0.15 * panel["service_access"], 0.60
    )
    panel["current_risk"] = rng.normal(panel["accumulated_risk"], 0.70)
    panel["current_stability"] = rng.normal(
        panel["caregiver_stability"] + 0.15 * panel["school_belonging"], 0.60
    )
    panel["current_regulation"] = rng.normal(panel["baseline_regulation"], 0.55)

    panel = panel.sort_values(["child_id", "time"]).reset_index(drop=True)
    panel["weighted_risk"] = panel["current_risk"] * panel["timing_weight"]
    panel["transition_support"] = panel["current_support"] * panel["transition_weight"]
    panel["cumulative_risk"] = panel.groupby("child_id")["weighted_risk"].cumsum()
    panel["cumulative_support"] = panel.groupby("child_id")["current_support"].cumsum()

    panel["adaptation_score"] = np.nan
    panel["internalizing_score"] = np.nan
    panel["externalizing_score"] = np.nan

    for _, rows in panel.groupby("child_id", sort=False):
        prev_adaptation = 50 + rng.normal(0, 3)
        prev_internalizing = 45 + rng.normal(0, 3)
        prev_externalizing = 45 + rng.normal(0, 3)

        for idx in rows.index:
            risk = panel.at[idx, "current_risk"]
            support = panel.at[idx, "current_support"]
            stability = panel.at[idx, "current_stability"]
            regulation = panel.at[idx, "current_regulation"]
            community = panel.at[idx, "community_support"]
            school = panel.at[idx, "school_belonging"]
            services = panel.at[idx, "service_access"]
            timing = panel.at[idx, "timing_weight"]
            cumulative_risk = panel.at[idx, "cumulative_risk"]
            transition_support = panel.at[idx, "transition_support"]
            sensitivity = panel.at[idx, "biological_sensitivity"]
            time = panel.at[idx, "time"]

            adaptation = (
                0.70 * prev_adaptation
                + 0.20 * time
                + 0.75 * regulation
                + 1.10 * support
                + 1.00 * stability
                + 0.85 * community
                + 0.75 * school
                + 0.65 * services
                + 0.70 * transition_support
                - 0.85 * cumulative_risk
                - 1.10 * risk * timing
                + 0.60 * sensitivity * support
                + 0.75 * support * stability
                + rng.normal(0, 2.3)
            )

            internalizing = (
                0.64 * prev_internalizing
                + 0.95 * risk * timing
                + 0.55 * cumulative_risk
                - 0.70 * support
                - 0.55 * stability
                - 0.45 * services
                - 0.45 * regulation
                + 0.40 * sensitivity
                + rng.normal(0, 2.1)
                + 30
            )

            externalizing = (
                0.62 * prev_externalizing
                + 0.85 * risk * timing
                + 0.45 * cumulative_risk
                - 0.65 * support
                - 0.70 * stability
                - 0.50 * school
                - 0.60 * regulation
                + 0.35 * sensitivity
                + rng.normal(0, 2.2)
                + 30
            )

            panel.at[idx, "adaptation_score"] = adaptation
            panel.at[idx, "internalizing_score"] = internalizing
            panel.at[idx, "externalizing_score"] = externalizing

            prev_adaptation = adaptation
            prev_internalizing = internalizing
            prev_externalizing = externalizing

    child_summary = panel.groupby("child_id", as_index=False).agg(
        average_risk=("current_risk", "mean"),
        average_support=("current_support", "mean"),
        average_stability=("current_stability", "mean"),
        final_adaptation=("adaptation_score", "last"),
        final_internalizing=("internalizing_score", "last"),
        final_externalizing=("externalizing_score", "last"),
    )

    child_summary["risk_support_profile"] = np.select(
        [
            (child_summary["average_risk"] < 0) & (child_summary["average_support"] >= 0),
            (child_summary["average_risk"] >= 0) & (child_summary["average_support"] >= 0),
            (child_summary["average_risk"] < 0) & (child_summary["average_support"] < 0),
        ],
        [
            "lower_risk_higher_support",
            "higher_risk_higher_support",
            "lower_risk_lower_support",
        ],
        default="higher_risk_lower_support",
    )

    panel = panel.merge(
        child_summary[["child_id", "risk_support_profile"]],
        on="child_id",
        how="left",
    )

    contexts.to_csv(DATA_DIR / "context_metadata.csv", index=False)
    child_summary.to_csv(DATA_DIR / "child_risk_support_profiles.csv", index=False)
    return panel


def main() -> None:
    panel = generate_panel()
    panel_path = DATA_DIR / "developmental_psychopathology_panel.csv"
    panel.to_csv(panel_path, index=False)

    trajectory = panel.groupby("time", as_index=False).agg(
        average_adaptation=("adaptation_score", "mean"),
        average_internalizing=("internalizing_score", "mean"),
        average_externalizing=("externalizing_score", "mean"),
        average_risk=("current_risk", "mean"),
        average_support=("current_support", "mean"),
        average_cumulative_risk=("cumulative_risk", "mean"),
    )
    trajectory.to_csv(OUTPUTS_DIR / "generated_psychopathology_trajectory.csv", index=False)

    print(f"Wrote {panel_path}")
    print(f"Rows: {len(panel):,}")
    print(f"Children: {panel['child_id'].nunique():,}")
    print(f"Contexts: {panel['context_id'].nunique():,}")


if __name__ == "__main__":
    main()
