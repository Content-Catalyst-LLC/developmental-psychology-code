#!/usr/bin/env python3
"""Scenario analysis for school connectedness, curriculum opportunity, and stress reduction."""

from __future__ import annotations

from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "schooling_development_panel.csv"
OUTPUTS_DIR = ROOT / "outputs"
OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)


def main() -> None:
    if not DATA_PATH.exists():
        raise FileNotFoundError("Run python/generate_schooling_development_panel.py first.")

    panel = pd.read_csv(DATA_PATH)

    scenarios = []
    for name, teacher_boost, peer_boost, curriculum_boost, stress_reduction in [
        ("baseline", 0.0, 0.0, 0.0, 0.0),
        ("teacher_support_boost", 0.75, 0.0, 0.0, 0.20),
        ("peer_belonging_boost", 0.0, 0.75, 0.0, 0.20),
        ("curriculum_opportunity_boost", 0.0, 0.0, 0.80, 0.0),
        ("combined_connected_school", 0.75, 0.75, 0.80, 0.75),
    ]:
        simulated = panel.copy()
        simulated["scenario_teacher"] = simulated["current_teacher"] + teacher_boost
        simulated["scenario_peer"] = simulated["current_peer"] + peer_boost
        simulated["scenario_curriculum"] = simulated["curriculum_opportunity"] + curriculum_boost
        simulated["scenario_stress"] = simulated["current_stress"] - stress_reduction

        simulated["scenario_connectedness"] = (
            simulated["connectedness_score"]
            + 1.20 * teacher_boost
            + 1.05 * peer_boost
            + 1.10 * stress_reduction
        )

        simulated["scenario_development"] = (
            simulated["development_score"]
            + 1.10 * teacher_boost
            + 1.00 * peer_boost
            + 0.90 * curriculum_boost
            + 1.05 * stress_reduction
            + 0.45 * teacher_boost * peer_boost
        )

        summary = simulated.groupby("time", as_index=False).agg(
            average_development=("scenario_development", "mean"),
            average_connectedness=("scenario_connectedness", "mean"),
        )
        summary["scenario"] = name
        scenarios.append(summary)

    result = pd.concat(scenarios, ignore_index=True)
    result.to_csv(OUTPUTS_DIR / "python_schooling_scenario_comparison.csv", index=False)

    plt.figure(figsize=(9, 5.5))
    for scenario, group in result.groupby("scenario"):
        plt.plot(group["time"], group["average_development"], marker="o", label=scenario)
    plt.xlabel("Time")
    plt.ylabel("Average scenario development")
    plt.title("Synthetic School Connectedness and Opportunity Scenarios")
    plt.legend()
    plt.tight_layout()
    plt.savefig(OUTPUTS_DIR / "python_schooling_scenario_comparison.png", dpi=160)
    plt.close()

    print("Wrote outputs/python_schooling_scenario_comparison.csv")
    print("Wrote outputs/python_schooling_scenario_comparison.png")


if __name__ == "__main__":
    main()
