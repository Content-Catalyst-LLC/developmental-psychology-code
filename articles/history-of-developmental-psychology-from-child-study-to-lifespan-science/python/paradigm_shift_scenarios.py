#!/usr/bin/env python3
"""Scenario analysis for synthetic historical paradigm broadening."""

from __future__ import annotations

from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "developmental_psychology_history_panel.csv"
OUT = ROOT / "outputs"
OUT.mkdir(exist_ok=True)


def main() -> None:
    df = pd.read_csv(DATA)

    scenarios = {
        "baseline": {
            "institutional_support": 0.00,
            "methodological_advantage": 0.00,
            "social_relevance": 0.00,
            "critique_index": 0.00,
        },
        "institutional_acceleration": {
            "institutional_support": 0.18,
            "methodological_advantage": 0.06,
            "social_relevance": 0.03,
            "critique_index": 0.02,
        },
        "methodological_acceleration": {
            "institutional_support": 0.05,
            "methodological_advantage": 0.18,
            "social_relevance": 0.03,
            "critique_index": 0.03,
        },
        "public_policy_relevance": {
            "institutional_support": 0.06,
            "methodological_advantage": 0.04,
            "social_relevance": 0.20,
            "critique_index": 0.04,
        },
        "critical_broadening": {
            "institutional_support": 0.06,
            "methodological_advantage": 0.05,
            "social_relevance": 0.08,
            "critique_index": 0.22,
        },
        "combined_broadening": {
            "institutional_support": 0.16,
            "methodological_advantage": 0.16,
            "social_relevance": 0.18,
            "critique_index": 0.18,
        },
    }

    rows = []
    for name, boosts in scenarios.items():
        sim = df.copy()
        for col, boost in boosts.items():
            sim[f"scenario_{col}"] = sim[col] + boost

        sim["scenario_broadening_index"] = (
            sim["broadening_index"]
            + 0.18 * boosts["institutional_support"]
            + 0.20 * boosts["methodological_advantage"]
            + 0.22 * boosts["social_relevance"]
            + 0.30 * boosts["critique_index"]
        )
        sim["scenario_lifespan_index"] = (
            sim["lifespan_index"]
            + 0.10 * boosts["institutional_support"]
            + 0.10 * boosts["methodological_advantage"]
            + 0.16 * boosts["social_relevance"]
            + 0.08 * boosts["critique_index"]
        )
        sim["scenario_ecological_systems_index"] = (
            sim["ecological_systems_index"]
            + 0.10 * boosts["institutional_support"]
            + 0.12 * boosts["methodological_advantage"]
            + 0.15 * boosts["social_relevance"]
            + 0.22 * boosts["critique_index"]
        )

        out = sim[[
            "year",
            "scenario_broadening_index",
            "scenario_lifespan_index",
            "scenario_ecological_systems_index",
        ]].copy()
        out["scenario"] = name
        rows.append(out)

    result = pd.concat(rows, ignore_index=True)
    result.to_csv(OUT / "python_paradigm_shift_scenarios.csv", index=False)

    plt.figure(figsize=(9, 5.5))
    for name, group in result.groupby("scenario"):
        plt.plot(group["year"], group["scenario_broadening_index"], label=name)
    plt.xlabel("Year")
    plt.ylabel("Synthetic broadening index")
    plt.title("Scenario Analysis: Broadening in Developmental Psychology")
    plt.legend(fontsize=8)
    plt.tight_layout()
    plt.savefig(OUT / "python_paradigm_shift_scenarios.png", dpi=160)
    plt.close()

    print("Wrote paradigm-shift scenario outputs.")


if __name__ == "__main__":
    main()
