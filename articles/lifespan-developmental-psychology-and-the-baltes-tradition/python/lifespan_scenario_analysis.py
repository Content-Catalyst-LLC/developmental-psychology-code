#!/usr/bin/env python3
"""Scenario analysis for support, compensation, health resources, and institutional security."""

from __future__ import annotations

from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "lifespan_baltes_panel.csv"
OUTPUTS_DIR = ROOT / "outputs"
OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)


def main() -> None:
    if not DATA_PATH.exists():
        raise FileNotFoundError("Run python/generate_lifespan_baltes_panel.py first.")

    panel = pd.read_csv(DATA_PATH)

    scenarios = []
    for name, support_boost, comp_boost, health_boost, institutional_boost, loss_reduction in [
        ("baseline", 0.0, 0.0, 0.0, 0.0, 0.0),
        ("context_support_boost", 0.85, 0.0, 0.0, 0.0, 0.15),
        ("compensation_boost", 0.0, 0.85, 0.0, 0.0, 0.20),
        ("health_resource_boost", 0.0, 0.0, 0.85, 0.0, 0.25),
        ("institutional_security_boost", 0.0, 0.0, 0.0, 0.85, 0.25),
        ("combined_lifespan_support", 0.85, 0.85, 0.85, 0.85, 0.80),
    ]:
        simulated = panel.copy()
        simulated["scenario_support"] = simulated["current_support"] + support_boost
        simulated["scenario_comp"] = simulated["current_comp"] + comp_boost
        simulated["scenario_health"] = simulated["health_resource"] + health_boost
        simulated["scenario_institutional"] = simulated["institutional_security"] + institutional_boost
        simulated["scenario_losses"] = simulated["losses"] - loss_reduction

        simulated["scenario_soc"] = (
            simulated["soc_index"]
            + 0.35 * support_boost
            + 0.40 * comp_boost
            + 0.20 * institutional_boost
        )

        simulated["scenario_development"] = (
            simulated["development_score"]
            + 0.95 * support_boost
            + 0.80 * comp_boost
            + 0.65 * health_boost
            + 0.70 * institutional_boost
            + 1.00 * loss_reduction
            + 0.90 * (simulated["scenario_soc"] - simulated["soc_index"])
            + 0.25 * simulated["plasticity"] * support_boost
        )

        summary = simulated.groupby("time", as_index=False).agg(
            average_development=("scenario_development", "mean"),
            average_soc=("scenario_soc", "mean"),
            average_losses=("scenario_losses", "mean"),
        )
        summary["scenario"] = name
        scenarios.append(summary)

    result = pd.concat(scenarios, ignore_index=True)
    result.to_csv(OUTPUTS_DIR / "python_lifespan_scenario_comparison.csv", index=False)

    plt.figure(figsize=(9, 5.5))
    for scenario, group in result.groupby("scenario"):
        plt.plot(group["time"], group["average_development"], marker="o", label=scenario)
    plt.xlabel("Time")
    plt.ylabel("Average scenario development")
    plt.title("Synthetic Lifespan Support and Compensation Scenarios")
    plt.legend()
    plt.tight_layout()
    plt.savefig(OUTPUTS_DIR / "python_lifespan_scenario_comparison.png", dpi=160)
    plt.close()

    print("Wrote outputs/python_lifespan_scenario_comparison.csv")
    print("Wrote outputs/python_lifespan_scenario_comparison.png")


if __name__ == "__main__":
    main()
