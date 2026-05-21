#!/usr/bin/env python3
"""Scenario analysis for adult development supports and burdens."""

from __future__ import annotations

from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "adult_development_life_stages_panel.csv"
OUTPUTS_DIR = ROOT / "outputs"
OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)


def main() -> None:
    if not DATA_PATH.exists():
        raise FileNotFoundError("Run python/generate_adult_development_panel.py first.")

    panel = pd.read_csv(DATA_PATH)

    scenarios = []
    for name, support_boost, work_boost, resource_boost, institutional_boost, community_boost, health_reduction, role_burden_reduction in [
        ("baseline", 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0),
        ("relational_support_boost", 0.85, 0.0, 0.25, 0.0, 0.20, 0.05, 0.10),
        ("work_integration_support", 0.0, 0.85, 0.20, 0.20, 0.0, 0.05, 0.10),
        ("adaptive_resource_boost", 0.25, 0.0, 0.85, 0.0, 0.0, 0.10, 0.25),
        ("institutional_community_support", 0.10, 0.20, 0.25, 0.85, 0.85, 0.10, 0.20),
        ("health_burden_reduction", 0.10, 0.0, 0.25, 0.20, 0.0, 0.85, 0.20),
        ("role_burden_reduction", 0.20, 0.0, 0.35, 0.30, 0.20, 0.10, 0.85),
        ("combined_adult_development_support", 0.85, 0.85, 0.85, 0.85, 0.85, 0.85, 0.85),
    ]:
        simulated = panel.copy()
        simulated["scenario_support"] = simulated["current_relational_support"] + support_boost
        simulated["scenario_work"] = simulated["current_work_integration"] + work_boost
        simulated["scenario_resources"] = simulated["current_adaptive_resources"] + resource_boost
        simulated["scenario_institutional"] = simulated["institutional_support"] + institutional_boost
        simulated["scenario_community"] = simulated["community_stability"] + community_boost
        simulated["scenario_health"] = simulated["current_health_burden"] - health_reduction
        simulated["scenario_role_burden"] = simulated["current_role_burden"] - role_burden_reduction

        simulated["scenario_adjustment"] = (
            simulated["adjustment_score"]
            + 1.15 * support_boost
            + 1.05 * work_boost
            + 0.95 * resource_boost
            + 0.70 * institutional_boost
            + 0.55 * community_boost
            + 1.20 * health_reduction
            + 0.80 * role_burden_reduction
            + 0.25 * (simulated["scenario_support"] * simulated["scenario_resources"]
                      - simulated["current_relational_support"] * simulated["current_adaptive_resources"])
        )

        summary = simulated.groupby(["time", "life_stage"], as_index=False).agg(
            average_adjustment=("scenario_adjustment", "mean"),
            average_health=("scenario_health", "mean"),
            average_role_burden=("scenario_role_burden", "mean"),
        )
        summary["scenario"] = name
        scenarios.append(summary)

    result = pd.concat(scenarios, ignore_index=True)
    result.to_csv(OUTPUTS_DIR / "python_adult_development_scenario_comparison.csv", index=False)

    overall = result.groupby(["time", "scenario"], as_index=False).agg(
        average_adjustment=("average_adjustment", "mean")
    )

    plt.figure(figsize=(9, 5.5))
    for scenario, group in overall.groupby("scenario"):
        plt.plot(group["time"], group["average_adjustment"], marker="o", label=scenario)
    plt.xlabel("Time")
    plt.ylabel("Average scenario adjustment")
    plt.title("Synthetic Adult Development Support Scenarios")
    plt.legend(fontsize=8)
    plt.tight_layout()
    plt.savefig(OUTPUTS_DIR / "python_adult_development_scenario_comparison.png", dpi=160)
    plt.close()

    print("Wrote outputs/python_adult_development_scenario_comparison.csv")
    print("Wrote outputs/python_adult_development_scenario_comparison.png")


if __name__ == "__main__":
    main()
