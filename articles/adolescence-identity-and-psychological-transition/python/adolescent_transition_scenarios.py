#!/usr/bin/env python3
from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "adolescence_identity_panel.csv"
OUT = ROOT / "outputs"
OUT.mkdir(exist_ok=True)

def main() -> None:
    panel = pd.read_csv(DATA)

    scenarios = {
        "baseline": (0,0,0,0,0,0,0,0,0,0),
        "peer_support_boost": (.85,.10,.10,.10,.10,.15,.10,.10,.10,.05),
        "family_support_boost": (.10,.85,.10,.15,.10,.10,.10,.10,.10,.05),
        "school_connectedness_boost": (.15,.10,.85,.15,.20,.20,.20,.10,.15,.10),
        "future_orientation_boost": (.10,.10,.20,.85,.15,.20,.10,.10,.05,.05),
        "counseling_access_boost": (.10,.15,.20,.15,.85,.15,.20,.15,.20,.15),
        "identity_safety_boost": (.15,.15,.20,.15,.20,.15,.85,.20,.35,.15),
        "digital_safety_boost": (.10,.10,.15,.10,.15,.10,.20,.85,.15,.55),
        "exclusion_reduction": (.25,.20,.25,.20,.25,.25,.35,.25,.85,.30),
        "combined_supportive_transition": (.85,.85,.85,.85,.85,.85,.85,.85,.85,.85),
    }

    rows = []
    for name, (peer, family, school, future, counsel, extra, identity, digital, exclusion_red, digital_red) in scenarios.items():
        sim = panel.copy()
        support_gain = peer + family + school + future + counsel + extra + identity + digital
        sim["scenario_identity"] = (
            sim.identity_score +
            1.10 * peer + 1.00 * family + 0.95 * school + 0.90 * future +
            0.70 * counsel + 0.65 * extra + 0.85 * identity + 0.55 * digital +
            1.25 * exclusion_red + 0.75 * digital_red + 0.18 * support_gain
        )
        s = sim.groupby(["time", "identity_profile"], as_index=False).agg(
            average_identity=("scenario_identity", "mean"),
            average_support_context=("support_context", "mean"),
            average_exclusion=("current_exclusion", "mean"),
            average_digital_stress=("digital_stress", "mean"),
            adolescents=("adolescent_id", "nunique"),
        )
        s["scenario"] = name
        rows.append(s)

    result = pd.concat(rows, ignore_index=True)
    result.to_csv(OUT / "python_adolescent_transition_scenario_comparison.csv", index=False)

    overall = result.groupby(["time", "scenario"], as_index=False).agg(average_identity=("average_identity", "mean"))
    plt.figure(figsize=(9, 5.5))
    for name, group in overall.groupby("scenario"):
        plt.plot(group.time, group.average_identity, marker="o", label=name)
    plt.xlabel("Time")
    plt.ylabel("Average scenario identity score")
    plt.title("Synthetic Adolescent Transition Support Scenarios")
    plt.legend(fontsize=8)
    plt.tight_layout()
    plt.savefig(OUT / "python_adolescent_transition_scenario_comparison.png", dpi=160)
    plt.close()
    print("Wrote scenario outputs.")

if __name__ == "__main__":
    main()
