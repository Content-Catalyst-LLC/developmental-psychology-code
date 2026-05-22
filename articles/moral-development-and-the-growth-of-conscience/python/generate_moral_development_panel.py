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
    n_children, n_periods, n_schools = 920, 10, 36

    children = pd.DataFrame({
        "child_id": np.arange(1, n_children + 1),
        "school_id": rng.integers(1, n_schools + 1, n_children),
        "baseline_morality": rng.normal(50, 8, n_children),
        "caregiving_guidance": rng.normal(0, 1, n_children),
        "empathic_sensitivity": rng.normal(0, 1, n_children),
        "peer_fairness_base": rng.normal(0, 1, n_children),
        "self_regulation": rng.normal(0, 1, n_children),
        "harm_recognition_base": rng.normal(0, 1, n_children),
        "chronic_exclusion": rng.binomial(1, 0.22, n_children),
    })

    schools = pd.DataFrame({
        "school_id": np.arange(1, n_schools + 1),
        "school_moral_climate": rng.normal(0, 0.6, n_schools),
        "restorative_practice_access": rng.normal(0, 0.6, n_schools),
        "punitive_inconsistency": rng.normal(0, 0.6, n_schools),
        "anti_bullying_climate": rng.normal(0, 0.6, n_schools),
        "digital_moral_safety": rng.normal(0, 0.5, n_schools),
    })

    panel = children.loc[children.index.repeat(n_periods)].copy()
    panel["time"] = np.tile(np.arange(n_periods), n_children)
    panel = panel.merge(schools, on="school_id", how="left")

    panel["current_guidance"] = rng.normal(panel["caregiving_guidance"], 0.70)
    panel["current_empathy"] = rng.normal(panel["empathic_sensitivity"], 0.70)
    panel["current_peer_fairness"] = rng.normal(panel["peer_fairness_base"], 0.70)
    panel["current_self_regulation"] = rng.normal(panel["self_regulation"], 0.50)
    panel["current_harm_recognition"] = rng.normal(panel["harm_recognition_base"], 0.60)

    panel["current_repair_opportunity"] = rng.normal(
        0.35 * panel["restorative_practice_access"]
        + 0.25 * panel["current_guidance"]
        + 0.20 * panel["school_moral_climate"]
        - 0.20 * panel["punitive_inconsistency"],
        0.65,
    )
    panel["current_exclusion"] = rng.normal(
        0.42 * panel["chronic_exclusion"]
        - 0.22 * panel["anti_bullying_climate"]
        + 0.18 * panel["punitive_inconsistency"],
        0.70,
    )
    panel["digital_cruelty_exposure"] = rng.normal(
        0.25 * panel["chronic_exclusion"]
        + 0.20 * panel["current_exclusion"]
        - 0.25 * panel["digital_moral_safety"],
        0.65,
    )
    panel["peer_pressure"] = rng.normal(
        0.25 * panel["current_exclusion"]
        - 0.18 * panel["current_peer_fairness"]
        - 0.15 * panel["anti_bullying_climate"],
        0.65,
    )

    panel["moral_support_context"] = (
        panel["current_guidance"]
        + panel["current_empathy"]
        + panel["current_peer_fairness"]
        + panel["current_self_regulation"]
        + panel["current_harm_recognition"]
        + panel["current_repair_opportunity"]
        + panel["school_moral_climate"]
        + panel["restorative_practice_access"]
        + panel["anti_bullying_climate"]
        + panel["digital_moral_safety"]
        - panel["punitive_inconsistency"]
    )

    panel = panel.sort_values(["child_id", "time"]).reset_index(drop=True)
    panel["conscience_score"] = np.nan
    panel["moral_action_score"] = np.nan

    for _, rows in panel.groupby("child_id", sort=False):
        previous_conscience = rows["baseline_morality"].iloc[0]
        for idx in rows.index:
            row = panel.loc[idx]
            conscience = (
                0.70 * previous_conscience
                + 0.80 * row.time
                + 1.05 * row.current_guidance
                + 1.00 * row.current_empathy
                + 0.95 * row.current_peer_fairness
                + 0.90 * row.current_self_regulation
                + 1.00 * row.current_harm_recognition
                + 0.95 * row.current_repair_opportunity
                + 0.80 * row.school_moral_climate
                + 0.90 * row.restorative_practice_access
                + 0.80 * row.anti_bullying_climate
                + 0.55 * row.digital_moral_safety
                - 1.00 * row.punitive_inconsistency
                - 1.20 * row.current_exclusion
                - 0.75 * row.digital_cruelty_exposure
                - 0.85 * row.chronic_exclusion
                + 0.25 * row.moral_support_context
                + rng.normal(0, 2.5)
            )
            action = (
                0.55 * conscience
                + 1.10 * row.current_self_regulation
                + 0.85 * row.current_peer_fairness
                + 0.80 * row.current_empathy
                + 0.75 * row.current_harm_recognition
                + 0.70 * row.current_repair_opportunity
                - 1.10 * row.peer_pressure
                - 0.95 * row.current_exclusion
                - 0.70 * row.digital_cruelty_exposure
                + rng.normal(0, 2.4)
            )
            panel.at[idx, "conscience_score"] = conscience
            panel.at[idx, "moral_action_score"] = action
            previous_conscience = conscience

    profiles = panel.groupby("child_id", as_index=False).agg(
        average_moral_support_context=("moral_support_context", "mean"),
        average_exclusion=("current_exclusion", "mean"),
        average_peer_pressure=("peer_pressure", "mean"),
        average_conscience=("conscience_score", "mean"),
        final_conscience=("conscience_score", "last"),
        average_moral_action=("moral_action_score", "mean"),
        chronic_exclusion=("chronic_exclusion", "first"),
    )
    support_median = profiles.average_moral_support_context.median()
    pressure_median = profiles.average_peer_pressure.median()
    profiles["moral_profile"] = np.select(
        [
            (profiles.chronic_exclusion == 1) & (profiles.average_moral_support_context >= support_median),
            (profiles.chronic_exclusion == 1) & (profiles.average_moral_support_context < support_median),
            (profiles.average_peer_pressure >= pressure_median) & (profiles.average_moral_support_context >= support_median),
            (profiles.average_peer_pressure >= pressure_median) & (profiles.average_moral_support_context < support_median),
        ],
        [
            "higher_exclusion_higher_moral_support",
            "higher_exclusion_lower_moral_support",
            "higher_peer_pressure_higher_moral_support",
            "higher_peer_pressure_lower_moral_support",
        ],
        default="lower_exclusion_or_peer_pressure",
    )
    panel = panel.merge(profiles[["child_id", "moral_profile"]], on="child_id", how="left")

    panel.to_csv(DATA / "moral_development_panel.csv", index=False)
    schools.to_csv(DATA / "school_moral_context_metadata.csv", index=False)
    profiles.to_csv(DATA / "moral_development_profiles.csv", index=False)

    panel.groupby(["time", "chronic_exclusion"], as_index=False).agg(
        average_conscience=("conscience_score", "mean"),
        average_moral_action=("moral_action_score", "mean"),
        average_moral_context=("moral_support_context", "mean"),
        average_exclusion=("current_exclusion", "mean"),
        average_peer_pressure=("peer_pressure", "mean"),
    ).to_csv(OUT / "generated_moral_development_trajectory.csv", index=False)

    print(f"Wrote {DATA / 'moral_development_panel.csv'} with {len(panel):,} rows")

if __name__ == "__main__":
    main()
