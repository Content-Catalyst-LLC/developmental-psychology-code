#!/usr/bin/env python3
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
    n, waves, schools_n = 900, 10, 36

    adolescents = pd.DataFrame({
        "adolescent_id": np.arange(1, n + 1),
        "school_id": rng.integers(1, schools_n + 1, n),
        "baseline_identity": rng.normal(50, 8, n),
        "peer_support_base": rng.normal(0, 1, n),
        "family_support_base": rng.normal(0, 1, n),
        "school_connectedness_base": rng.normal(0, 1, n),
        "future_orientation_base": rng.normal(0, 1, n),
        "chronic_exclusion": rng.binomial(1, 0.24, n),
    })

    schools = pd.DataFrame({
        "school_id": np.arange(1, schools_n + 1),
        "school_climate": rng.normal(0, 0.6, schools_n),
        "counseling_access": rng.normal(0, 0.5, schools_n),
        "extracurricular_access": rng.normal(0, 0.5, schools_n),
        "identity_safety": rng.normal(0, 0.6, schools_n),
        "digital_safety": rng.normal(0, 0.5, schools_n),
    })

    panel = adolescents.loc[adolescents.index.repeat(waves)].copy()
    panel["time"] = np.tile(np.arange(waves), n)
    panel = panel.merge(schools, on="school_id", how="left")

    panel["current_peer_support"] = rng.normal(panel["peer_support_base"], 0.70)
    panel["current_family_support"] = rng.normal(panel["family_support_base"], 0.70)
    panel["current_connectedness"] = rng.normal(panel["school_connectedness_base"], 0.70)
    panel["current_future_orientation"] = rng.normal(panel["future_orientation_base"], 0.70)
    panel["current_exclusion"] = rng.normal(0.45 * panel["chronic_exclusion"] - 0.20 * panel["identity_safety"], 0.70)
    panel["digital_stress"] = rng.normal(0.30 * panel["chronic_exclusion"] - 0.25 * panel["digital_safety"], 0.65)

    panel["support_context"] = (
        panel["current_peer_support"] + panel["current_family_support"] +
        panel["current_connectedness"] + panel["current_future_orientation"] +
        panel["school_climate"] + panel["counseling_access"] +
        panel["extracurricular_access"] + panel["identity_safety"] +
        panel["digital_safety"]
    )

    panel = panel.sort_values(["adolescent_id", "time"]).reset_index(drop=True)
    panel["identity_score"] = np.nan

    for _, rows in panel.groupby("adolescent_id", sort=False):
        prev = rows["baseline_identity"].iloc[0]
        for idx in rows.index:
            row = panel.loc[idx]
            score = (
                0.70 * prev + 0.85 * row.time +
                1.10 * row.current_peer_support +
                1.00 * row.current_family_support +
                0.95 * row.current_connectedness +
                0.90 * row.current_future_orientation +
                0.80 * row.school_climate +
                0.70 * row.counseling_access +
                0.65 * row.extracurricular_access +
                0.85 * row.identity_safety +
                0.55 * row.digital_safety -
                1.25 * row.current_exclusion -
                0.75 * row.digital_stress -
                0.90 * row.chronic_exclusion +
                rng.normal(0, 2.5)
            )
            panel.at[idx, "identity_score"] = score
            prev = score

    profiles = panel.groupby("adolescent_id", as_index=False).agg(
        average_support_context=("support_context", "mean"),
        average_exclusion=("current_exclusion", "mean"),
        average_digital_stress=("digital_stress", "mean"),
        average_identity=("identity_score", "mean"),
        final_identity=("identity_score", "last"),
        chronic_exclusion=("chronic_exclusion", "first"),
    )

    support_median = profiles.average_support_context.median()
    profiles["identity_profile"] = np.select(
        [
            (profiles.chronic_exclusion == 1) & (profiles.average_support_context >= support_median),
            (profiles.chronic_exclusion == 1) & (profiles.average_support_context < support_median),
            (profiles.chronic_exclusion == 0) & (profiles.average_support_context >= support_median),
        ],
        ["higher_exclusion_higher_support", "higher_exclusion_lower_support", "lower_exclusion_higher_support"],
        default="lower_exclusion_lower_support",
    )

    panel = panel.merge(profiles[["adolescent_id", "identity_profile"]], on="adolescent_id")
    panel.to_csv(DATA / "adolescence_identity_panel.csv", index=False)
    schools.to_csv(DATA / "school_context_metadata.csv", index=False)
    profiles.to_csv(DATA / "adolescent_identity_profiles.csv", index=False)
    print(f"Wrote {DATA / 'adolescence_identity_panel.csv'} with {len(panel):,} rows")

if __name__ == "__main__":
    main()
