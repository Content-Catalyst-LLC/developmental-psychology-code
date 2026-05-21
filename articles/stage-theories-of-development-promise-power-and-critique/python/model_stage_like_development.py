#!/usr/bin/env python3
"""Model synthetic continuous and stage-like developmental trajectories."""

from __future__ import annotations

from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd
import statsmodels.formula.api as smf

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "stage_theory_development_panel.csv"
OUTPUTS_DIR = ROOT / "outputs"
OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)


def main() -> None:
    if not DATA_PATH.exists():
        raise FileNotFoundError("Run python/generate_stage_theory_panel.py first.")

    panel = pd.read_csv(DATA_PATH).sort_values(["child_id", "time"]).reset_index(drop=True)
    panel["lag_score"] = panel.groupby("child_id")["development_score"].shift(1)
    model_data = panel.dropna(subset=["lag_score"]).copy()

    threshold_model = smf.ols(
        """
        development_score ~ lag_score + time + current_support +
        school_support + resource_stability + chronic_stress +
        threshold_on + logistic_transition + stage_pattern +
        transition_readiness + threshold_on:stage_pattern +
        logistic_transition:stage_pattern +
        threshold_on:stage_pattern:transition_readiness
        """,
        data=model_data,
    ).fit(cov_type="HC3")

    profile_model = smf.ols(
        """
        development_score ~ time + transition_readiness + chronic_stress +
        C(stage_profile) + logistic_transition + stage_pattern
        """,
        data=panel,
    ).fit(cov_type="HC3")

    with open(OUTPUTS_DIR / "python_stage_model_summary.txt", "w", encoding="utf-8") as f:
        f.write("DYNAMIC STAGE-LIKE DEVELOPMENT MODEL\n")
        f.write("=" * 80 + "\n")
        f.write(threshold_model.summary().as_text())
        f.write("\n\nPROFILE MODEL\n")
        f.write("=" * 80 + "\n")
        f.write(profile_model.summary().as_text())

    trajectory = panel.groupby(["time", "stage_pattern"], as_index=False).agg(
        average_score=("development_score", "mean"),
        average_readiness=("transition_readiness", "mean"),
        average_support=("current_support", "mean"),
        standard_error=("development_score", lambda x: x.std() / (len(x) ** 0.5)),
    )
    trajectory["pattern_label"] = trajectory["stage_pattern"].map({
        0: "Mostly continuous growth",
        1: "Stage-like reorganization",
    })
    trajectory["lower"] = trajectory["average_score"] - 1.96 * trajectory["standard_error"]
    trajectory["upper"] = trajectory["average_score"] + 1.96 * trajectory["standard_error"]
    trajectory.to_csv(OUTPUTS_DIR / "python_stage_trajectory.csv", index=False)

    plt.figure(figsize=(8, 5))
    for group_name, group in trajectory.groupby("pattern_label"):
        plt.plot(group["time"], group["average_score"], marker="o", label=str(group_name))
    plt.xlabel("Time")
    plt.ylabel("Average development score")
    plt.title("Synthetic Continuous and Stage-Like Developmental Patterns")
    plt.legend()
    plt.tight_layout()
    plt.savefig(OUTPUTS_DIR / "python_stage_trajectory.png", dpi=160)
    plt.close()

    threshold_summary = panel.groupby(["threshold_time", "stage_pattern"], as_index=False).agg(
        average_score=("development_score", "mean"),
        average_readiness=("transition_readiness", "mean"),
        average_support=("current_support", "mean"),
        average_stress=("chronic_stress", "mean"),
    )
    threshold_summary["pattern_label"] = threshold_summary["stage_pattern"].map({
        0: "Mostly continuous growth",
        1: "Stage-like reorganization",
    })
    threshold_summary.to_csv(OUTPUTS_DIR / "python_threshold_summary.csv", index=False)

    plt.figure(figsize=(8, 5))
    for group_name, group in threshold_summary.groupby("pattern_label"):
        plt.plot(group["threshold_time"], group["average_score"], marker="o", label=str(group_name))
    plt.xlabel("Threshold time")
    plt.ylabel("Average development score")
    plt.title("Synthetic Threshold Timing and Developmental Outcome")
    plt.legend()
    plt.tight_layout()
    plt.savefig(OUTPUTS_DIR / "python_threshold_summary.png", dpi=160)
    plt.close()

    profile_summary = panel.groupby("stage_profile", as_index=False).agg(
        individuals=("child_id", "nunique"),
        average_score=("development_score", "mean"),
        average_readiness=("transition_readiness", "mean"),
        average_support=("current_support", "mean"),
        average_stress=("chronic_stress", "mean"),
        average_threshold=("threshold_time", "mean"),
    )
    profile_summary.to_csv(OUTPUTS_DIR / "python_stage_profiles.csv", index=False)

    print("Wrote Python stage-like development model outputs.")


if __name__ == "__main__":
    main()
