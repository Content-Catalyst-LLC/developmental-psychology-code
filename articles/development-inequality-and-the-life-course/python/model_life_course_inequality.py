#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd
import statsmodels.formula.api as smf

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "life_course_inequality_panel.csv"
OUTPUTS_DIR = ROOT / "outputs"
OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)

def main() -> None:
    if not DATA_PATH.exists():
        raise FileNotFoundError("Run python/generate_life_course_inequality.py first.")

    panel = pd.read_csv(DATA_PATH).sort_values(["person_id", "time"]).reset_index(drop=True)
    panel["lag_score"] = panel.groupby("person_id")["development_score"].shift(1)
    model_data = panel.dropna(subset=["lag_score"]).copy()

    model = smf.ols(
        """
        development_score ~ lag_score + time + current_resources +
        current_burden + current_support + transition_support +
        health_status + community_opportunity + institutional_support +
        environmental_safety + early_timing_weight + person_resilience
        """,
        data=model_data,
    ).fit(cov_type="HC3")

    profile_model = smf.ols(
        """
        development_score ~ time + C(inequality_profile) +
        current_support + health_status + community_opportunity + institutional_support
        """,
        data=panel,
    ).fit(cov_type="HC3")

    with open(OUTPUTS_DIR / "python_life_course_model_summary.txt", "w", encoding="utf-8") as f:
        f.write("DYNAMIC LIFE-COURSE INEQUALITY MODEL\\n")
        f.write("=" * 80 + "\\n")
        f.write(model.summary().as_text())
        f.write("\\n\\nINEQUALITY PROFILE MODEL\\n")
        f.write("=" * 80 + "\\n")
        f.write(profile_model.summary().as_text())

    trajectory = panel.groupby("time", as_index=False).agg(
        average_development=("development_score", "mean"),
        standard_error=("development_score", lambda x: x.std() / (len(x) ** 0.5)),
        average_resources=("current_resources", "mean"),
        average_burden=("current_burden", "mean"),
        average_support=("current_support", "mean"),
    )
    trajectory["lower"] = trajectory["average_development"] - 1.96 * trajectory["standard_error"]
    trajectory["upper"] = trajectory["average_development"] + 1.96 * trajectory["standard_error"]
    trajectory.to_csv(OUTPUTS_DIR / "python_life_course_trajectory.csv", index=False)

    plt.figure(figsize=(8, 5))
    plt.plot(trajectory["time"], trajectory["average_development"], linewidth=2)
    plt.fill_between(trajectory["time"], trajectory["lower"], trajectory["upper"], alpha=0.2)
    plt.xlabel("Time")
    plt.ylabel("Average development score")
    plt.title("Synthetic Development, Inequality, and the Life Course")
    plt.tight_layout()
    plt.savefig(OUTPUTS_DIR / "python_life_course_trajectory.png", dpi=160)
    plt.close()

    person_summary = panel.groupby("person_id", as_index=False).agg(
        inequality_profile=("inequality_profile", "first"),
        average_resources=("current_resources", "mean"),
        average_burden=("current_burden", "mean"),
        final_score=("development_score", "last"),
    )
    profile_summary = person_summary.groupby("inequality_profile", as_index=False).agg(
        people=("person_id", "count"),
        average_final_score=("final_score", "mean"),
        average_resources=("average_resources", "mean"),
        average_burden=("average_burden", "mean"),
    )
    profile_summary.to_csv(OUTPUTS_DIR / "python_inequality_profiles.csv", index=False)

    profile_trajectory = panel.groupby(["inequality_profile", "time"], as_index=False).agg(
        average_development=("development_score", "mean")
    )
    profile_trajectory.to_csv(OUTPUTS_DIR / "python_profile_trajectories.csv", index=False)

    plt.figure(figsize=(9, 5.5))
    for profile, group in profile_trajectory.groupby("inequality_profile"):
        plt.plot(group["time"], group["average_development"], marker="o", label=profile)
    plt.xlabel("Time")
    plt.ylabel("Average development score")
    plt.title("Synthetic Developmental Trajectories by Inequality Profile")
    plt.legend()
    plt.tight_layout()
    plt.savefig(OUTPUTS_DIR / "python_profile_trajectories.png", dpi=160)
    plt.close()

    print("Wrote Python model outputs.")

if __name__ == "__main__":
    main()
