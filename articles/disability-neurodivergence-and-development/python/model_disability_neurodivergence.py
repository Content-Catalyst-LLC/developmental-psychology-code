#!/usr/bin/env python3
"""Model synthetic disability, neurodivergence, access, and participation."""

from __future__ import annotations

from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd
import statsmodels.formula.api as smf

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "disability_neurodivergence_panel.csv"
OUTPUTS_DIR = ROOT / "outputs"
OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)


def main() -> None:
    if not DATA_PATH.exists():
        raise FileNotFoundError("Run python/generate_disability_neurodivergence_panel.py first.")

    panel = pd.read_csv(DATA_PATH).sort_values(["child_id", "time"]).reset_index(drop=True)
    panel["lag_score"] = panel.groupby("child_id")["development_score"].shift(1)
    model_data = panel.dropna(subset=["lag_score"]).copy()

    development_model = smf.ols(
        """
        development_score ~ lag_score + time + neuro_profile +
        current_support + current_access + current_barrier +
        current_communication + participation_score + current_advocacy +
        inclusion_climate + service_access + sensory_flexibility +
        current_support:current_access + current_barrier:neuro_profile
        """,
        data=model_data,
    ).fit(cov_type="HC3")

    participation_model = smf.ols(
        """
        participation_score ~ time + neuro_profile +
        current_support + current_access + current_barrier +
        current_communication + current_advocacy +
        inclusion_climate + service_access + sensory_flexibility
        """,
        data=panel,
    ).fit(cov_type="HC3")

    with open(OUTPUTS_DIR / "python_accessibility_model_summary.txt", "w", encoding="utf-8") as f:
        f.write("DYNAMIC DEVELOPMENT MODEL\n")
        f.write("=" * 80 + "\n")
        f.write(development_model.summary().as_text())
        f.write("\n\nPARTICIPATION MODEL\n")
        f.write("=" * 80 + "\n")
        f.write(participation_model.summary().as_text())

    trajectory = panel.groupby("time", as_index=False).agg(
        average_development=("development_score", "mean"),
        average_participation=("participation_score", "mean"),
        standard_error=("development_score", lambda x: x.std() / (len(x) ** 0.5)),
    )
    trajectory["lower"] = trajectory["average_development"] - 1.96 * trajectory["standard_error"]
    trajectory["upper"] = trajectory["average_development"] + 1.96 * trajectory["standard_error"]
    trajectory.to_csv(OUTPUTS_DIR / "python_development_trajectory.csv", index=False)

    plt.figure(figsize=(8, 5))
    plt.plot(trajectory["time"], trajectory["average_development"], linewidth=2)
    plt.fill_between(trajectory["time"], trajectory["lower"], trajectory["upper"], alpha=0.2)
    plt.xlabel("Time")
    plt.ylabel("Average development score")
    plt.title("Synthetic Disability, Neurodivergence, and Development")
    plt.tight_layout()
    plt.savefig(OUTPUTS_DIR / "python_development_trajectory.png", dpi=160)
    plt.close()

    plt.figure(figsize=(8, 5))
    plt.plot(trajectory["time"], trajectory["average_participation"], marker="o")
    plt.xlabel("Time")
    plt.ylabel("Average participation score")
    plt.title("Synthetic Participation Trajectory")
    plt.tight_layout()
    plt.savefig(OUTPUTS_DIR / "python_participation_trajectory.png", dpi=160)
    plt.close()

    profile_summary = panel.groupby("access_condition", as_index=False).agg(
        children=("child_id", "nunique"),
        average_development=("development_score", "mean"),
        average_participation=("participation_score", "mean"),
        average_access=("current_access", "mean"),
        average_barrier=("current_barrier", "mean"),
        average_support=("current_support", "mean"),
    )
    profile_summary.to_csv(OUTPUTS_DIR / "python_access_profiles.csv", index=False)

    print("Wrote Python accessibility model outputs.")


if __name__ == "__main__":
    main()
