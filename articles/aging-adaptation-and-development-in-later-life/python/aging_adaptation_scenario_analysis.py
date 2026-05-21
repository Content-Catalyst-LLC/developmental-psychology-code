#!/usr/bin/env python3
"""Scenario analysis for accessibility, support, adaptation, dignity, services, and health burden."""

from __future__ import annotations

from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "aging_adaptation_later_life_panel.csv"
OUTPUTS_DIR = ROOT / "outputs"
OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)


def main() -> None:
    if not DATA_PATH.exists():
        raise FileNotFoundError("Run python/generate_aging_adaptation_panel.py first.")

    panel = pd.read_csv(DATA_PATH)

    scenarios = []
    for name, function_boost, support_boost, adaptation_boost, meaning_boost, accessibility_boost, dignity_boost, service_boost, health_reduction in [
        ("baseline", 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0),
        ("social_support_boost", 0.0, 0.85, 0.20, 0.0, 0.0, 0.0, 0.0, 0.10),
        ("adaptive_strategy_boost", 0.0, 0.20, 0.85, 0.0, 0.0, 0.0, 0.0, 0.15),
        ("accessibility_boost", 0.0, 0.0, 0.20, 0.0, 0.85, 0.0, 0.20, 0.20),
        ("dignity_service_support", 0.0, 0.20, 0.20, 0.0, 0.0, 0.85, 0.85, 0.20),
        ("meaning_role_revision", 0.0, 0.20, 0.20, 0.85, 0.0, 0.20, 0.0, 0.05),
        ("health_burden_reduction", 0.0, 0.20, 0.20, 0.0, 0.20, 0.20, 0.20, 0.85),
        ("combined_healthy_aging_support", 0.45, 0.85, 0.85, 0.85, 0.85, 0.85, 0.85, 0.85),
    ]:
        simulated = panel.copy()
        simulated["scenario_function"] = simulated["current_function"] + function_boost
        simulated["scenario_support"] = simulated["current_support"] + support_boost
        simulated["scenario_adaptation"] = simulated["current_adaptation"] + adaptation_boost
        simulated["scenario_meaning"] = simulated["current_meaning"] + meaning_boost
        simulated["scenario_accessibility"] = simulated["environmental_accessibility"] + accessibility_boost
        simulated["scenario_dignity"] = simulated["dignity_support"] + dignity_boost
        simulated["scenario_service"] = simulated["service_access"] + service_boost
        simulated["scenario_health"] = simulated["current_health"] - health_reduction

        simulated["scenario_functional_fit"] = (
            simulated["scenario_function"]
            + simulated["scenario_accessibility"]
            + 0.35 * simulated["scenario_function"] * simulated["scenario_accessibility"]
        )

        simulated["scenario_adjustment"] = (
            simulated["adjustment_score"]
            + 1.15 * (simulated["scenario_functional_fit"] - simulated["functional_fit"])
            + 1.05 * support_boost
            + 0.95 * adaptation_boost
            + 0.80 * meaning_boost
            + 0.75 * dignity_boost
            + 0.60 * service_boost
            + 1.30 * health_reduction
        )

        summary = simulated.groupby("time", as_index=False).agg(
            average_adjustment=("scenario_adjustment", "mean"),
            average_functional_fit=("scenario_functional_fit", "mean"),
            average_health=("scenario_health", "mean"),
        )
        summary["scenario"] = name
        scenarios.append(summary)

    result = pd.concat(scenarios, ignore_index=True)
    result.to_csv(OUTPUTS_DIR / "python_aging_adaptation_scenario_comparison.csv", index=False)

    plt.figure(figsize=(9, 5.5))
    for scenario, group in result.groupby("scenario"):
        plt.plot(group["time"], group["average_adjustment"], marker="o", label=scenario)
    plt.xlabel("Time")
    plt.ylabel("Average scenario adjustment")
    plt.title("Synthetic Later-Life Adaptation Support Scenarios")
    plt.legend(fontsize=8)
    plt.tight_layout()
    plt.savefig(OUTPUTS_DIR / "python_aging_adaptation_scenario_comparison.png", dpi=160)
    plt.close()

    print("Wrote outputs/python_aging_adaptation_scenario_comparison.csv")
    print("Wrote outputs/python_aging_adaptation_scenario_comparison.png")


if __name__ == "__main__":
    main()
