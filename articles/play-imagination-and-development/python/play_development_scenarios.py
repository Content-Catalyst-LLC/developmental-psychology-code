#!/usr/bin/env python3
from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "play_development_panel.csv"
OUT = ROOT / "outputs"
OUT.mkdir(exist_ok=True)

def main() -> None:
    panel = pd.read_csv(DATA)

    scenarios = {
        "baseline": (0,0,0,0,0,0,0,0,0,0),
        "pretend_play_boost": (.85,.15,.10,.10,.10,.10,.10,.10,.10,.05),
        "social_play_boost": (.15,.85,.10,.10,.15,.20,.15,.15,.10,.05),
        "constructive_play_boost": (.10,.10,.85,.10,.15,.10,.10,.10,.10,.05),
        "outdoor_play_boost": (.10,.15,.10,.85,.10,.15,.15,.85,.25,.10),
        "caregiver_support_boost": (.20,.20,.15,.15,.85,.20,.25,.15,.15,.10),
        "peer_inclusion_boost": (.15,.35,.15,.15,.20,.85,.35,.20,.35,.10),
        "play_space_quality_boost": (.15,.20,.20,.25,.20,.25,.85,.35,.35,.10),
        "outdoor_safety_boost": (.10,.15,.15,.45,.15,.20,.35,.85,.45,.10),
        "stress_reduction": (.20,.20,.20,.20,.20,.20,.20,.20,.85,.15),
        "combined_play_support": (.85,.85,.85,.85,.85,.85,.85,.85,.85,.85),
    }

    rows = []
    for name, (
        pretend,
        social,
        constructive,
        outdoor,
        caregiver,
        peer,
        space,
        safety,
        stress_reduction,
        restriction_reduction,
    ) in scenarios.items():
        support_gain = pretend + social + constructive + outdoor + caregiver + peer + space + safety
        sim = panel.copy()
        sim["scenario_development"] = (
            sim.development_score
            + 1.15 * pretend
            + 1.05 * social
            + 1.00 * constructive
            + 0.90 * outdoor
            + 1.00 * caregiver
            + 0.90 * peer
            + 0.75 * space
            + 0.65 * safety
            + 1.15 * stress_reduction
            + 0.90 * restriction_reduction
            + 0.25 * support_gain
        )

        s = sim.groupby(["time", "play_profile"], as_index=False).agg(
            average_development=("scenario_development", "mean"),
            average_play_support_context=("play_support_context", "mean"),
            average_play_restriction=("play_restriction", "mean"),
            average_stress=("current_stress", "mean"),
            average_peer_inclusion=("peer_inclusion", "mean"),
            children=("child_id", "nunique"),
        )
        s["scenario"] = name
        rows.append(s)

    result = pd.concat(rows, ignore_index=True)
    result.to_csv(OUT / "python_play_development_scenario_comparison.csv", index=False)

    overall = result.groupby(["time", "scenario"], as_index=False).agg(
        average_development=("average_development", "mean")
    )

    plt.figure(figsize=(9, 5.5))
    for name, group in overall.groupby("scenario"):
        plt.plot(group.time, group.average_development, marker="o", label=name)
    plt.xlabel("Time")
    plt.ylabel("Average scenario development score")
    plt.title("Synthetic Play Development Support Scenarios")
    plt.legend(fontsize=8)
    plt.tight_layout()
    plt.savefig(OUT / "python_play_development_scenario_comparison.png", dpi=160)
    plt.close()

    print("Wrote play development scenario outputs.")

if __name__ == "__main__":
    main()
