#!/usr/bin/env python3
"""Scenario analysis for connection, reflection, health burden, dignity, service, and community support."""

from __future__ import annotations

from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "wisdom_meaning_later_life_panel.csv"
OUTPUTS_DIR = ROOT / "outputs"
OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)


def main() -> None:
    if not DATA_PATH.exists():
        raise FileNotFoundError("Run python/generate_wisdom_meaning_panel.py first.")

    panel = pd.read_csv(DATA_PATH)

    scenarios = []
    for name, connection_boost, reflection_boost, support_boost, legacy_boost, dignity_boost, service_boost, community_boost, health_reduction in [
        ("baseline", 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0),
        ("social_connection_support", 0.85, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.10),
        ("life_review_reflection", 0.0, 0.85, 0.0, 0.0, 0.0, 0.0, 0.0, 0.05),
        ("adaptive_support", 0.0, 0.0, 0.85, 0.0, 0.0, 0.0, 0.0, 0.20),
        ("legacy_intergenerational_program", 0.30, 0.20, 0.0, 0.85, 0.0, 0.0, 0.25, 0.05),
        ("dignity_service_access", 0.0, 0.0, 0.20, 0.0, 0.85, 0.85, 0.0, 0.20),
        ("community_participation", 0.35, 0.0, 0.0, 0.20, 0.20, 0.20, 0.85, 0.10),
        ("combined_later_life_support", 0.85, 0.85, 0.85, 0.85, 0.85, 0.85, 0.85, 0.85),
    ]:
        simulated = panel.copy()
        simulated["scenario_connection"] = simulated["current_connection"] + connection_boost
        simulated["scenario_reflection"] = simulated["current_reflection"] + reflection_boost
        simulated["scenario_support"] = simulated["current_support"] + support_boost
        simulated["scenario_legacy"] = simulated["current_legacy"] + legacy_boost
        simulated["scenario_dignity"] = simulated["dignity_support"] + dignity_boost
        simulated["scenario_service"] = simulated["service_access"] + service_boost
        simulated["scenario_community"] = simulated["community_participation"] + community_boost
        simulated["scenario_health"] = simulated["current_health"] - health_reduction

        simulated["scenario_wisdom"] = (
            simulated["wisdom_index"]
            + 0.35 * reflection_boost
            + 0.25 * connection_boost
            + 0.20 * legacy_boost
            + 0.20 * dignity_boost
            + 0.20 * health_reduction
        )

        simulated["scenario_meaning"] = (
            simulated["meaning_score"]
            + 1.10 * connection_boost
            + 1.05 * reflection_boost
            + 0.90 * support_boost
            + 0.75 * legacy_boost
            + 0.75 * dignity_boost
            + 0.60 * service_boost
            + 0.55 * community_boost
            + 1.15 * health_reduction
            + 0.85 * (simulated["scenario_wisdom"] - simulated["wisdom_index"])
        )

        summary = simulated.groupby("time", as_index=False).agg(
            average_meaning=("scenario_meaning", "mean"),
            average_wisdom=("scenario_wisdom", "mean"),
            average_health=("scenario_health", "mean"),
        )
        summary["scenario"] = name
        scenarios.append(summary)

    result = pd.concat(scenarios, ignore_index=True)
    result.to_csv(OUTPUTS_DIR / "python_wisdom_meaning_scenario_comparison.csv", index=False)

    plt.figure(figsize=(9, 5.5))
    for scenario, group in result.groupby("scenario"):
        plt.plot(group["time"], group["average_meaning"], marker="o", label=scenario)
    plt.xlabel("Time")
    plt.ylabel("Average scenario meaning")
    plt.title("Synthetic Later-Life Meaning Support Scenarios")
    plt.legend(fontsize=8)
    plt.tight_layout()
    plt.savefig(OUTPUTS_DIR / "python_wisdom_meaning_scenario_comparison.png", dpi=160)
    plt.close()

    print("Wrote outputs/python_wisdom_meaning_scenario_comparison.csv")
    print("Wrote outputs/python_wisdom_meaning_scenario_comparison.png")


if __name__ == "__main__":
    main()
