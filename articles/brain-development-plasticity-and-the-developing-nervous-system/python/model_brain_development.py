#!/usr/bin/env python3
from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd
import statsmodels.formula.api as smf

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "brain_development_panel.csv"
OUT = ROOT / "outputs"
OUT.mkdir(exist_ok=True)

def main():
    panel = pd.read_csv(DATA).sort_values(["child_id", "time"])
    panel["lag_neural_state"] = panel.groupby("child_id")["neural_state"].shift(1)
    panel["lag_outcome"] = panel.groupby("child_id")["developmental_outcome"].shift(1)
    model_data = panel.dropna(subset=["lag_neural_state", "lag_outcome"]).copy()

    model = smf.ols(
        """
        developmental_outcome ~ lag_outcome + neural_state + lag_neural_state +
        time + I(time ** 2) + current_family_support + current_learning +
        current_sleep + current_sensory_support + school_support +
        neighborhood_safety + health_service_access + environmental_risk +
        acute_stress + chronic_stress + developmental_support_context
        """,
        data=model_data,
    ).fit(cov_type="HC3")

    with open(OUT / "python_brain_model_summary.txt", "w", encoding="utf-8") as f:
        f.write(model.summary().as_text())

    trajectory = panel.groupby(["time", "chronic_stress"], as_index=False).agg(
        average_developmental_outcome=("developmental_outcome", "mean"),
        average_neural_state=("neural_state", "mean"),
        average_family_support=("current_family_support", "mean"),
        average_learning=("current_learning", "mean"),
        average_sleep=("current_sleep", "mean"),
        average_sensory_support=("current_sensory_support", "mean"),
        average_stress=("acute_stress", "mean"),
        average_support_context=("developmental_support_context", "mean"),
    )
    trajectory["stress_group"] = trajectory["chronic_stress"].map({0: "Lower chronic stress", 1: "Higher chronic stress"})
    trajectory.to_csv(OUT / "python_stress_neurodevelopment_trajectory.csv", index=False)

    plt.figure(figsize=(8, 5))
    for label, group in trajectory.groupby("stress_group"):
        plt.plot(group["time"], group["average_developmental_outcome"], marker="o", label=label)
    plt.xlabel("Time")
    plt.ylabel("Average developmental outcome")
    plt.title("Synthetic Brain Development Under Support and Adversity")
    plt.legend()
    plt.tight_layout()
    plt.savefig(OUT / "python_stress_neurodevelopment_trajectory.png", dpi=160)
    plt.close()

    context = panel.groupby("time", as_index=False).agg(
        average_family_support=("current_family_support", "mean"),
        average_learning=("current_learning", "mean"),
        average_sleep=("current_sleep", "mean"),
        average_sensory_support=("current_sensory_support", "mean"),
        average_stress=("acute_stress", "mean"),
        average_support_context=("developmental_support_context", "mean"),
        average_neural_state=("neural_state", "mean"),
        average_outcome=("developmental_outcome", "mean"),
    )
    context.to_csv(OUT / "python_neurodevelopment_context_trajectory.csv", index=False)

    plt.figure(figsize=(8, 5))
    for col, label in [
        ("average_family_support", "family support"),
        ("average_learning", "learning opportunity"),
        ("average_sleep", "sleep quality"),
        ("average_sensory_support", "sensory support"),
        ("average_stress", "acute stress"),
        ("average_support_context", "support context"),
    ]:
        plt.plot(context["time"], context[col], marker="o", label=label)
    plt.xlabel("Time")
    plt.ylabel("Average index")
    plt.title("Synthetic Neurodevelopmental Support Context Across Time")
    plt.legend(fontsize=8)
    plt.tight_layout()
    plt.savefig(OUT / "python_neurodevelopment_context_trajectory.png", dpi=160)
    plt.close()

    panel.groupby("neurodevelopment_profile", as_index=False).agg(
        children=("child_id", "nunique"),
        average_neural_state=("neural_state", "mean"),
        average_developmental_outcome=("developmental_outcome", "mean"),
        average_developmental_support_context=("developmental_support_context", "mean"),
        average_stress=("acute_stress", "mean"),
        chronic_stress_rate=("chronic_stress", "mean"),
    ).to_csv(OUT / "python_neurodevelopment_profiles.csv", index=False)

    panel.groupby("context_id", as_index=False).agg(
        school_support=("school_support", "mean"),
        neighborhood_safety=("neighborhood_safety", "mean"),
        health_service_access=("health_service_access", "mean"),
        environmental_risk=("environmental_risk", "mean"),
        average_neural_state=("neural_state", "mean"),
        average_developmental_outcome=("developmental_outcome", "mean"),
        average_stress=("acute_stress", "mean"),
        average_support_context=("developmental_support_context", "mean"),
        children=("child_id", "nunique"),
    ).to_csv(OUT / "python_neurodevelopment_context_summary.csv", index=False)

    print("Wrote Python brain development outputs.")

if __name__ == "__main__":
    main()
