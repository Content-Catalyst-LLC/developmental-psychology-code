#!/usr/bin/env python3
"""Scenario analysis for support, stress, rupture, intervention, and developmental turning points."""

from __future__ import annotations

from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "continuity_discontinuity_panel.csv"
OUTPUTS_DIR = ROOT / "outputs"
OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)


def main() -> None:
    if not DATA_PATH.exists():
        raise FileNotFoundError("Run python/generate_continuity_discontinuity_panel.py first.")

    panel = pd.read_csv(DATA_PATH)

    scenarios = []
    for name, support_boost, school_boost, stability_boost, stress_reduction, rupture_reduction, intervention_boost, readiness_boost in [
        ("baseline", 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0),
        ("family_support_boost", 0.85, 0.10, 0.10, 0.05, 0.05, 0.10, 0.20),
        ("school_support_boost", 0.20, 0.85, 0.20, 0.05, 0.05, 0.10, 0.25),
        ("resource_stability_boost", 0.10, 0.20, 0.85, 0.10, 0.10, 0.10, 0.25),
        ("stress_reduction", 0.15, 0.10, 0.20, 0.85, 0.10, 0.15, 0.30),
        ("rupture_reduction", 0.20, 0.20, 0.35, 0.20, 0.85, 0.25, 0.35),
        ("intervention_boost", 0.25, 0.20, 0.25, 0.20, 0.20, 0.85, 0.45),
        ("combined_protective_turning_point", 0.85, 0.85, 0.85, 0.85, 0.85, 0.85, 0.85),
    ]:
        simulated = panel.copy()
        simulated["scenario_support"] = simulated["current_support"] + support_boost
        simulated["scenario_school_support"] = simulated["school_support"] + school_boost
        simulated["scenario_stability"] = simulated["resource_stability"] + stability_boost
        simulated["scenario_stress"] = (simulated["chronic_stress"] - stress_reduction).clip(lower=0)
        simulated["scenario_rupture"] = (simulated["institutional_rupture"] - rupture_reduction).clip(lower=0)
        simulated["scenario_intervention"] = (simulated["intervention_exposure"] + intervention_boost).clip(upper=1)

        simulated["scenario_readiness"] = (
            simulated["scenario_support"]
            + simulated["scenario_school_support"]
            + simulated["scenario_stability"]
            + 0.85 * simulated["scenario_intervention"]
            - 0.75 * simulated["scenario_stress"]
            - 0.80 * simulated["scenario_rupture"]
            + readiness_boost
        )

        readiness_gain = simulated["scenario_readiness"] - simulated["transition_readiness"]

        simulated["scenario_score"] = (
            simulated["development_score"]
            + 1.25 * support_boost
            + 0.90 * school_boost
            + 0.70 * stability_boost
            + 2.00 * stress_reduction
            + 2.40 * rupture_reduction
            + 1.30 * intervention_boost
            + 0.75 * simulated["threshold_on"] * simulated["threshold_sensitive"] * readiness_gain
        )

        summary = simulated.groupby(["time", "change_profile"], as_index=False).agg(
            average_score=("scenario_score", "mean"),
            average_readiness=("scenario_readiness", "mean"),
            average_support=("scenario_support", "mean"),
            average_stress=("scenario_stress", "mean"),
            average_rupture=("scenario_rupture", "mean"),
            average_intervention=("scenario_intervention", "mean"),
            individuals=("person_id", "nunique"),
        )
        summary["scenario"] = name
        scenarios.append(summary)

    result = pd.concat(scenarios, ignore_index=True)
    result.to_csv(OUTPUTS_DIR / "python_turning_point_scenario_comparison.csv", index=False)

    overall = result.groupby(["time", "scenario"], as_index=False).agg(
        average_score=("average_score", "mean")
    )

    plt.figure(figsize=(9, 5.5))
    for scenario, group in overall.groupby("scenario"):
        plt.plot(group["time"], group["average_score"], marker="o", label=scenario)
    plt.xlabel("Time")
    plt.ylabel("Average scenario development score")
    plt.title("Synthetic Developmental Turning Point Scenarios")
    plt.legend(fontsize=8)
    plt.tight_layout()
    plt.savefig(OUTPUTS_DIR / "python_turning_point_scenario_comparison.png", dpi=160)
    plt.close()

    print("Wrote outputs/python_turning_point_scenario_comparison.csv")
    print("Wrote outputs/python_turning_point_scenario_comparison.png")


if __name__ == "__main__":
    main()
