#!/usr/bin/env python3
"""Scenario analysis for nature-nurture supports, stress, and protective context."""

from __future__ import annotations

from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "nature_nurture_development_panel.csv"
OUTPUTS_DIR = ROOT / "outputs"
OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)


def main() -> None:
    if not DATA_PATH.exists():
        raise FileNotFoundError("Run python/generate_nature_nurture_panel.py first.")

    panel = pd.read_csv(DATA_PATH)

    scenarios = []
    for name, caregiver_boost, institution_boost, disability_boost, stability_boost, stress_reduction, intervention_boost, risk_reduction in [
        ("baseline", 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0),
        ("caregiver_support_boost", 0.85, 0.10, 0.10, 0.10, 0.05, 0.10, 0.05),
        ("institutional_support_boost", 0.15, 0.85, 0.15, 0.20, 0.10, 0.15, 0.05),
        ("disability_support_boost", 0.10, 0.20, 0.85, 0.15, 0.10, 0.15, 0.05),
        ("resource_stability_boost", 0.10, 0.20, 0.15, 0.85, 0.15, 0.10, 0.10),
        ("stress_reduction", 0.15, 0.15, 0.15, 0.20, 0.85, 0.20, 0.10),
        ("intervention_boost", 0.25, 0.25, 0.25, 0.25, 0.20, 0.85, 0.10),
        ("structural_risk_reduction", 0.20, 0.30, 0.20, 0.35, 0.35, 0.25, 0.85),
        ("combined_protective_context", 0.85, 0.85, 0.85, 0.85, 0.85, 0.85, 0.85),
    ]:
        simulated = panel.copy()
        simulated["scenario_caregiver_support"] = simulated["caregiver_support"] + caregiver_boost
        simulated["scenario_institutional_support"] = simulated["institutional_support"] + institution_boost
        simulated["scenario_disability_support"] = simulated["disability_support"] + disability_boost
        simulated["scenario_resource_stability"] = simulated["resource_stability"] + stability_boost
        simulated["scenario_acute_stress"] = simulated["acute_stress"] - stress_reduction
        simulated["scenario_intervention"] = (simulated["intervention"] + intervention_boost).clip(upper=1)
        simulated["scenario_structural_risk"] = (simulated["structural_risk"] - risk_reduction).clip(lower=0)

        simulated["scenario_protective_context"] = (
            simulated["scenario_caregiver_support"]
            + simulated["scenario_institutional_support"]
            + simulated["scenario_disability_support"]
            + simulated["scenario_resource_stability"]
            + simulated["scenario_intervention"]
        )

        protective_gain = simulated["scenario_protective_context"] - simulated["protective_context"]
        stress_gain = simulated["acute_stress"] - simulated["scenario_acute_stress"]
        risk_gain = simulated["structural_risk"] - simulated["scenario_structural_risk"]

        bio = simulated["biological_sensitivity"]

        simulated["scenario_development"] = (
            simulated["development_score"]
            + 1.20 * caregiver_boost
            + 0.95 * institution_boost
            + 0.85 * disability_boost
            + 0.70 * stability_boost
            + 1.40 * stress_gain
            + 1.60 * intervention_boost
            + 2.20 * risk_gain
            + 1.00 * bio * caregiver_boost
            + 0.90 * bio * stress_gain
            + 0.65 * bio * protective_gain
        )

        summary = simulated.groupby(["time", "sensitivity_profile"], as_index=False).agg(
            average_development=("scenario_development", "mean"),
            average_protective_context=("scenario_protective_context", "mean"),
            average_stress=("scenario_acute_stress", "mean"),
            average_structural_risk=("scenario_structural_risk", "mean"),
            children=("child_id", "nunique"),
        )
        summary["scenario"] = name
        scenarios.append(summary)

    result = pd.concat(scenarios, ignore_index=True)
    result.to_csv(OUTPUTS_DIR / "python_nature_nurture_scenario_comparison.csv", index=False)

    overall = result.groupby(["time", "scenario"], as_index=False).agg(
        average_development=("average_development", "mean")
    )

    plt.figure(figsize=(9, 5.5))
    for scenario, group in overall.groupby("scenario"):
        plt.plot(group["time"], group["average_development"], marker="o", label=scenario)
    plt.xlabel("Time")
    plt.ylabel("Average scenario development score")
    plt.title("Synthetic Nature-Nurture Protective Context Scenarios")
    plt.legend(fontsize=8)
    plt.tight_layout()
    plt.savefig(OUTPUTS_DIR / "python_nature_nurture_scenario_comparison.png", dpi=160)
    plt.close()

    print("Wrote outputs/python_nature_nurture_scenario_comparison.csv")
    print("Wrote outputs/python_nature_nurture_scenario_comparison.png")


if __name__ == "__main__":
    main()
