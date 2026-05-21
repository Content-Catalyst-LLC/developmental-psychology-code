#!/usr/bin/env python3
"""Model synthetic continuous, nonlinear, and threshold-sensitive developmental trajectories."""

from __future__ import annotations

from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd
import statsmodels.formula.api as smf

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "continuity_discontinuity_panel.csv"
OUTPUTS_DIR = ROOT / "outputs"
OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)


def main() -> None:
    if not DATA_PATH.exists():
        raise FileNotFoundError("Run python/generate_continuity_discontinuity_panel.py first.")

    panel = pd.read_csv(DATA_PATH).sort_values(["person_id", "time"]).reset_index(drop=True)
    panel["time_squared"] = panel["time"] ** 2
    panel["lag_score"] = panel.groupby("person_id")["development_score"].shift(1)
    model_data = panel.dropna(subset=["lag_score"]).copy()

    continuity_model = smf.ols(
        """
        development_score ~ lag_score + time + time_squared + current_support +
        school_support + resource_stability + chronic_stress +
        institutional_rupture + intervention_exposure +
        threshold_on + logistic_transition + threshold_sensitive +
        threshold_on:threshold_sensitive +
        logistic_transition:threshold_sensitive +
        threshold_on:threshold_sensitive:transition_readiness
        """,
        data=model_data,
    ).fit(cov_type="HC3")

    profile_model = smf.ols(
        """
        development_score ~ time + time_squared + transition_readiness +
        chronic_stress + institutional_rupture + intervention_exposure +
        C(change_profile) + logistic_transition + threshold_sensitive
        """,
        data=panel,
    ).fit(cov_type="HC3")

    with open(OUTPUTS_DIR / "python_continuity_discontinuity_model_summary.txt", "w", encoding="utf-8") as f:
        f.write("DYNAMIC CONTINUITY-DISCONTINUITY MODEL\n")
        f.write("=" * 80 + "\n")
        f.write(continuity_model.summary().as_text())
        f.write("\n\nPROFILE MODEL\n")
        f.write("=" * 80 + "\n")
        f.write(profile_model.summary().as_text())

    trajectory = panel.groupby(["time", "threshold_sensitive"], as_index=False).agg(
        average_score=("development_score", "mean"),
        average_readiness=("transition_readiness", "mean"),
        average_support=("current_support", "mean"),
        average_stress=("chronic_stress", "mean"),
        average_rupture=("institutional_rupture", "mean"),
        average_intervention=("intervention_exposure", "mean"),
        standard_error=("development_score", lambda x: x.std() / (len(x) ** 0.5)),
    )
    trajectory["group_label"] = trajectory["threshold_sensitive"].map({
        0: "Mostly continuous growth",
        1: "Threshold-sensitive development",
    })
    trajectory["lower"] = trajectory["average_score"] - 1.96 * trajectory["standard_error"]
    trajectory["upper"] = trajectory["average_score"] + 1.96 * trajectory["standard_error"]
    trajectory.to_csv(OUTPUTS_DIR / "python_developmental_trajectory.csv", index=False)

    plt.figure(figsize=(8, 5))
    for group_name, group in trajectory.groupby("group_label"):
        plt.plot(group["time"], group["average_score"], marker="o", label=str(group_name))
    plt.xlabel("Time")
    plt.ylabel("Average development score")
    plt.title("Synthetic Continuous and Threshold-Sensitive Development")
    plt.legend()
    plt.tight_layout()
    plt.savefig(OUTPUTS_DIR / "python_developmental_trajectory.png", dpi=160)
    plt.close()

    threshold_summary = panel.groupby(["threshold_time", "threshold_sensitive"], as_index=False).agg(
        average_score=("development_score", "mean"),
        average_readiness=("transition_readiness", "mean"),
        average_support=("current_support", "mean"),
        average_stress=("chronic_stress", "mean"),
        average_rupture=("institutional_rupture", "mean"),
        average_intervention=("intervention_exposure", "mean"),
    )
    threshold_summary["group_label"] = threshold_summary["threshold_sensitive"].map({
        0: "Mostly continuous growth",
        1: "Threshold-sensitive development",
    })
    threshold_summary.to_csv(OUTPUTS_DIR / "python_threshold_summary.csv", index=False)

    plt.figure(figsize=(8, 5))
    for group_name, group in threshold_summary.groupby("group_label"):
        plt.plot(group["threshold_time"], group["average_score"], marker="o", label=str(group_name))
    plt.xlabel("Threshold time")
    plt.ylabel("Average development score")
    plt.title("Synthetic Threshold Timing and Developmental Outcome")
    plt.legend()
    plt.tight_layout()
    plt.savefig(OUTPUTS_DIR / "python_threshold_summary.png", dpi=160)
    plt.close()

    profile_summary = panel.groupby("change_profile", as_index=False).agg(
        individuals=("person_id", "nunique"),
        average_score=("development_score", "mean"),
        average_readiness=("transition_readiness", "mean"),
        average_support=("current_support", "mean"),
        average_stress=("chronic_stress", "mean"),
        average_rupture=("institutional_rupture", "mean"),
        average_intervention=("intervention_exposure", "mean"),
        average_threshold=("threshold_time", "mean"),
    )
    profile_summary.to_csv(OUTPUTS_DIR / "python_developmental_profiles.csv", index=False)

    print("Wrote Python continuity/discontinuity model outputs.")


if __name__ == "__main__":
    main()
