#!/usr/bin/env python3
"""Model synthetic trauma, adversity, and life-course adaptation trajectories."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import statsmodels.formula.api as smf


ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "trauma_life_course_panel.csv"
OUTPUTS_DIR = ROOT / "outputs"
OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)


def main() -> None:
    if not DATA_PATH.exists():
        raise FileNotFoundError(
            f"Missing {DATA_PATH}. Run python/generate_trauma_life_course.py first."
        )

    panel = pd.read_csv(DATA_PATH)
    panel = panel.sort_values(["child_id", "time"]).reset_index(drop=True)
    panel["lag_score"] = panel.groupby("child_id")["adaptation_score"].shift(1)

    regression_data = panel.dropna(subset=["lag_score"]).copy()

    dynamic_model = smf.ols(
        formula="""
        adaptation_score ~ lag_score + time + cumulative_adversity +
        current_adversity + early_timing_weight + current_support +
        current_stability + transition_support + community_buffer +
        institutional_safety + service_access + current_health +
        child_resilience + current_support:current_stability
        """,
        data=regression_data,
    ).fit(cov_type="HC3")

    profile_model = smf.ols(
        formula="""
        adaptation_score ~ time + C(adversity_support_profile) +
        current_support + current_stability + community_buffer +
        institutional_safety + service_access
        """,
        data=panel,
    ).fit(cov_type="HC3")

    with open(OUTPUTS_DIR / "python_trauma_model_summary.txt", "w", encoding="utf-8") as f:
        f.write("DYNAMIC TRAUMA / ADVERSITY LIFE-COURSE MODEL\n")
        f.write("=" * 80 + "\n")
        f.write(dynamic_model.summary().as_text())
        f.write("\n\nADVERSITY-SUPPORT PROFILE MODEL\n")
        f.write("=" * 80 + "\n")
        f.write(profile_model.summary().as_text())

    trajectory = panel.groupby("time", as_index=False).agg(
        average_adaptation=("adaptation_score", "mean"),
        standard_error=("adaptation_score", lambda x: x.std() / (len(x) ** 0.5)),
        average_adversity=("current_adversity", "mean"),
        average_support=("current_support", "mean"),
        average_stability=("current_stability", "mean"),
        average_cumulative_adversity=("cumulative_adversity", "mean"),
    )
    trajectory["lower"] = trajectory["average_adaptation"] - 1.96 * trajectory["standard_error"]
    trajectory["upper"] = trajectory["average_adaptation"] + 1.96 * trajectory["standard_error"]
    trajectory.to_csv(OUTPUTS_DIR / "python_adaptation_trajectory.csv", index=False)

    plt.figure(figsize=(8, 5))
    plt.plot(trajectory["time"], trajectory["average_adaptation"], linewidth=2)
    plt.fill_between(trajectory["time"], trajectory["lower"], trajectory["upper"], alpha=0.2)
    plt.xlabel("Time")
    plt.ylabel("Average adaptation score")
    plt.title("Synthetic Trauma, Adversity, and the Life Course")
    plt.tight_layout()
    plt.savefig(OUTPUTS_DIR / "python_adaptation_trajectory.png", dpi=160)
    plt.close()

    child_summary = panel.groupby("child_id", as_index=False).agg(
        adversity_support_profile=("adversity_support_profile", "first"),
        average_adversity=("current_adversity", "mean"),
        average_support=("current_support", "mean"),
        average_stability=("current_stability", "mean"),
        final_score=("adaptation_score", "last"),
    )

    profile_summary = child_summary.groupby("adversity_support_profile", as_index=False).agg(
        children=("child_id", "count"),
        average_final_score=("final_score", "mean"),
        average_adversity=("average_adversity", "mean"),
        average_support=("average_support", "mean"),
        average_stability=("average_stability", "mean"),
    )
    profile_summary.to_csv(OUTPUTS_DIR / "python_adversity_support_profiles.csv", index=False)

    profile_trajectory = panel.groupby(
        ["adversity_support_profile", "time"],
        as_index=False,
    ).agg(average_adaptation=("adaptation_score", "mean"))

    profile_trajectory.to_csv(OUTPUTS_DIR / "python_profile_trajectories.csv", index=False)

    plt.figure(figsize=(9, 5.5))
    for profile, group in profile_trajectory.groupby("adversity_support_profile"):
        plt.plot(group["time"], group["average_adaptation"], marker="o", label=profile)
    plt.xlabel("Time")
    plt.ylabel("Average adaptation score")
    plt.title("Synthetic Adaptation Trajectories by Adversity-Support Profile")
    plt.legend()
    plt.tight_layout()
    plt.savefig(OUTPUTS_DIR / "python_profile_trajectories.png", dpi=160)
    plt.close()

    print("Wrote outputs/python_trauma_model_summary.txt")
    print("Wrote outputs/python_adaptation_trajectory.csv")
    print("Wrote outputs/python_adaptation_trajectory.png")
    print("Wrote outputs/python_adversity_support_profiles.csv")
    print("Wrote outputs/python_profile_trajectories.csv")
    print("Wrote outputs/python_profile_trajectories.png")


if __name__ == "__main__":
    main()
