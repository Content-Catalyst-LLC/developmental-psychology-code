#!/usr/bin/env python3
from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "attachment_development_panel.csv"
OUT = ROOT / "outputs"
OUT.mkdir(exist_ok=True)

def main() -> None:
    panel = pd.read_csv(DATA)

    scenarios = {
        "baseline": (0,0,0,0,0,0,0,0),
        "caregiving_responsiveness_boost": (.85,.15,.15,.10,.10,.10,.10,.05),
        "relational_repair_boost": (.20,.85,.20,.10,.10,.20,.10,.05),
        "caregiver_support_boost": (.20,.20,.85,.15,.15,.20,.15,.10),
        "childcare_continuity_boost": (.15,.15,.20,.85,.15,.20,.15,.10),
        "family_service_access_boost": (.15,.20,.25,.20,.15,.85,.20,.15),
        "neighborhood_safety_boost": (.15,.15,.20,.20,.85,.20,.15,.15),
        "stress_reduction": (.20,.20,.25,.20,.20,.20,.85,.20),
        "combined_attachment_support": (.85,.85,.85,.85,.85,.85,.85,.85),
    }

    rows = []
    for name, (
        care,
        repair,
        caregiver_support,
        childcare,
        safety,
        services,
        stress_reduction,
        ecology,
    ) in scenarios.items():
        support_gain = care + repair + caregiver_support + childcare + safety + services + ecology
        sim = panel.copy()
        sim["scenario_regulation"] = (
            sim.regulation_score
            + 1.35 * care
            + 1.10 * repair
            + 1.00 * caregiver_support
            + 0.80 * childcare
            + 0.75 * safety
            + 0.80 * services
            + 0.75 * ecology
            + 1.30 * stress_reduction
            + 0.70 * services * sim.disability_support_need
            + 0.25 * support_gain
        )

        s = sim.groupby(["time", "attachment_profile"], as_index=False).agg(
            average_regulation=("scenario_regulation", "mean"),
            average_caregiving_support_context=("caregiving_support_context", "mean"),
            average_care=("current_care", "mean"),
            average_repair=("current_repair", "mean"),
            average_stress=("current_stress", "mean"),
            children=("child_id", "nunique"),
        )
        s["scenario"] = name
        rows.append(s)

    result = pd.concat(rows, ignore_index=True)
    result.to_csv(OUT / "python_attachment_support_scenario_comparison.csv", index=False)

    overall = result.groupby(["time", "scenario"], as_index=False).agg(
        average_regulation=("average_regulation", "mean")
    )

    plt.figure(figsize=(9, 5.5))
    for name, group in overall.groupby("scenario"):
        plt.plot(group.time, group.average_regulation, marker="o", label=name)
    plt.xlabel("Time")
    plt.ylabel("Average scenario regulation score")
    plt.title("Synthetic Attachment and Caregiving Support Scenarios")
    plt.legend(fontsize=8)
    plt.tight_layout()
    plt.savefig(OUT / "python_attachment_support_scenario_comparison.png", dpi=160)
    plt.close()

    print("Wrote attachment support scenario outputs.")

if __name__ == "__main__":
    main()
