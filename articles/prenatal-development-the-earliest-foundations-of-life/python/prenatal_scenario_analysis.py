#!/usr/bin/env python3
"""Scenario analysis for prenatal care, support, exposure reduction, and public health."""

from __future__ import annotations

from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "prenatal_development_foundations_panel.csv"
OUTPUTS_DIR = ROOT / "outputs"
OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)


def main() -> None:
    if not DATA_PATH.exists():
        raise FileNotFoundError("Run python/generate_prenatal_development_panel.py first.")

    prenatal = pd.read_csv(DATA_PATH)

    scenarios = []
    for name, care_boost, healthcare_boost, nutrition_boost, social_boost, stress_reduction, exposure_reduction, environmental_reduction, economic_boost in [
        ("baseline", 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0),
        ("prenatal_care_boost", 0.85, 0.20, 0.10, 0.10, 0.10, 0.05, 0.05, 0.10),
        ("healthcare_access_boost", 0.20, 0.85, 0.10, 0.10, 0.10, 0.05, 0.10, 0.20),
        ("nutrition_support_boost", 0.10, 0.10, 0.85, 0.15, 0.05, 0.05, 0.05, 0.10),
        ("social_support_boost", 0.10, 0.10, 0.20, 0.85, 0.25, 0.05, 0.05, 0.15),
        ("stress_reduction", 0.10, 0.10, 0.20, 0.25, 0.85, 0.05, 0.05, 0.20),
        ("environmental_protection", 0.10, 0.20, 0.10, 0.10, 0.10, 0.85, 0.85, 0.20),
        ("combined_prenatal_public_health_support", 0.85, 0.85, 0.85, 0.85, 0.85, 0.85, 0.85, 0.85),
    ]:
        simulated = prenatal.copy()
        simulated["scenario_prenatal_care"] = simulated["prenatal_care"] + care_boost
        simulated["scenario_healthcare_access"] = simulated["healthcare_access"] + healthcare_boost
        simulated["scenario_nutrition"] = simulated["nutrition_support"] + nutrition_boost
        simulated["scenario_social_support"] = simulated["social_support"] + social_boost
        simulated["scenario_chronic_stress"] = simulated["chronic_stress"] - stress_reduction
        simulated["scenario_toxic_exposure"] = simulated["toxic_exposure"] - exposure_reduction
        simulated["scenario_environmental_burden"] = simulated["environmental_burden"] - environmental_reduction
        simulated["scenario_economic_security"] = simulated["economic_security"] + economic_boost

        simulated["scenario_effective_care"] = (
            simulated["scenario_prenatal_care"]
            + simulated["scenario_healthcare_access"]
            + 0.30 * simulated["scenario_social_support"]
        )

        simulated["scenario_developmental_risk"] = (
            simulated["scenario_chronic_stress"]
            + simulated["scenario_toxic_exposure"]
            + simulated["scenario_environmental_burden"]
            - 0.40 * simulated["scenario_economic_security"]
        )

        simulated["scenario_outcome"] = (
            simulated["early_outcome"]
            + 1.35 * (simulated["scenario_effective_care"] - simulated["effective_care"])
            + 1.10 * nutrition_boost
            + 0.85 * social_boost
            + 1.55 * stress_reduction
            + 1.45 * exposure_reduction
            + 1.10 * environmental_reduction
            + 0.70 * simulated["maternal_health"] * (simulated["scenario_effective_care"] - simulated["effective_care"])
            + 0.60 * simulated["maternal_health"] * stress_reduction
            - 0.55 * (
                simulated["scenario_developmental_risk"] * simulated["scenario_effective_care"]
                - simulated["developmental_risk"] * simulated["effective_care"]
            )
        )

        summary = simulated.groupby("prenatal_profile", as_index=False).agg(
            average_outcome=("scenario_outcome", "mean"),
            average_effective_care=("scenario_effective_care", "mean"),
            average_developmental_risk=("scenario_developmental_risk", "mean"),
            cases=("case_id", "count"),
        )
        summary["scenario"] = name
        scenarios.append(summary)

    result = pd.concat(scenarios, ignore_index=True)
    result.to_csv(OUTPUTS_DIR / "python_prenatal_scenario_comparison.csv", index=False)

    overall = result.groupby("scenario", as_index=False).agg(
        average_outcome=("average_outcome", "mean"),
        average_effective_care=("average_effective_care", "mean"),
        average_developmental_risk=("average_developmental_risk", "mean"),
    ).sort_values("average_outcome")

    plt.figure(figsize=(10, 5.5))
    plt.barh(overall["scenario"], overall["average_outcome"])
    plt.xlabel("Average scenario early developmental outcome")
    plt.ylabel("Scenario")
    plt.title("Synthetic Prenatal Public-Health Support Scenarios")
    plt.tight_layout()
    plt.savefig(OUTPUTS_DIR / "python_prenatal_scenario_comparison.png", dpi=160)
    plt.close()

    print("Wrote outputs/python_prenatal_scenario_comparison.csv")
    print("Wrote outputs/python_prenatal_scenario_comparison.png")


if __name__ == "__main__":
    main()
