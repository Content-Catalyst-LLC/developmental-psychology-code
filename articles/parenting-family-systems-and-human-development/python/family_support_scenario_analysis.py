#!/usr/bin/env python3
"""Scenario analysis for caregiver support, kin support, stability, and stress reduction."""

from __future__ import annotations

from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "family_systems_panel.csv"
OUTPUTS_DIR = ROOT / "outputs"
OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)


def main() -> None:
    if not DATA_PATH.exists():
        raise FileNotFoundError("Run python/generate_family_systems_panel.py first.")

    panel = pd.read_csv(DATA_PATH)

    scenarios = []
    for name, parenting_boost, kin_boost, stability_boost, stress_reduction in [
        ("baseline", 0.0, 0.0, 0.0, 0.0),
        ("parenting_support", 0.75, 0.0, 0.0, 0.25),
        ("kin_support_boost", 0.0, 0.75, 0.0, 0.10),
        ("household_stability_boost", 0.0, 0.0, 0.75, 0.25),
        ("combined_family_support", 0.75, 0.75, 0.75, 0.75),
    ]:
        simulated = panel.copy()
        simulated["scenario_parenting"] = simulated["current_parenting"] + parenting_boost
        simulated["scenario_kin"] = simulated["kin_support"] + kin_boost
        simulated["scenario_stability"] = simulated["household_stability"] + stability_boost
        simulated["scenario_stress"] = simulated["current_stress"] - stress_reduction

        simulated["scenario_family_support"] = (
            simulated["family_support_index"]
            + parenting_boost
            + kin_boost
            + stability_boost
            + stress_reduction
        )

        simulated["scenario_development"] = (
            simulated["development_score"]
            + 1.15 * parenting_boost
            + 0.80 * kin_boost
            + 0.90 * stability_boost
            + 1.10 * stress_reduction
            + 0.35 * parenting_boost * simulated["current_family"]
        )

        summary = simulated.groupby("time", as_index=False).agg(
            average_development=("scenario_development", "mean"),
            average_family_support=("scenario_family_support", "mean"),
        )
        summary["scenario"] = name
        scenarios.append(summary)

    result = pd.concat(scenarios, ignore_index=True)
    result.to_csv(OUTPUTS_DIR / "python_family_support_scenario_comparison.csv", index=False)

    plt.figure(figsize=(9, 5.5))
    for scenario, group in result.groupby("scenario"):
        plt.plot(group["time"], group["average_development"], marker="o", label=scenario)
    plt.xlabel("Time")
    plt.ylabel("Average scenario development")
    plt.title("Synthetic Family Support and Stress-Reduction Scenarios")
    plt.legend()
    plt.tight_layout()
    plt.savefig(OUTPUTS_DIR / "python_family_support_scenario_comparison.png", dpi=160)
    plt.close()

    print("Wrote outputs/python_family_support_scenario_comparison.csv")
    print("Wrote outputs/python_family_support_scenario_comparison.png")


if __name__ == "__main__":
    main()
