#!/usr/bin/env python3
from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "moral_development_panel.csv"
OUT = ROOT / "outputs"
OUT.mkdir(exist_ok=True)

def main() -> None:
    panel = pd.read_csv(DATA)
    scenarios = {
        "baseline": (0,0,0,0,0,0,0,0,0,0),
        "caregiving_guidance_boost": (.85,.15,.10,.10,.15,.10,.10,.10,.10,.05),
        "empathy_boost": (.15,.85,.15,.10,.15,.10,.10,.10,.10,.05),
        "peer_fairness_boost": (.10,.15,.85,.15,.15,.10,.15,.15,.10,.10),
        "repair_opportunity_boost": (.15,.15,.15,.85,.20,.15,.20,.15,.20,.10),
        "school_moral_climate_boost": (.15,.15,.20,.20,.85,.25,.25,.20,.20,.15),
        "restorative_practice_boost": (.15,.15,.20,.85,.25,.85,.25,.20,.30,.15),
        "anti_bullying_boost": (.15,.20,.20,.25,.25,.25,.85,.20,.45,.20),
        "digital_moral_safety_boost": (.10,.10,.15,.10,.15,.15,.20,.85,.20,.55),
        "exclusion_reduction": (.20,.20,.25,.30,.20,.30,.45,.20,.85,.25),
        "combined_moral_support": (.85,.85,.85,.85,.85,.85,.85,.85,.85,.85),
    }

    rows = []
    for name, (guidance, empathy, peer, repair, climate, restorative, bullying, digital, exclusion_reduction, pressure_reduction) in scenarios.items():
        support_gain = guidance + empathy + peer + repair + climate + restorative + bullying + digital
        sim = panel.copy()
        sim["scenario_conscience"] = (
            sim.conscience_score
            + 1.05 * guidance + 1.00 * empathy + 0.95 * peer + 0.95 * repair
            + 0.80 * climate + 0.90 * restorative + 0.80 * bullying + 0.55 * digital
            + 1.20 * exclusion_reduction + 0.45 * pressure_reduction + 0.25 * support_gain
        )
        sim["scenario_moral_action"] = (
            sim.moral_action_score
            + 0.20 * sim["scenario_conscience"] + 0.85 * peer + 0.80 * empathy
            + 0.70 * repair + 1.10 * pressure_reduction + 0.95 * exclusion_reduction
            + 0.35 * support_gain
        )
        s = sim.groupby(["time", "moral_profile"], as_index=False).agg(
            average_conscience=("scenario_conscience", "mean"),
            average_moral_action=("scenario_moral_action", "mean"),
            average_moral_support_context=("moral_support_context", "mean"),
            average_exclusion=("current_exclusion", "mean"),
            average_peer_pressure=("peer_pressure", "mean"),
            children=("child_id", "nunique"),
        )
        s["scenario"] = name
        rows.append(s)

    result = pd.concat(rows, ignore_index=True)
    result.to_csv(OUT / "python_moral_development_scenario_comparison.csv", index=False)

    overall = result.groupby(["time", "scenario"], as_index=False).agg(
        average_conscience=("average_conscience", "mean")
    )
    plt.figure(figsize=(9, 5.5))
    for name, group in overall.groupby("scenario"):
        plt.plot(group.time, group.average_conscience, marker="o", label=name)
    plt.xlabel("Time")
    plt.ylabel("Average scenario conscience score")
    plt.title("Synthetic Moral Development Support Scenarios")
    plt.legend(fontsize=8)
    plt.tight_layout()
    plt.savefig(OUT / "python_moral_development_scenario_comparison.png", dpi=160)
    plt.close()
    print("Wrote moral development scenario outputs.")

if __name__ == "__main__":
    main()
