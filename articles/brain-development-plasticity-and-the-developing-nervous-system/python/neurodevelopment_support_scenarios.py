#!/usr/bin/env python3
from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "brain_development_panel.csv"
OUT = ROOT / "outputs"
OUT.mkdir(exist_ok=True)

def main():
    panel = pd.read_csv(DATA)
    scenarios = {
        "baseline": (0,0,0,0,0,0,0,0),
        "family_support_boost": (.85,.20,.20,.20,.10,.10,.10,.05),
        "learning_opportunity_boost": (.20,.85,.15,.15,.20,.10,.10,.05),
        "sleep_quality_boost": (.15,.15,.85,.20,.10,.10,.20,.05),
        "sensory_support_boost": (.15,.15,.20,.85,.10,.10,.10,.05),
        "health_access_boost": (.15,.20,.20,.20,.20,.85,.10,.05),
        "environmental_risk_reduction": (.10,.10,.10,.10,.20,.20,.10,.20),
        "stress_reduction": (.20,.20,.25,.20,.20,.20,.85,.20),
        "combined_neurodevelopmental_support": (.85,.85,.85,.85,.85,.85,.85,.85),
    }

    rows = []
    for name, (family, learning, sleep, sensory, school, health, stress_reduction, risk_reduction) in scenarios.items():
        support_gain = family + learning + sleep + sensory + school + health + stress_reduction + risk_reduction
        sim = panel.copy()
        sim["scenario_neural_state"] = (
            sim.neural_state + 1.15*family + 1.20*learning + 0.90*sleep + 0.75*sensory +
            0.80*school + 0.75*health + 1.30*stress_reduction + 0.70*risk_reduction + 0.25*support_gain
        )
        sim["scenario_developmental_outcome"] = (
            sim.developmental_outcome + 0.72*(sim.scenario_neural_state - sim.neural_state) +
            0.85*family + 0.80*learning + 0.70*sleep + 0.65*sensory + 0.95*stress_reduction + 0.65*risk_reduction
        )

        s = sim.groupby(["time", "neurodevelopment_profile"], as_index=False).agg(
            average_developmental_outcome=("scenario_developmental_outcome", "mean"),
            average_neural_state=("scenario_neural_state", "mean"),
            average_stress=("acute_stress", "mean"),
            children=("child_id", "nunique"),
        )
        s["scenario"] = name
        rows.append(s)

    result = pd.concat(rows, ignore_index=True)
    result.to_csv(OUT / "python_neurodevelopment_support_scenario_comparison.csv", index=False)

    overall = result.groupby(["time", "scenario"], as_index=False).agg(
        average_developmental_outcome=("average_developmental_outcome", "mean")
    )

    plt.figure(figsize=(9, 5.5))
    for name, group in overall.groupby("scenario"):
        plt.plot(group.time, group.average_developmental_outcome, marker="o", label=name)
    plt.xlabel("Time")
    plt.ylabel("Average scenario developmental outcome")
    plt.title("Synthetic Neurodevelopmental Support Scenarios")
    plt.legend(fontsize=8)
    plt.tight_layout()
    plt.savefig(OUT / "python_neurodevelopment_support_scenario_comparison.png", dpi=160)
    plt.close()

    print("Wrote neurodevelopment support scenario outputs.")

if __name__ == "__main__":
    main()
