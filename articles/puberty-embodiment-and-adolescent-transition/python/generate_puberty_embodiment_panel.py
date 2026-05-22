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
    n, waves, schools_n = 920, 10, 36

    adolescents = pd.DataFrame({
        "adolescent_id": np.arange(1, n + 1),
        "school_id": rng.integers(1, schools_n + 1, n),
        "baseline_adjustment": rng.normal(50, 8, n),
        "timing_deviation": rng.normal(0, 1, n),
        "family_support_base": rng.normal(0, 1, n),
        "peer_comparison_base": rng.normal(0, 1, n),
        "body_image_vulnerability": rng.normal(0, 1, n),
        "chronic_stigma": rng.binomial(1, 0.22, n),
    })

    schools = pd.DataFrame({
        "school_id": np.arange(1, schools_n + 1),
        "school_support": rng.normal(0, 0.6, schools_n),
        "health_education_quality": rng.normal(0, 0.6, schools_n),
        "privacy_protection": rng.normal(0, 0.5, schools_n),
        "menstrual_support": rng.normal(0, 0.5, schools_n),
        "disability_accommodation": rng.normal(0, 0.6, schools_n),
        "anti_harassment_climate": rng.normal(0, 0.6, schools_n),
        "digital_safety": rng.normal(0, 0.5, schools_n),
    })

    panel = adolescents.loc[adolescents.index.repeat(waves)].copy()
    panel["time"] = np.tile(np.arange(waves), n)
    panel = panel.merge(schools, on="school_id", how="left")

    panel["pubertal_progress"] = panel["time"] + rng.normal(0, 0.4, len(panel))
    panel["current_family_support"] = rng.normal(panel["family_support_base"], 0.70)
    panel["current_peer_comparison"] = rng.normal(panel["peer_comparison_base"], 0.70)
    panel["current_body_concern"] = rng.normal(panel["body_image_vulnerability"] + 0.25 * np.abs(panel["timing_deviation"]), 0.60)
    panel["current_stigma"] = rng.normal(0.42 * panel["chronic_stigma"] + 0.20 * panel["current_peer_comparison"] - 0.20 * panel["anti_harassment_climate"], 0.70)
    panel["digital_visibility_stress"] = rng.normal(0.25 * panel["current_body_concern"] + 0.20 * panel["chronic_stigma"] - 0.25 * panel["digital_safety"], 0.65)

    panel["protective_context"] = (
        panel["current_family_support"] + panel["school_support"] +
        panel["health_education_quality"] + panel["privacy_protection"] +
        panel["menstrual_support"] + panel["disability_accommodation"] +
        panel["anti_harassment_climate"] + panel["digital_safety"]
    )

    panel = panel.sort_values(["adolescent_id", "time"]).reset_index(drop=True)
    panel["adjustment_score"] = np.nan

    for _, rows in panel.groupby("adolescent_id", sort=False):
        prev = rows["baseline_adjustment"].iloc[0]
        for idx in rows.index:
            row = panel.loc[idx]
            score = (
                0.70 * prev + 0.90 * row.pubertal_progress -
                0.95 * abs(row.timing_deviation) +
                1.05 * row.current_family_support -
                1.10 * row.current_peer_comparison -
                0.85 * row.current_body_concern -
                1.20 * row.current_stigma -
                0.75 * row.digital_visibility_stress -
                0.80 * row.chronic_stigma +
                0.80 * row.school_support +
                0.75 * row.health_education_quality +
                0.70 * row.privacy_protection +
                0.65 * row.menstrual_support +
                0.75 * row.disability_accommodation +
                0.80 * row.anti_harassment_climate +
                0.55 * row.digital_safety +
                0.25 * row.protective_context +
                rng.normal(0, 2.5)
            )
            panel.at[idx, "adjustment_score"] = score
            prev = score

    profiles = panel.groupby("adolescent_id", as_index=False).agg(
        average_protective_context=("protective_context", "mean"),
        average_stigma=("current_stigma", "mean"),
        average_body_concern=("current_body_concern", "mean"),
        average_digital_visibility_stress=("digital_visibility_stress", "mean"),
        average_adjustment=("adjustment_score", "mean"),
        final_adjustment=("adjustment_score", "last"),
        timing_deviation=("timing_deviation", "first"),
        chronic_stigma=("chronic_stigma", "first"),
    )

    protection_median = profiles.average_protective_context.median()
    timing_abs_median = profiles.timing_deviation.abs().median()

    profiles["puberty_profile"] = np.select(
        [
            (profiles.chronic_stigma == 1) & (profiles.average_protective_context >= protection_median),
            (profiles.chronic_stigma == 1) & (profiles.average_protective_context < protection_median),
            (profiles.timing_deviation.abs() >= timing_abs_median) & (profiles.average_protective_context >= protection_median),
            (profiles.timing_deviation.abs() >= timing_abs_median) & (profiles.average_protective_context < protection_median),
        ],
        [
            "higher_stigma_higher_support",
            "higher_stigma_lower_support",
            "higher_timing_difference_higher_support",
            "higher_timing_difference_lower_support",
        ],
        default="lower_stigma_or_timing_difference",
    )

    panel = panel.merge(profiles[["adolescent_id", "puberty_profile"]], on="adolescent_id", how="left")
    panel.to_csv(DATA / "puberty_embodiment_panel.csv", index=False)
    schools.to_csv(DATA / "school_puberty_context_metadata.csv", index=False)
    profiles.to_csv(DATA / "puberty_embodiment_profiles.csv", index=False)
    print(f"Wrote {DATA / 'puberty_embodiment_panel.csv'} with {len(panel):,} rows")

if __name__ == "__main__":
    main()
