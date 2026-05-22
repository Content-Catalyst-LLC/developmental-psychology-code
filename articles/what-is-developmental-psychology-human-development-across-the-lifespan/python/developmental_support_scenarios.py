#!/usr/bin/env python3
"""Scenario analysis for developmental support and protective context."""

from __future__ import annotations

from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "developmental_lifespan_panel.csv"
OUT = ROOT / "outputs"
OUT.mkdir(exist_ok=True)


def main() -> None:
    panel = pd.read_csv(DATA)

    scenarios = {
        "baseline": (0,0,0,0,0,0,0,0,0),
        "caregiver_support_boost": (.85,.15,.10,.10,.10,.10,.10,.10,.05),
        "school_support_boost": (.15,.85,.20,.15,.15,.15,.20,.15,.10),
        "counseling_access_boost": (.15,.20,.85,.15,.15,.15,.25,.20,.15),
        "disability_accommodation_boost": (.10,.20,.15,.85,.15,.15,.20,.15,.10),
        "language_access_boost": (.10,.20,.15,.20,.85,.15,.15,.15,.05),
        "community_resource_boost": (.15,.20,.20,.15,.15,.85,.20,.20,.10),
        "structural_risk_reduction": (.20,.25,.20,.20,.15,.25,.25,.85,.25),
        "combined_protective_context": (.85,.85,.85,.85,.85,.85,.85,.85,.85),
    }

    rows = []
    for name, (
        caregiver,
        school,
        counseling,
        disability,
        language,
        community,
        support,
        risk_reduction,
        stress_reduction,
    ) in scenarios.items():
        sim = panel.copy()
        protective_gain = caregiver + school + counseling + disability + language + community + support
        sim["scenario_development"] = (
            sim.development_score
            + 1.10 * caregiver
            + 0.85 * school
            + 0.65 * counseling
            + 0.95 * disability * sim.disability_support_need
            + 0.55 * language
            + 0.55 * community
            + 0.70 * support
            + 2.30 * risk_reduction
            + 1.45 * stress_reduction
            + 0.28 * protective_gain
        )

        s = sim.groupby(["time", "development_profile"], as_index=False).agg(
            average_development=("scenario_development", "mean"),
            average_protective_context=("protective_context", "mean"),
            average_support=("current_support", "mean"),
            average_stress=("acute_stress", "mean"),
            children=("child_id", "nunique"),
        )
        s["scenario"] = name
        rows.append(s)

    result = pd.concat(rows, ignore_index=True)
    result.to_csv(OUT / "python_developmental_support_scenario_comparison.csv", index=False)

    overall = result.groupby(["time", "scenario"], as_index=False).agg(
        average_development=("average_development", "mean")
    )

    plt.figure(figsize=(9, 5.5))
    for name, group in overall.groupby("scenario"):
        plt.plot(group.time, group.average_development, marker="o", label=name)
    plt.xlabel("Time")
    plt.ylabel("Average scenario development score")
    plt.title("Synthetic Developmental Support Scenarios")
    plt.legend(fontsize=8)
    plt.tight_layout()
    plt.savefig(OUT / "python_developmental_support_scenario_comparison.png", dpi=160)
    plt.close()

    print("Wrote developmental support scenario outputs.")


if __name__ == "__main__":
    main()
