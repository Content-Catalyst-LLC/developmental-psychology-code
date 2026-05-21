#!/usr/bin/env python3
"""Model synthetic adult development and the psychology of life stages."""

from __future__ import annotations

from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd
import statsmodels.formula.api as smf

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "adult_development_life_stages_panel.csv"
OUTPUTS_DIR = ROOT / "outputs"
OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)


def main() -> None:
    if not DATA_PATH.exists():
        raise FileNotFoundError("Run python/generate_adult_development_panel.py first.")

    panel = pd.read_csv(DATA_PATH).sort_values(["id", "time"]).reset_index(drop=True)
    panel["lag_score"] = panel.groupby("id")["adjustment_score"].shift(1)
    model_data = panel.dropna(subset=["lag_score"]).copy()

    adjustment_model = smf.ols(
        """
        adjustment_score ~ lag_score + time + current_relational_support +
        current_work_integration + current_health_burden +
        current_adaptive_resources + current_role_burden +
        institutional_support + community_stability +
        young_stage + midlife_stage + later_stage +
        current_relational_support:current_adaptive_resources
        """,
        data=model_data,
    ).fit(cov_type="HC3")

    burden_model = smf.ols(
        """
        adjustment_score ~ time + current_role_burden + current_health_burden +
        current_relational_support + current_adaptive_resources +
        current_work_integration + institutional_support +
        C(life_stage)
        """,
        data=panel,
    ).fit(cov_type="HC3")

    with open(OUTPUTS_DIR / "python_adult_development_model_summary.txt", "w", encoding="utf-8") as f:
        f.write("DYNAMIC ADULT DEVELOPMENT MODEL\n")
        f.write("=" * 80 + "\n")
        f.write(adjustment_model.summary().as_text())
        f.write("\n\nROLE BURDEN AND HEALTH BURDEN MODEL\n")
        f.write("=" * 80 + "\n")
        f.write(burden_model.summary().as_text())

    trajectory = panel.groupby(["time", "life_stage"], as_index=False).agg(
        average_adjustment=("adjustment_score", "mean"),
        standard_error=("adjustment_score", lambda x: x.std() / (len(x) ** 0.5)),
    )
    trajectory["lower"] = trajectory["average_adjustment"] - 1.96 * trajectory["standard_error"]
    trajectory["upper"] = trajectory["average_adjustment"] + 1.96 * trajectory["standard_error"]
    trajectory.to_csv(OUTPUTS_DIR / "python_adult_stage_trajectory.csv", index=False)

    plt.figure(figsize=(8, 5))
    for group_name, group in trajectory.groupby("life_stage"):
        plt.plot(group["time"], group["average_adjustment"], marker="o", label=str(group_name))
    plt.xlabel("Time")
    plt.ylabel("Average adjustment score")
    plt.title("Synthetic Adult Development Across Life Stages")
    plt.legend()
    plt.tight_layout()
    plt.savefig(OUTPUTS_DIR / "python_adult_stage_trajectory.png", dpi=160)
    plt.close()

    support_burden = panel.groupby("time", as_index=False).agg(
        average_support=("current_relational_support", "mean"),
        average_work=("current_work_integration", "mean"),
        average_health=("current_health_burden", "mean"),
        average_resources=("current_adaptive_resources", "mean"),
        average_role_burden=("current_role_burden", "mean"),
    )
    support_burden.to_csv(OUTPUTS_DIR / "python_adult_support_burden_trajectory.csv", index=False)

    plt.figure(figsize=(8, 5))
    plt.plot(support_burden["time"], support_burden["average_support"], marker="o", label="relational support")
    plt.plot(support_burden["time"], support_burden["average_work"], marker="o", label="work integration")
    plt.plot(support_burden["time"], support_burden["average_health"], marker="o", label="health burden")
    plt.plot(support_burden["time"], support_burden["average_role_burden"], marker="o", label="role burden")
    plt.xlabel("Time")
    plt.ylabel("Average index")
    plt.title("Synthetic Adult Support, Work, Health, and Role Burden")
    plt.legend()
    plt.tight_layout()
    plt.savefig(OUTPUTS_DIR / "python_adult_support_burden_trajectory.png", dpi=160)
    plt.close()

    profile_summary = panel.groupby("adult_development_profile", as_index=False).agg(
        adults=("id", "nunique"),
        average_adjustment=("adjustment_score", "mean"),
        average_support=("current_relational_support", "mean"),
        average_work=("current_work_integration", "mean"),
        average_health=("current_health_burden", "mean"),
        average_resources=("current_adaptive_resources", "mean"),
        average_role_burden=("current_role_burden", "mean"),
    )
    profile_summary.to_csv(OUTPUTS_DIR / "python_adult_development_profiles.csv", index=False)

    print("Wrote Python adult development model outputs.")


if __name__ == "__main__":
    main()
