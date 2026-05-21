#!/usr/bin/env python3
"""Scenario analysis for protective support and service access.

This script compares synthetic intervention-style scenarios. It is not causal
evidence; it shows how scenario logic can be represented transparently.
"""

from __future__ import annotations

from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "developmental_psychopathology_panel.csv"
OUTPUTS_DIR = ROOT / "outputs"
OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)


def main() -> None:
    if not DATA_PATH.exists():
        raise FileNotFoundError("Run python/generate_developmental_psychopathology.py first.")

    panel = pd.read_csv(DATA_PATH)

    scenarios = []
    for name, support_boost, risk_reduction in [
        ("baseline", 0.0, 0.0),
        ("support_boost", 0.75, 0.0),
        ("risk_reduction", 0.0, 0.75),
        ("combined_support_and_risk", 0.75, 0.75),
    ]:
        simulated = panel.copy()
        simulated["scenario_support"] = simulated["current_support"] + support_boost
        simulated["scenario_risk"] = simulated["current_risk"] - risk_reduction
        simulated["scenario_adaptation"] = (
            simulated["adaptation_score"]
            + 1.10 * support_boost
            + 1.10 * risk_reduction * simulated["timing_weight"]
            + 0.35 * support_boost * simulated["current_stability"]
        )
        summary = simulated.groupby("time", as_index=False).agg(
            average_adaptation=("scenario_adaptation", "mean")
        )
        summary["scenario"] = name
        scenarios.append(summary)

    result = pd.concat(scenarios, ignore_index=True)
    result.to_csv(OUTPUTS_DIR / "python_scenario_comparison.csv", index=False)

    plt.figure(figsize=(9, 5.5))
    for scenario, group in result.groupby("scenario"):
        plt.plot(group["time"], group["average_adaptation"], marker="o", label=scenario)
    plt.xlabel("Time")
    plt.ylabel("Average scenario adaptation")
    plt.title("Synthetic Support and Risk-Reduction Scenarios")
    plt.legend()
    plt.tight_layout()
    plt.savefig(OUTPUTS_DIR / "python_scenario_comparison.png", dpi=160)
    plt.close()

    print("Wrote outputs/python_scenario_comparison.csv")
    print("Wrote outputs/python_scenario_comparison.png")


if __name__ == "__main__":
    main()
