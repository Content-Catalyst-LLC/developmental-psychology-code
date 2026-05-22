#!/usr/bin/env python3
from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "language_development_panel.csv"
OUT = ROOT / "outputs"
OUT.mkdir(exist_ok=True)

def main() -> None:
    panel = pd.read_csv(DATA)

    scenarios = {
        "baseline": (0,0,0,0,0,0,0,0,0,0),
        "responsive_interaction_boost": (.85,.15,.20,.20,.10,.10,.10,.10,.10,.05),
        "shared_reading_boost": (.15,.85,.15,.15,.10,.15,.85,.20,.15,.05),
        "joint_attention_boost": (.25,.15,.85,.25,.10,.15,.15,.15,.15,.05),
        "turn_taking_boost": (.20,.15,.25,.85,.10,.15,.15,.15,.15,.05),
        "hearing_support_boost": (.15,.15,.20,.20,.85,.10,.15,.15,.15,.05),
        "home_language_recognition_boost": (.15,.20,.15,.15,.10,.85,.15,.20,.25,.10),
        "book_access_boost": (.15,.85,.10,.10,.10,.20,.85,.20,.10,.05),
        "early_education_quality_boost": (.20,.25,.20,.20,.15,.25,.25,.85,.20,.10),
        "stress_reduction": (.20,.20,.20,.20,.20,.20,.20,.20,.85,.20),
        "combined_language_support": (.85,.85,.85,.85,.85,.85,.85,.85,.85,.85),
    }

    rows = []
    for name, (
        interaction,
        reading,
        joint_attention,
        turn_taking,
        hearing,
        home_language,
        books,
        education,
        stress_reduction,
        ecology,
    ) in scenarios.items():
        support_gain = interaction + reading + joint_attention + turn_taking + hearing + home_language + books + education + ecology
        sim = panel.copy()
        sim["scenario_language"] = (
            sim.language_score
            + 1.30 * interaction
            + 1.10 * reading
            + 1.05 * joint_attention
            + 1.00 * turn_taking
            + 0.95 * hearing
            + 0.65 * home_language
            + 0.70 * books
            + 0.75 * education
            + 0.70 * ecology
            + 1.20 * stress_reduction
            + 0.50 * sim.multilingual_exposure * home_language
            + 0.25 * support_gain
        )

        s = sim.groupby(["time", "language_profile"], as_index=False).agg(
            average_language=("scenario_language", "mean"),
            average_language_support_context=("language_support_context", "mean"),
            average_interaction=("current_interaction", "mean"),
            average_reading=("current_reading", "mean"),
            average_stress=("current_stress", "mean"),
            children=("child_id", "nunique"),
        )
        s["scenario"] = name
        rows.append(s)

    result = pd.concat(rows, ignore_index=True)
    result.to_csv(OUT / "python_language_support_scenario_comparison.csv", index=False)

    overall = result.groupby(["time", "scenario"], as_index=False).agg(
        average_language=("average_language", "mean")
    )

    plt.figure(figsize=(9, 5.5))
    for name, group in overall.groupby("scenario"):
        plt.plot(group.time, group.average_language, marker="o", label=name)
    plt.xlabel("Time")
    plt.ylabel("Average scenario language score")
    plt.title("Synthetic Language Support Scenarios")
    plt.legend(fontsize=8)
    plt.tight_layout()
    plt.savefig(OUT / "python_language_support_scenario_comparison.png", dpi=160)
    plt.close()

    print("Wrote language support scenario outputs.")

if __name__ == "__main__":
    main()
