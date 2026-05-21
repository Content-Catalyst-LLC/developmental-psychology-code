#!/usr/bin/env python3
"""Model synthetic aging, adaptation, and development in later life."""

from __future__ import annotations

from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd
import statsmodels.formula.api as smf

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "aging_adaptation_later_life_panel.csv"
OUTPUTS_DIR = ROOT / "outputs"
OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)


def main() -> None:
    if not DATA_PATH.exists():
        raise FileNotFoundError("Run python/generate_aging_adaptation_panel.py first.")

    panel = pd.read_csv(DATA_PATH).sort_values(["id", "time"]).reset_index(drop=True)
    panel["lag_score"] = panel.groupby("id")["adjustment_score"].shift(1)
    model_data = panel.dropna(subset=["lag_score"]).copy()

    adjustment_model = smf.ols(
        """
        adjustment_score ~ lag_score + time + functional_fit +
        current_support + current_adaptation + current_meaning +
        current_health + dignity_support + service_access
        """,
        data=model_data,
    ).fit(cov_type="HC3")

    fit_model = smf.ols(
        """
        functional_fit ~ time + current_function + environmental_accessibility +
        current_function:environmental_accessibility + current_support +
        dignity_support + service_access
        """,
        data=panel,
    ).fit(cov_type="HC3")

    with open(OUTPUTS_DIR / "python_aging_adaptation_model_summary.txt", "w", encoding="utf-8") as f:
        f.write("DYNAMIC LATER-LIFE ADJUSTMENT MODEL\n")
        f.write("=" * 80 + "\n")
        f.write(adjustment_model.summary().as_text())
        f.write("\n\nFUNCTIONAL FIT MODEL\n")
        f.write("=" * 80 + "\n")
        f.write(fit_model.summary().as_text())

    panel["health_group"] = pd.qcut(
        panel["current_health"],
        3,
        labels=["Lower burden", "Moderate burden", "Higher burden"],
    )

    trajectory = panel.groupby(["time", "health_group"], as_index=False, observed=True).agg(
        average_adjustment=("adjustment_score", "mean"),
        average_functional_fit=("functional_fit", "mean"),
        standard_error=("adjustment_score", lambda x: x.std() / (len(x) ** 0.5)),
    )
    trajectory["lower"] = trajectory["average_adjustment"] - 1.96 * trajectory["standard_error"]
    trajectory["upper"] = trajectory["average_adjustment"] + 1.96 * trajectory["standard_error"]
    trajectory.to_csv(OUTPUTS_DIR / "python_adjustment_trajectory.csv", index=False)

    plt.figure(figsize=(8, 5))
    for group_name, group in trajectory.groupby("health_group", observed=True):
        plt.plot(group["time"], group["average_adjustment"], marker="o", label=str(group_name))
    plt.xlabel("Time")
    plt.ylabel("Average adjustment score")
    plt.title("Synthetic Aging, Adaptation, and Later-Life Development")
    plt.legend()
    plt.tight_layout()
    plt.savefig(OUTPUTS_DIR / "python_adjustment_trajectory.png", dpi=160)
    plt.close()

    fit_trajectory = panel.groupby("time", as_index=False).agg(
        average_functional_fit=("functional_fit", "mean"),
        average_function=("current_function", "mean"),
        average_support=("current_support", "mean"),
        average_health=("current_health", "mean"),
        average_adaptation=("current_adaptation", "mean"),
    )
    fit_trajectory.to_csv(OUTPUTS_DIR / "python_functional_fit_trajectory.csv", index=False)

    plt.figure(figsize=(8, 5))
    plt.plot(fit_trajectory["time"], fit_trajectory["average_functional_fit"], marker="o", label="functional fit")
    plt.plot(fit_trajectory["time"], fit_trajectory["average_support"], marker="o", label="support")
    plt.plot(fit_trajectory["time"], fit_trajectory["average_health"], marker="o", label="health burden")
    plt.xlabel("Time")
    plt.ylabel("Average index")
    plt.title("Synthetic Functional Fit, Support, and Health Burden")
    plt.legend()
    plt.tight_layout()
    plt.savefig(OUTPUTS_DIR / "python_functional_fit_trajectory.png", dpi=160)
    plt.close()

    profile_summary = panel.groupby("adaptation_profile", as_index=False).agg(
        people=("id", "nunique"),
        average_adjustment=("adjustment_score", "mean"),
        average_functional_fit=("functional_fit", "mean"),
        average_support=("current_support", "mean"),
        average_health=("current_health", "mean"),
        average_adaptation=("current_adaptation", "mean"),
        average_meaning=("current_meaning", "mean"),
    )
    profile_summary.to_csv(OUTPUTS_DIR / "python_aging_adaptation_profiles.csv", index=False)

    print("Wrote Python aging adaptation model outputs.")


if __name__ == "__main__":
    main()
