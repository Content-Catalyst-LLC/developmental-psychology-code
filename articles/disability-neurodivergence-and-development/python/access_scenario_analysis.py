#!/usr/bin/env python3
"""Scenario analysis for access, communication support, and barrier reduction."""

from __future__ import annotations

from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "disability_neurodivergence_panel.csv"
OUTPUTS_DIR = ROOT / "outputs"
OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)


def main() -> None:
    if not DATA_PATH.exists():
        raise FileNotFoundError("Run python/generate_disability_neurodivergence_panel.py first.")

    panel = pd.read_csv(DATA_PATH)

    scenarios = []
    for name, access_boost, barrier_reduction, communication_boost in [
        ("baseline", 0.0, 0.0, 0.0),
        ("universal_design", 0.80, 0.40, 0.0),
        ("communication_access", 0.30, 0.20, 0.90),
        ("barrier_reduction", 0.20, 0.90, 0.0),
        ("combined_access_plan", 0.80, 0.90, 0.90),
    ]:
        simulated = panel.copy()
        simulated["scenario_access"] = simulated["current_access"] + access_boost
        simulated["scenario_barrier"] = simulated["current_barrier"] - barrier_reduction
        simulated["scenario_communication"] = simulated["current_communication"] + communication_boost
        simulated["scenario_participation"] = (
            simulated["participation_score"]
            + 1.10 * access_boost
            + 1.25 * barrier_reduction
            + 0.95 * communication_boost
        )
        simulated["scenario_development"] = (
            simulated["development_score"]
            + 1.05 * access_boost
            + 1.15 * barrier_reduction
            + 0.90 * communication_boost
            + 0.45 * simulated["current_support"] * access_boost
        )

        summary = simulated.groupby("time", as_index=False).agg(
            average_development=("scenario_development", "mean"),
            average_participation=("scenario_participation", "mean"),
        )
        summary["scenario"] = name
        scenarios.append(summary)

    result = pd.concat(scenarios, ignore_index=True)
    result.to_csv(OUTPUTS_DIR / "python_access_scenario_comparison.csv", index=False)

    plt.figure(figsize=(9, 5.5))
    for scenario, group in result.groupby("scenario"):
        plt.plot(group["time"], group["average_development"], marker="o", label=scenario)
    plt.xlabel("Time")
    plt.ylabel("Average scenario development")
    plt.title("Synthetic Access and Barrier-Reduction Scenarios")
    plt.legend()
    plt.tight_layout()
    plt.savefig(OUTPUTS_DIR / "python_access_scenario_comparison.png", dpi=160)
    plt.close()

    print("Wrote outputs/python_access_scenario_comparison.csv")
    print("Wrote outputs/python_access_scenario_comparison.png")


if __name__ == "__main__":
    main()
