#!/usr/bin/env python3
"""Model synthetic parenting, family systems, and development."""

from __future__ import annotations

from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd
import statsmodels.formula.api as smf

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "family_systems_panel.csv"
OUTPUTS_DIR = ROOT / "outputs"
OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)


def main() -> None:
    if not DATA_PATH.exists():
        raise FileNotFoundError("Run python/generate_family_systems_panel.py first.")

    panel = pd.read_csv(DATA_PATH).sort_values(["child_id", "time"]).reset_index(drop=True)
    panel["lag_score"] = panel.groupby("child_id")["development_score"].shift(1)
    model_data = panel.dropna(subset=["lag_score"]).copy()

    development_model = smf.ols(
        """
        development_score ~ lag_score + time + current_parenting +
        current_family + current_stress + household_stability +
        kin_support + economic_security + current_sibling +
        current_regulation + caregiver_support +
        current_parenting:current_family
        """,
        data=model_data,
    ).fit(cov_type="HC3")

    family_support_model = smf.ols(
        """
        family_support_index ~ time + current_parenting + current_family +
        household_stability + kin_support + economic_security +
        current_sibling + current_regulation + caregiver_support -
        current_stress
        """,
        data=panel,
    ).fit(cov_type="HC3")

    with open(OUTPUTS_DIR / "python_family_systems_model_summary.txt", "w", encoding="utf-8") as f:
        f.write("DYNAMIC DEVELOPMENT MODEL\n")
        f.write("=" * 80 + "\n")
        f.write(development_model.summary().as_text())
        f.write("\n\nFAMILY SUPPORT INDEX MODEL\n")
        f.write("=" * 80 + "\n")
        f.write(family_support_model.summary().as_text())

    trajectory = panel.groupby(["time", "caregiver_support"], as_index=False).agg(
        average_development=("development_score", "mean"),
        average_family_support=("family_support_index", "mean"),
        standard_error=("development_score", lambda x: x.std() / (len(x) ** 0.5)),
    )
    trajectory["lower"] = trajectory["average_development"] - 1.96 * trajectory["standard_error"]
    trajectory["upper"] = trajectory["average_development"] + 1.96 * trajectory["standard_error"]
    trajectory["group"] = trajectory["caregiver_support"].map({0: "No added support", 1: "Caregiver support"})
    trajectory.to_csv(OUTPUTS_DIR / "python_development_trajectory.csv", index=False)

    plt.figure(figsize=(8, 5))
    for group_name, group in trajectory.groupby("group"):
        plt.plot(group["time"], group["average_development"], marker="o", label=group_name)
    plt.xlabel("Time")
    plt.ylabel("Average development score")
    plt.title("Synthetic Parenting, Family Systems, and Development")
    plt.legend()
    plt.tight_layout()
    plt.savefig(OUTPUTS_DIR / "python_development_trajectory.png", dpi=160)
    plt.close()

    support_trajectory = panel.groupby("time", as_index=False).agg(
        average_family_support=("family_support_index", "mean"),
        average_parenting=("current_parenting", "mean"),
        average_family=("current_family", "mean"),
        average_stress=("current_stress", "mean"),
    )
    support_trajectory.to_csv(OUTPUTS_DIR / "python_family_support_trajectory.csv", index=False)

    plt.figure(figsize=(8, 5))
    plt.plot(support_trajectory["time"], support_trajectory["average_family_support"], marker="o")
    plt.xlabel("Time")
    plt.ylabel("Average family support index")
    plt.title("Synthetic Family Support Trajectory")
    plt.tight_layout()
    plt.savefig(OUTPUTS_DIR / "python_family_support_trajectory.png", dpi=160)
    plt.close()

    profile_summary = panel.groupby("family_support_profile", as_index=False).agg(
        children=("child_id", "nunique"),
        average_development=("development_score", "mean"),
        average_family_support=("family_support_index", "mean"),
        average_parenting=("current_parenting", "mean"),
        average_family=("current_family", "mean"),
        average_stress=("current_stress", "mean"),
    )
    profile_summary.to_csv(OUTPUTS_DIR / "python_family_support_profiles.csv", index=False)

    print("Wrote Python family systems model outputs.")


if __name__ == "__main__":
    main()
