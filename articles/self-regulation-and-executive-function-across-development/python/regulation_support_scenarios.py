#!/usr/bin/env python3
from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "regulation_development_panel.csv"
OUT = ROOT / "outputs"
OUT.mkdir(exist_ok=True)

def main() -> None:
    panel = pd.read_csv(DATA)

    scenarios = {
        "baseline": (0,0,0,0,0,0,0,0,0),
        "caregiving_support_boost": (.85,.15,.15,.10,.10,.10,.10,.10,.05),
        "classroom_structure_boost": (.15,.85,.15,.15,.20,.15,.20,.10,.05),
        "sleep_quality_boost": (.15,.15,.85,.10,.10,.10,.10,.10,.05),
        "school_climate_boost": (.15,.20,.10,.85,.25,.20,.25,.15,.10),
        "regulation_scaffolding_boost": (.20,.25,.15,.25,.85,.25,.35,.20,.15),
        "transition_predictability_boost": (.15,.25,.15,.20,.25,.85,.30,.20,.15),
        "disability_accommodation_boost": (.10,.20,.10,.15,.20,.20,.85,.15,.10),
        "stress_reduction": (.20,.20,.20,.20,.20,.20,.20,.85,.20),
        "intervention_expansion": (.25,.25,.20,.20,.35,.30,.25,.25,.85),
        "combined_regulatory_support": (.85,.85,.85,.85,.85,.85,.85,.85,.85),
    }

    rows = []
    for name, (
        caregiving,
        structure,
        sleep,
        school,
        scaffolding,
        transition,
        accommodation,
        stress_reduction,
        intervention_boost,
    ) in scenarios.items():
        support_gain = caregiving + structure + sleep + school + scaffolding + transition + accommodation
        sim = panel.copy()
        sim["scenario_regulation"] = (
            sim.regulation_score
            + 1.15 * caregiving
            + 1.05 * structure
            + 0.90 * sleep
            + 0.80 * school
            + 0.95 * scaffolding
            + 0.80 * transition
            + 0.90 * accommodation * sim.disability_support_need
            + 1.25 * stress_reduction
            + 1.10 * intervention_boost
            + 0.25 * support_gain
        )

        s = sim.groupby(["time", "regulation_profile"], as_index=False).agg(
            average_regulation=("scenario_regulation", "mean"),
            average_regulatory_support_context=("regulatory_support_context", "mean"),
            average_stress=("acute_stress", "mean"),
            average_sleep=("current_sleep", "mean"),
            intervention_rate=("intervention_exposure", "mean"),
            children=("child_id", "nunique"),
        )
        s["scenario"] = name
        rows.append(s)

    result = pd.concat(rows, ignore_index=True)
    result.to_csv(OUT / "python_regulation_support_scenario_comparison.csv", index=False)

    overall = result.groupby(["time", "scenario"], as_index=False).agg(
        average_regulation=("average_regulation", "mean")
    )

    plt.figure(figsize=(9, 5.5))
    for name, group in overall.groupby("scenario"):
        plt.plot(group.time, group.average_regulation, marker="o", label=name)
    plt.xlabel("Time")
    plt.ylabel("Average scenario regulation score")
    plt.title("Synthetic Self-Regulation Support Scenarios")
    plt.legend(fontsize=8)
    plt.tight_layout()
    plt.savefig(OUT / "python_regulation_support_scenario_comparison.png", dpi=160)
    plt.close()

    print("Wrote regulation support scenario outputs.")

if __name__ == "__main__":
    main()
