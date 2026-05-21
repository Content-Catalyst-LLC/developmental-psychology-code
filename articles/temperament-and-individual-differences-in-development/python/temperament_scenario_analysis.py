#!/usr/bin/env python3
"""Scenario analysis for temperament support, stress reduction, and goodness of fit."""

from __future__ import annotations

from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "temperament_individual_differences_panel.csv"
OUTPUTS_DIR = ROOT / "outputs"
OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)


def main() -> None:
    if not DATA_PATH.exists():
        raise FileNotFoundError("Run python/generate_temperament_panel.py first.")

    panel = pd.read_csv(DATA_PATH)

    scenarios = []
    for name, support_boost, fit_boost, accommodation_boost, teacher_boost, movement_boost, stress_reduction, chronic_reduction in [
        ("baseline", 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0),
        ("caregiver_support_boost", 0.85, 0.0, 0.20, 0.0, 0.0, 0.10, 0.0),
        ("classroom_fit_boost", 0.10, 0.85, 0.35, 0.25, 0.25, 0.10, 0.0),
        ("teacher_responsiveness_boost", 0.10, 0.20, 0.30, 0.85, 0.10, 0.10, 0.0),
        ("movement_flexibility_boost", 0.0, 0.20, 0.30, 0.10, 0.85, 0.05, 0.0),
        ("stress_reduction", 0.20, 0.10, 0.10, 0.10, 0.0, 0.85, 0.20),
        ("accommodation_support", 0.20, 0.25, 0.85, 0.25, 0.25, 0.15, 0.0),
        ("combined_goodness_of_fit_support", 0.85, 0.85, 0.85, 0.85, 0.85, 0.85, 0.35),
    ]:
        simulated = panel.copy()
        simulated["scenario_support"] = simulated["current_support"] + support_boost
        simulated["scenario_school_fit"] = simulated["current_school_fit"] + fit_boost
        simulated["scenario_accommodation"] = simulated["current_accommodation"] + accommodation_boost
        simulated["scenario_teacher"] = simulated["teacher_responsiveness"] + teacher_boost
        simulated["scenario_movement"] = simulated["movement_flexibility"] + movement_boost
        simulated["scenario_stress"] = simulated["acute_stress"] - stress_reduction
        simulated["scenario_chronic"] = (simulated["chronic_stress"] - chronic_reduction).clip(lower=0)

        simulated["scenario_goodness_of_fit"] = (
            simulated["scenario_school_fit"]
            + simulated["scenario_teacher"]
            + simulated["scenario_movement"]
            - (simulated["temperament_reactivity"] - simulated["classroom_structure"]).abs()
            + simulated["scenario_accommodation"]
        )

        fit_gain = simulated["scenario_goodness_of_fit"] - simulated["goodness_of_fit"]

        simulated["scenario_adjustment"] = (
            simulated["adjustment_score"]
            + 1.30 * support_boost
            + 1.20 * fit_gain
            + 0.50 * teacher_boost
            + 1.50 * stress_reduction
            + 1.10 * chronic_reduction
            + 0.95 * simulated["temperament_reactivity"] * support_boost
            + 0.85 * simulated["temperament_reactivity"] * fit_gain
            + 0.90 * simulated["temperament_reactivity"] * stress_reduction
        )

        summary = simulated.groupby("time", as_index=False).agg(
            average_adjustment=("scenario_adjustment", "mean"),
            average_fit=("scenario_goodness_of_fit", "mean"),
            average_stress=("scenario_stress", "mean"),
            average_support=("scenario_support", "mean"),
        )
        summary["scenario"] = name
        scenarios.append(summary)

    result = pd.concat(scenarios, ignore_index=True)
    result.to_csv(OUTPUTS_DIR / "python_temperament_scenario_comparison.csv", index=False)

    plt.figure(figsize=(9, 5.5))
    for scenario, group in result.groupby("scenario"):
        plt.plot(group["time"], group["average_adjustment"], marker="o", label=scenario)
    plt.xlabel("Time")
    plt.ylabel("Average scenario adjustment")
    plt.title("Synthetic Temperament Goodness-of-Fit Support Scenarios")
    plt.legend(fontsize=8)
    plt.tight_layout()
    plt.savefig(OUTPUTS_DIR / "python_temperament_scenario_comparison.png", dpi=160)
    plt.close()

    print("Wrote outputs/python_temperament_scenario_comparison.csv")
    print("Wrote outputs/python_temperament_scenario_comparison.png")


if __name__ == "__main__":
    main()
