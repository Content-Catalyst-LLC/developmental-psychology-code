#!/usr/bin/env python3
from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "puberty_embodiment_panel.csv"
OUT = ROOT / "outputs"
OUT.mkdir(exist_ok=True)

def main() -> None:
    panel = pd.read_csv(DATA)

    scenarios = {
        "baseline": (0,0,0,0,0,0,0,0,0,0),
        "family_support_boost": (.85,.10,.10,.10,.10,.10,.10,.10,.10,.05),
        "school_support_boost": (.10,.85,.20,.15,.15,.15,.20,.10,.15,.10),
        "health_education_boost": (.15,.20,.85,.20,.20,.20,.15,.10,.20,.10),
        "privacy_protection_boost": (.15,.20,.25,.85,.20,.15,.20,.10,.25,.15),
        "menstrual_support_boost": (.10,.15,.20,.20,.85,.15,.15,.10,.15,.10),
        "disability_accommodation_boost": (.10,.20,.20,.20,.15,.85,.20,.15,.20,.10),
        "anti_harassment_boost": (.20,.25,.20,.25,.15,.20,.85,.20,.45,.20),
        "digital_safety_boost": (.10,.10,.10,.10,.10,.15,.20,.85,.15,.55),
        "stigma_reduction": (.20,.25,.20,.25,.20,.20,.45,.20,.85,.30),
        "combined_protective_context": (.85,.85,.85,.85,.85,.85,.85,.85,.85,.85),
    }

    rows = []
    for name, (family, school, health, privacy, menstrual, disability, harassment, digital, stigma_reduction, digital_stress_reduction) in scenarios.items():
        sim = panel.copy()
        protective_gain = family + school + health + privacy + menstrual + disability + harassment + digital
        sim["scenario_adjustment"] = (
            sim.adjustment_score + 1.05 * family + 0.80 * school + 0.75 * health +
            0.70 * privacy + 0.65 * menstrual + 0.75 * disability +
            0.80 * harassment + 0.55 * digital + 1.20 * stigma_reduction +
            0.75 * digital_stress_reduction + 0.25 * protective_gain
        )
        s = sim.groupby(["time", "puberty_profile"], as_index=False).agg(
            average_adjustment=("scenario_adjustment", "mean"),
            average_protective_context=("protective_context", "mean"),
            average_stigma=("current_stigma", "mean"),
            average_body_concern=("current_body_concern", "mean"),
            average_digital_visibility_stress=("digital_visibility_stress", "mean"),
            adolescents=("adolescent_id", "nunique"),
        )
        s["scenario"] = name
        rows.append(s)

    result = pd.concat(rows, ignore_index=True)
    result.to_csv(OUT / "python_puberty_transition_scenario_comparison.csv", index=False)

    overall = result.groupby(["time", "scenario"], as_index=False).agg(average_adjustment=("average_adjustment", "mean"))

    plt.figure(figsize=(9, 5.5))
    for name, group in overall.groupby("scenario"):
        plt.plot(group.time, group.average_adjustment, marker="o", label=name)
    plt.xlabel("Time")
    plt.ylabel("Average scenario adjustment score")
    plt.title("Synthetic Puberty Support and Protective Context Scenarios")
    plt.legend(fontsize=8)
    plt.tight_layout()
    plt.savefig(OUT / "python_puberty_transition_scenario_comparison.png", dpi=160)
    plt.close()

    print("Wrote puberty transition scenario outputs.")

if __name__ == "__main__":
    main()
