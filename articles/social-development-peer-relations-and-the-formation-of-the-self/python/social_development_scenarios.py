#!/usr/bin/env python3
from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "social_development_panel.csv"
OUT = ROOT / "outputs"
OUT.mkdir(exist_ok=True)

def main() -> None:
    panel = pd.read_csv(DATA)
    scenarios = {
        "baseline": (0,0,0,0,0,0,0,0,0),
        "peer_support_boost": (.85,.20,.10,.10,.10,.10,.10,.10,.05),
        "friendship_quality_boost": (.20,.85,.10,.10,.10,.10,.10,.10,.05),
        "family_support_boost": (.15,.15,.85,.10,.10,.10,.10,.10,.05),
        "school_connectedness_boost": (.15,.15,.15,.85,.20,.20,.20,.10,.10),
        "teacher_support_boost": (.10,.10,.15,.20,.85,.20,.20,.10,.10),
        "inclusion_climate_boost": (.15,.20,.15,.25,.25,.85,.35,.25,.15),
        "anti_bullying_boost": (.15,.20,.15,.25,.25,.35,.85,.45,.20),
        "digital_comparison_reduction": (.10,.15,.10,.15,.10,.20,.20,.10,.85),
        "combined_social_support": (.85,.85,.85,.85,.85,.85,.85,.85,.85),
    }

    rows = []
    for name, (peer, friendship, family, connectedness, teacher, inclusion, bullying, exclusion_reduction, digital_reduction) in scenarios.items():
        support_gain = peer + friendship + family + connectedness + teacher + inclusion + bullying
        sim = panel.copy()
        sim["scenario_social_self"] = (
            sim.social_self_score
            + 1.10 * peer
            + 1.00 * friendship
            + 0.95 * family
            + 0.90 * connectedness
            + 0.75 * teacher
            + 0.80 * inclusion
            + 0.80 * bullying
            + 1.20 * exclusion_reduction
            + 0.75 * digital_reduction
            + 0.25 * support_gain
        )
        s = sim.groupby(["time", "social_profile"], as_index=False).agg(
            average_social_self=("scenario_social_self", "mean"),
            average_social_support_context=("social_support_context", "mean"),
            average_exclusion=("current_exclusion", "mean"),
            average_bullying=("bullying_exposure", "mean"),
            average_digital_comparison=("digital_comparison_stress", "mean"),
            children=("child_id", "nunique"),
        )
        s["scenario"] = name
        rows.append(s)

    result = pd.concat(rows, ignore_index=True)
    result.to_csv(OUT / "python_social_development_scenario_comparison.csv", index=False)

    overall = result.groupby(["time", "scenario"], as_index=False).agg(
        average_social_self=("average_social_self", "mean")
    )

    plt.figure(figsize=(9, 5.5))
    for name, group in overall.groupby("scenario"):
        plt.plot(group.time, group.average_social_self, marker="o", label=name)
    plt.xlabel("Time")
    plt.ylabel("Average scenario social-self score")
    plt.title("Synthetic Social Development Support Scenarios")
    plt.legend(fontsize=8)
    plt.tight_layout()
    plt.savefig(OUT / "python_social_development_scenario_comparison.png", dpi=160)
    plt.close()
    print("Wrote social development scenario outputs.")

if __name__ == "__main__":
    main()
