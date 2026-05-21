#!/usr/bin/env python3
"""Scenario analysis for support, recognition, consent knowledge, and stigma reduction."""

from __future__ import annotations

from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "gender_sexual_development_panel.csv"
OUTPUTS_DIR = ROOT / "outputs"
OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)


def main() -> None:
    if not DATA_PATH.exists():
        raise FileNotFoundError("Run python/generate_gender_sexual_development_panel.py first.")

    panel = pd.read_csv(DATA_PATH)

    scenarios = []
    for name, family_boost, recognition_boost, consent_boost, connectedness_boost, climate_boost, education_boost, harassment_boost, stigma_reduction in [
        ("baseline", 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0),
        ("family_support_boost", 0.85, 0.20, 0.10, 0.15, 0.0, 0.0, 0.0, 0.10),
        ("social_recognition_boost", 0.15, 0.85, 0.10, 0.20, 0.0, 0.0, 0.10, 0.15),
        ("consent_education_boost", 0.10, 0.10, 0.85, 0.15, 0.10, 0.85, 0.15, 0.10),
        ("school_connectedness_boost", 0.10, 0.20, 0.15, 0.85, 0.50, 0.20, 0.20, 0.15),
        ("anti_harassment_support_boost", 0.10, 0.25, 0.20, 0.25, 0.30, 0.20, 0.85, 0.30),
        ("stigma_reduction", 0.15, 0.25, 0.20, 0.20, 0.20, 0.20, 0.30, 0.85),
        ("combined_protective_context", 0.85, 0.85, 0.85, 0.85, 0.85, 0.85, 0.85, 0.85),
    ]:
        simulated = panel.copy()
        simulated["scenario_family"] = simulated["current_family_support"] + family_boost
        simulated["scenario_recognition"] = simulated["current_recognition"] + recognition_boost
        simulated["scenario_consent"] = simulated["current_consent_knowledge"] + consent_boost
        simulated["scenario_connectedness"] = simulated["current_connectedness"] + connectedness_boost
        simulated["scenario_climate"] = simulated["school_climate"] + climate_boost
        simulated["scenario_education"] = simulated["health_education_quality"] + education_boost
        simulated["scenario_harassment_support"] = simulated["anti_harassment_support"] + harassment_boost
        simulated["scenario_stigma"] = simulated["current_stigma"] - stigma_reduction

        simulated["scenario_protective_context"] = (
            simulated["scenario_family"]
            + simulated["scenario_recognition"]
            + simulated["scenario_consent"]
            + simulated["scenario_connectedness"]
            + simulated["scenario_climate"]
            + simulated["scenario_education"]
            + simulated["scenario_harassment_support"]
        )

        protective_gain = simulated["scenario_protective_context"] - simulated["protective_context"]

        simulated["scenario_adjustment"] = (
            simulated["adjustment_score"]
            + 1.15 * family_boost
            + 1.05 * recognition_boost
            + 1.00 * consent_boost
            + 0.95 * connectedness_boost
            + 0.70 * climate_boost
            + 0.70 * education_boost
            + 0.65 * harassment_boost
            + 1.40 * stigma_reduction
            - 0.35 * (
                simulated["scenario_stigma"] * simulated["scenario_protective_context"]
                - simulated["current_stigma"] * simulated["protective_context"]
            )
        )

        summary = simulated.groupby(["time", "development_profile"], as_index=False).agg(
            average_adjustment=("scenario_adjustment", "mean"),
            average_protective_context=("scenario_protective_context", "mean"),
            average_stigma=("scenario_stigma", "mean"),
            protective_gain=("scenario_protective_context", lambda x: protective_gain.loc[x.index].mean()),
            adolescents=("id", "nunique"),
        )
        summary["scenario"] = name
        scenarios.append(summary)

    result = pd.concat(scenarios, ignore_index=True)
    result.to_csv(OUTPUTS_DIR / "python_gender_sexual_development_scenario_comparison.csv", index=False)

    overall = result.groupby(["time", "scenario"], as_index=False).agg(
        average_adjustment=("average_adjustment", "mean")
    )

    plt.figure(figsize=(9, 5.5))
    for scenario, group in overall.groupby("scenario"):
        plt.plot(group["time"], group["average_adjustment"], marker="o", label=scenario)
    plt.xlabel("Time")
    plt.ylabel("Average scenario adjustment")
    plt.title("Synthetic Gender/Sexual Development Protective Context Scenarios")
    plt.legend(fontsize=8)
    plt.tight_layout()
    plt.savefig(OUTPUTS_DIR / "python_gender_sexual_development_scenario_comparison.png", dpi=160)
    plt.close()

    print("Wrote outputs/python_gender_sexual_development_scenario_comparison.csv")
    print("Wrote outputs/python_gender_sexual_development_scenario_comparison.png")


if __name__ == "__main__":
    main()
