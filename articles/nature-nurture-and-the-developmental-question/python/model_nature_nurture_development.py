#!/usr/bin/env python3
"""Model synthetic nature-nurture development and differential susceptibility."""

from __future__ import annotations

from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd
import statsmodels.formula.api as smf

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "nature_nurture_development_panel.csv"
OUTPUTS_DIR = ROOT / "outputs"
OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)


def main() -> None:
    if not DATA_PATH.exists():
        raise FileNotFoundError("Run python/generate_nature_nurture_panel.py first.")

    panel = pd.read_csv(DATA_PATH).sort_values(["child_id", "time"]).reset_index(drop=True)
    panel["lag_score"] = panel.groupby("child_id")["development_score"].shift(1)
    model_data = panel.dropna(subset=["lag_score"]).copy()

    dynamic_model = smf.ols(
        """
        development_score ~ lag_score + time + biological_sensitivity +
        caregiver_support + acute_stress + structural_risk + chronic_adversity +
        institutional_support + disability_support + resource_stability +
        intervention + protective_context +
        biological_sensitivity:caregiver_support +
        biological_sensitivity:acute_stress +
        biological_sensitivity:protective_context
        """,
        data=model_data,
    ).fit(cov_type="HC3")

    profile_model = smf.ols(
        """
        development_score ~ time + biological_sensitivity + structural_risk +
        chronic_adversity + protective_context + acute_stress +
        C(sensitivity_profile)
        """,
        data=panel,
    ).fit(cov_type="HC3")

    with open(OUTPUTS_DIR / "python_nature_nurture_model_summary.txt", "w", encoding="utf-8") as f:
        f.write("DYNAMIC NATURE-NURTURE DEVELOPMENT MODEL\n")
        f.write("=" * 80 + "\n")
        f.write(dynamic_model.summary().as_text())
        f.write("\n\nSENSITIVITY PROFILE MODEL\n")
        f.write("=" * 80 + "\n")
        f.write(profile_model.summary().as_text())

    trajectory = panel.groupby(["time", "structural_risk"], as_index=False).agg(
        average_development=("development_score", "mean"),
        average_support=("caregiver_support", "mean"),
        average_stress=("acute_stress", "mean"),
        average_protective_context=("protective_context", "mean"),
        standard_error=("development_score", lambda x: x.std() / (len(x) ** 0.5)),
    )
    trajectory["risk_group"] = trajectory["structural_risk"].map({
        0: "Lower structural risk",
        1: "Higher structural risk",
    })
    trajectory["lower"] = trajectory["average_development"] - 1.96 * trajectory["standard_error"]
    trajectory["upper"] = trajectory["average_development"] + 1.96 * trajectory["standard_error"]
    trajectory.to_csv(OUTPUTS_DIR / "python_structural_risk_trajectory.csv", index=False)

    plt.figure(figsize=(8, 5))
    for group_name, group in trajectory.groupby("risk_group"):
        plt.plot(group["time"], group["average_development"], marker="o", label=str(group_name))
    plt.xlabel("Time")
    plt.ylabel("Average development score")
    plt.title("Synthetic Developmental Trajectories by Structural Risk")
    plt.legend()
    plt.tight_layout()
    plt.savefig(OUTPUTS_DIR / "python_structural_risk_trajectory.png", dpi=160)
    plt.close()

    protective = panel.groupby("time", as_index=False).agg(
        average_caregiver_support=("caregiver_support", "mean"),
        average_acute_stress=("acute_stress", "mean"),
        average_protective_context=("protective_context", "mean"),
        average_intervention=("intervention", "mean"),
        average_development=("development_score", "mean"),
    )
    protective.to_csv(OUTPUTS_DIR / "python_protective_context_trajectory.csv", index=False)

    plt.figure(figsize=(8, 5))
    plt.plot(protective["time"], protective["average_caregiver_support"], marker="o", label="caregiver support")
    plt.plot(protective["time"], protective["average_acute_stress"], marker="o", label="acute stress")
    plt.plot(protective["time"], protective["average_protective_context"], marker="o", label="protective context")
    plt.plot(protective["time"], protective["average_intervention"], marker="o", label="intervention")
    plt.xlabel("Time")
    plt.ylabel("Average index")
    plt.title("Synthetic Nature-Nurture Protective Context Over Time")
    plt.legend(fontsize=8)
    plt.tight_layout()
    plt.savefig(OUTPUTS_DIR / "python_protective_context_trajectory.png", dpi=160)
    plt.close()

    profile_summary = panel.groupby("sensitivity_profile", as_index=False).agg(
        children=("child_id", "nunique"),
        average_development=("development_score", "mean"),
        average_protective_context=("protective_context", "mean"),
        average_stress=("acute_stress", "mean"),
        average_sensitivity=("biological_sensitivity", "mean"),
        average_structural_risk=("structural_risk", "mean"),
        average_chronic_adversity=("chronic_adversity", "mean"),
    )
    profile_summary.to_csv(OUTPUTS_DIR / "python_sensitivity_profiles.csv", index=False)

    school_summary = panel.groupby("school_id", as_index=False).agg(
        institutional_support=("institutional_support", "mean"),
        disability_support=("disability_support", "mean"),
        resource_stability=("resource_stability", "mean"),
        average_development=("development_score", "mean"),
        average_stress=("acute_stress", "mean"),
        average_protective_context=("protective_context", "mean"),
    )
    school_summary.to_csv(OUTPUTS_DIR / "python_school_context_summary.csv", index=False)

    print("Wrote Python nature-nurture model outputs.")


if __name__ == "__main__":
    main()
