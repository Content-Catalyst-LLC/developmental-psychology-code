#!/usr/bin/env python3
"""Scenario analysis for stage-like transitions, support, stress, and readiness."""

from __future__ import annotations

from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "stage_theory_development_panel.csv"
OUTPUTS_DIR = ROOT / "outputs"
OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)


def main() -> None:
    if not DATA_PATH.exists():
        raise FileNotFoundError("Run python/generate_stage_theory_panel.py first.")

    panel = pd.read_csv(DATA_PATH)

    scenarios = []
    for name, support_boost, school_boost, stability_boost, stress_reduction, transition_boost in [
        ("baseline", 0.0, 0.0, 0.0, 0.0, 0.0),
        ("family_support_boost", 0.85, 0.10, 0.10, 0.05, 0.20),
        ("school_support_boost", 0.20, 0.85, 0.20, 0.05, 0.25),
        ("resource_stability_boost", 0.10, 0.20, 0.85, 0.10, 0.25),
        ("stress_reduction", 0.15, 0.10, 0.20, 0.85, 0.30),
        ("transition_readiness_boost", 0.45, 0.45, 0.45, 0.45, 0.85),
        ("combined_context_support", 0.85, 0.85, 0.85, 0.85, 0.85),
    ]:
        simulated = panel.copy()
        simulated["scenario_support"] = simulated["current_support"] + support_boost
        simulated["scenario_school_support"] = simulated["school_support"] + school_boost
        simulated["scenario_stability"] = simulated["resource_stability"] + stability_boost
        simulated["scenario_stress"] = (simulated["chronic_stress"] - stress_reduction).clip(lower=0)

        simulated["scenario_readiness"] = (
            simulated["scenario_support"]
            + simulated["scenario_school_support"]
            + simulated["scenario_stability"]
            - 0.75 * simulated["scenario_stress"]
            + transition_boost
        )

        readiness_gain = simulated["scenario_readiness"] - simulated["transition_readiness"]

        simulated["scenario_score"] = (
            simulated["development_score"]
            + 1.15 * support_boost
            + 0.90 * school_boost
            + 0.70 * stability_boost
            + 2.00 * stress_reduction
            + 0.75 * simulated["threshold_on"] * simulated["stage_pattern"] * readiness_gain
        )

        summary = simulated.groupby(["time", "stage_profile"], as_index=False).agg(
            average_score=("scenario_score", "mean"),
            average_readiness=("scenario_readiness", "mean"),
            average_support=("scenario_support", "mean"),
            average_stress=("scenario_stress", "mean"),
            individuals=("child_id", "nunique"),
        )
        summary["scenario"] = name
        scenarios.append(summary)

    result = pd.concat(scenarios, ignore_index=True)
    result.to_csv(OUTPUTS_DIR / "python_stage_transition_scenario_comparison.csv", index=False)

    overall = result.groupby(["time", "scenario"], as_index=False).agg(
        average_score=("average_score", "mean")
    )

    plt.figure(figsize=(9, 5.5))
    for scenario, group in overall.groupby("scenario"):
        plt.plot(group["time"], group["average_score"], marker="o", label=scenario)
    plt.xlabel("Time")
    plt.ylabel("Average scenario development score")
    plt.title("Synthetic Stage-Like Development Context Support Scenarios")
    plt.legend(fontsize=8)
    plt.tight_layout()
    plt.savefig(OUTPUTS_DIR / "python_stage_transition_scenario_comparison.png", dpi=160)
    plt.close()

    print("Wrote outputs/python_stage_transition_scenario_comparison.csv")
    print("Wrote outputs/python_stage_transition_scenario_comparison.png")


if __name__ == "__main__":
    main()
