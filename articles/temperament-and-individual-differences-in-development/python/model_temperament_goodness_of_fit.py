#!/usr/bin/env python3
"""Model synthetic temperament, stress, support, and goodness of fit."""

from __future__ import annotations

from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd
import statsmodels.formula.api as smf

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "temperament_individual_differences_panel.csv"
OUTPUTS_DIR = ROOT / "outputs"
OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)


def main() -> None:
    if not DATA_PATH.exists():
        raise FileNotFoundError("Run python/generate_temperament_panel.py first.")

    panel = pd.read_csv(DATA_PATH).sort_values(["child_id", "time"]).reset_index(drop=True)
    panel["lag_score"] = panel.groupby("child_id")["adjustment_score"].shift(1)
    model_data = panel.dropna(subset=["lag_score"]).copy()

    temperament_model = smf.ols(
        """
        adjustment_score ~ lag_score + time + temperament_reactivity +
        inhibition + activity_level + current_support + goodness_of_fit +
        acute_stress + chronic_stress + teacher_responsiveness +
        temperament_reactivity:current_support +
        temperament_reactivity:goodness_of_fit +
        temperament_reactivity:acute_stress
        """,
        data=model_data,
    ).fit(cov_type="HC3")

    fit_model = smf.ols(
        """
        goodness_of_fit ~ current_school_fit + teacher_responsiveness +
        movement_flexibility + current_accommodation + classroom_structure +
        temperament_reactivity + inhibition + activity_level +
        current_support + acute_stress
        """,
        data=panel,
    ).fit(cov_type="HC3")

    with open(OUTPUTS_DIR / "python_temperament_model_summary.txt", "w", encoding="utf-8") as f:
        f.write("DYNAMIC TEMPERAMENT AND GOODNESS-OF-FIT MODEL\n")
        f.write("=" * 80 + "\n")
        f.write(temperament_model.summary().as_text())
        f.write("\n\nGOODNESS-OF-FIT MODEL\n")
        f.write("=" * 80 + "\n")
        f.write(fit_model.summary().as_text())

    panel["reactivity_group"] = pd.qcut(
        panel["temperament_reactivity"],
        3,
        labels=["Lower reactivity", "Moderate reactivity", "Higher reactivity"],
    )

    trajectory = panel.groupby(["time", "reactivity_group"], as_index=False, observed=True).agg(
        average_adjustment=("adjustment_score", "mean"),
        average_fit=("goodness_of_fit", "mean"),
        standard_error=("adjustment_score", lambda x: x.std() / (len(x) ** 0.5)),
    )
    trajectory["lower"] = trajectory["average_adjustment"] - 1.96 * trajectory["standard_error"]
    trajectory["upper"] = trajectory["average_adjustment"] + 1.96 * trajectory["standard_error"]
    trajectory.to_csv(OUTPUTS_DIR / "python_temperament_trajectory.csv", index=False)

    plt.figure(figsize=(8, 5))
    for group_name, group in trajectory.groupby("reactivity_group", observed=True):
        plt.plot(group["time"], group["average_adjustment"], marker="o", label=str(group_name))
    plt.xlabel("Time")
    plt.ylabel("Average adjustment score")
    plt.title("Synthetic Temperament and Developmental Adjustment")
    plt.legend()
    plt.tight_layout()
    plt.savefig(OUTPUTS_DIR / "python_temperament_trajectory.png", dpi=160)
    plt.close()

    fit_trajectory = panel.groupby("time", as_index=False).agg(
        average_fit=("goodness_of_fit", "mean"),
        average_support=("current_support", "mean"),
        average_stress=("acute_stress", "mean"),
        average_accommodation=("current_accommodation", "mean"),
        average_adjustment=("adjustment_score", "mean"),
    )
    fit_trajectory.to_csv(OUTPUTS_DIR / "python_goodness_of_fit_trajectory.csv", index=False)

    plt.figure(figsize=(8, 5))
    plt.plot(fit_trajectory["time"], fit_trajectory["average_fit"], marker="o", label="goodness of fit")
    plt.plot(fit_trajectory["time"], fit_trajectory["average_support"], marker="o", label="support")
    plt.plot(fit_trajectory["time"], fit_trajectory["average_stress"], marker="o", label="stress")
    plt.plot(fit_trajectory["time"], fit_trajectory["average_accommodation"], marker="o", label="accommodation")
    plt.xlabel("Time")
    plt.ylabel("Average index")
    plt.title("Synthetic Goodness of Fit, Support, Stress, and Accommodation")
    plt.legend()
    plt.tight_layout()
    plt.savefig(OUTPUTS_DIR / "python_goodness_of_fit_trajectory.png", dpi=160)
    plt.close()

    profile_summary = panel.groupby("temperament_profile", as_index=False).agg(
        children=("child_id", "nunique"),
        average_adjustment=("adjustment_score", "mean"),
        average_fit=("goodness_of_fit", "mean"),
        average_support=("current_support", "mean"),
        average_stress=("acute_stress", "mean"),
        average_reactivity=("temperament_reactivity", "mean"),
        average_accommodation=("current_accommodation", "mean"),
    )
    profile_summary.to_csv(OUTPUTS_DIR / "python_temperament_profiles.csv", index=False)

    print("Wrote Python temperament and goodness-of-fit model outputs.")


if __name__ == "__main__":
    main()
