#!/usr/bin/env python3
"""Scenario analysis for care, nutrition, school support, and stress reduction."""

from __future__ import annotations

from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "genes_environment_plasticity_panel.csv"
OUTPUTS_DIR = ROOT / "outputs"
OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)


def main() -> None:
    if not DATA_PATH.exists():
        raise FileNotFoundError("Run python/generate_genes_environment_panel.py first.")

    panel = pd.read_csv(DATA_PATH)

    scenarios = []
    for name, care_boost, nutrition_boost, school_boost, stress_reduction in [
        ("baseline", 0.0, 0.0, 0.0, 0.0),
        ("caregiving_support", 0.80, 0.0, 0.0, 0.20),
        ("nutrition_support", 0.0, 0.80, 0.0, 0.10),
        ("school_support", 0.0, 0.0, 0.80, 0.10),
        ("stress_reduction", 0.0, 0.0, 0.0, 0.85),
        ("combined_support_ecology", 0.80, 0.80, 0.80, 0.85),
    ]:
        simulated = panel.copy()
        simulated["scenario_care"] = simulated["current_care"] + care_boost
        simulated["scenario_nutrition"] = simulated["current_nutrition"] + nutrition_boost
        simulated["scenario_school"] = simulated["school_support"] + school_boost
        simulated["scenario_stress"] = simulated["current_stress"] - stress_reduction

        simulated["scenario_embedded_support"] = (
            simulated["embedded_support"]
            + (care_boost + nutrition_boost + school_boost) * simulated["timing_weight"]
        )

        simulated["scenario_embedded_stress"] = (
            simulated["embedded_stress"]
            - stress_reduction * simulated["timing_weight"]
        )

        simulated["scenario_development"] = (
            simulated["development_score"]
            + 1.10 * care_boost
            + 0.80 * nutrition_boost
            + 0.75 * school_boost
            + 1.05 * stress_reduction
            + 0.50 * simulated["bio_sensitivity"] * care_boost
            + 0.40 * simulated["bio_sensitivity"] * stress_reduction
            + 0.30 * (care_boost + nutrition_boost + school_boost) * simulated["timing_weight"]
        )

        summary = simulated.groupby("time", as_index=False).agg(
            average_development=("scenario_development", "mean"),
            average_embedded_support=("scenario_embedded_support", "mean"),
            average_embedded_stress=("scenario_embedded_stress", "mean"),
        )
        summary["scenario"] = name
        scenarios.append(summary)

    result = pd.concat(scenarios, ignore_index=True)
    result.to_csv(OUTPUTS_DIR / "python_plasticity_scenario_comparison.csv", index=False)

    plt.figure(figsize=(9, 5.5))
    for scenario, group in result.groupby("scenario"):
        plt.plot(group["time"], group["average_development"], marker="o", label=scenario)
    plt.xlabel("Time")
    plt.ylabel("Average scenario development")
    plt.title("Synthetic Plasticity Support and Stress-Reduction Scenarios")
    plt.legend()
    plt.tight_layout()
    plt.savefig(OUTPUTS_DIR / "python_plasticity_scenario_comparison.png", dpi=160)
    plt.close()

    print("Wrote outputs/python_plasticity_scenario_comparison.csv")
    print("Wrote outputs/python_plasticity_scenario_comparison.png")


if __name__ == "__main__":
    main()
