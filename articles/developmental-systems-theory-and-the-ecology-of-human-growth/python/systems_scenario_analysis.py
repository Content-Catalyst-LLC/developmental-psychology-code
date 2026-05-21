#!/usr/bin/env python3
"""Scenario analysis for family, peer, school, neighborhood, service, and material supports."""

from __future__ import annotations

from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "developmental_systems_panel.csv"
OUTPUTS_DIR = ROOT / "outputs"
OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)


def main() -> None:
    if not DATA_PATH.exists():
        raise FileNotFoundError("Run python/generate_developmental_systems_panel.py first.")

    panel = pd.read_csv(DATA_PATH)

    scenarios = []
    for name, family_boost, peer_boost, school_boost, neighborhood_boost, service_boost, material_boost, stress_reduction in [
        ("baseline", 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0),
        ("family_support", 0.80, 0.0, 0.0, 0.0, 0.0, 0.0, 0.20),
        ("peer_belonging", 0.0, 0.80, 0.0, 0.0, 0.0, 0.0, 0.10),
        ("school_climate", 0.0, 0.0, 0.80, 0.0, 0.0, 0.0, 0.20),
        ("neighborhood_safety", 0.0, 0.0, 0.0, 0.80, 0.0, 0.0, 0.25),
        ("service_material_support", 0.0, 0.0, 0.0, 0.0, 0.75, 0.75, 0.30),
        ("combined_ecological_support", 0.80, 0.80, 0.80, 0.80, 0.75, 0.75, 0.90),
    ]:
        simulated = panel.copy()
        simulated["scenario_family"] = simulated["current_family"] + family_boost
        simulated["scenario_peer"] = simulated["current_peer"] + peer_boost
        simulated["scenario_school"] = simulated["school_climate"] + school_boost
        simulated["scenario_neighborhood"] = simulated["neighborhood_safety"] + neighborhood_boost
        simulated["scenario_service"] = simulated["service_access"] + service_boost
        simulated["scenario_material"] = simulated["material_security"] + material_boost
        simulated["scenario_stress"] = simulated["ecological_stress"] - stress_reduction

        simulated["scenario_ecological_support"] = (
            simulated["ecological_support"]
            + family_boost
            + peer_boost
            + school_boost
            + neighborhood_boost
            + service_boost
            + material_boost
        )

        simulated["scenario_development"] = (
            simulated["development_score"]
            + 1.15 * family_boost
            + 0.95 * peer_boost
            + 0.95 * school_boost
            + 0.85 * neighborhood_boost
            + 0.70 * service_boost
            + 0.65 * material_boost
            + 1.10 * stress_reduction
            + 0.35 * simulated["biological_sensitivity"] * family_boost
            + 0.25 * simulated["biological_sensitivity"] * stress_reduction
        )

        summary = simulated.groupby("time", as_index=False).agg(
            average_development=("scenario_development", "mean"),
            average_ecological_support=("scenario_ecological_support", "mean"),
            average_ecological_stress=("scenario_stress", "mean"),
        )
        summary["scenario"] = name
        scenarios.append(summary)

    result = pd.concat(scenarios, ignore_index=True)
    result.to_csv(OUTPUTS_DIR / "python_systems_scenario_comparison.csv", index=False)

    plt.figure(figsize=(9, 5.5))
    for scenario, group in result.groupby("scenario"):
        plt.plot(group["time"], group["average_development"], marker="o", label=scenario)
    plt.xlabel("Time")
    plt.ylabel("Average scenario development")
    plt.title("Synthetic Developmental Systems Support Scenarios")
    plt.legend()
    plt.tight_layout()
    plt.savefig(OUTPUTS_DIR / "python_systems_scenario_comparison.png", dpi=160)
    plt.close()

    print("Wrote outputs/python_systems_scenario_comparison.csv")
    print("Wrote outputs/python_systems_scenario_comparison.png")


if __name__ == "__main__":
    main()
