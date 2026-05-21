#!/usr/bin/env python3
"""Model synthetic gender development, sexual development, support, and stigma."""

from __future__ import annotations

from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd
import statsmodels.formula.api as smf

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "gender_sexual_development_panel.csv"
OUTPUTS_DIR = ROOT / "outputs"
OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)


def main() -> None:
    if not DATA_PATH.exists():
        raise FileNotFoundError("Run python/generate_gender_sexual_development_panel.py first.")

    panel = pd.read_csv(DATA_PATH).sort_values(["id", "time"]).reset_index(drop=True)
    panel["lag_score"] = panel.groupby("id")["adjustment_score"].shift(1)
    model_data = panel.dropna(subset=["lag_score"]).copy()

    adjustment_model = smf.ols(
        """
        adjustment_score ~ lag_score + pubertal_progress +
        current_family_support + current_recognition +
        current_consent_knowledge + current_connectedness +
        school_climate + health_education_quality +
        anti_harassment_support + current_stigma + chronic_stigma +
        current_stigma:protective_context
        """,
        data=model_data,
    ).fit(cov_type="HC3")

    protective_model = smf.ols(
        """
        adjustment_score ~ pubertal_progress + protective_context +
        current_stigma + chronic_stigma + protective_context:current_stigma +
        C(development_profile)
        """,
        data=panel,
    ).fit(cov_type="HC3")

    with open(OUTPUTS_DIR / "python_gender_sexual_development_model_summary.txt", "w", encoding="utf-8") as f:
        f.write("DYNAMIC GENDER/SEXUAL DEVELOPMENT ADJUSTMENT MODEL\n")
        f.write("=" * 80 + "\n")
        f.write(adjustment_model.summary().as_text())
        f.write("\n\nPROTECTIVE CONTEXT AND STIGMA MODEL\n")
        f.write("=" * 80 + "\n")
        f.write(protective_model.summary().as_text())

    trajectory = panel.groupby(["time", "chronic_stigma"], as_index=False).agg(
        average_adjustment=("adjustment_score", "mean"),
        average_protective_context=("protective_context", "mean"),
        average_stigma=("current_stigma", "mean"),
        standard_error=("adjustment_score", lambda x: x.std() / (len(x) ** 0.5)),
    )
    trajectory["group_label"] = trajectory["chronic_stigma"].map({
        0: "Lower stigma risk",
        1: "Higher stigma risk",
    })
    trajectory["lower"] = trajectory["average_adjustment"] - 1.96 * trajectory["standard_error"]
    trajectory["upper"] = trajectory["average_adjustment"] + 1.96 * trajectory["standard_error"]
    trajectory.to_csv(OUTPUTS_DIR / "python_stigma_trajectory.csv", index=False)

    plt.figure(figsize=(8, 5))
    for group_name, group in trajectory.groupby("group_label"):
        plt.plot(group["time"], group["average_adjustment"], marker="o", label=str(group_name))
    plt.xlabel("Time")
    plt.ylabel("Average adjustment score")
    plt.title("Synthetic Gender Development, Sexual Development, and Adjustment")
    plt.legend()
    plt.tight_layout()
    plt.savefig(OUTPUTS_DIR / "python_stigma_trajectory.png", dpi=160)
    plt.close()

    protective = panel.groupby("time", as_index=False).agg(
        average_family_support=("current_family_support", "mean"),
        average_recognition=("current_recognition", "mean"),
        average_consent_knowledge=("current_consent_knowledge", "mean"),
        average_connectedness=("current_connectedness", "mean"),
        average_stigma=("current_stigma", "mean"),
        average_protective_context=("protective_context", "mean"),
        average_adjustment=("adjustment_score", "mean"),
    )
    protective.to_csv(OUTPUTS_DIR / "python_protective_context_trajectory.csv", index=False)

    plt.figure(figsize=(8, 5))
    plt.plot(protective["time"], protective["average_family_support"], marker="o", label="family support")
    plt.plot(protective["time"], protective["average_recognition"], marker="o", label="recognition")
    plt.plot(protective["time"], protective["average_consent_knowledge"], marker="o", label="consent knowledge")
    plt.plot(protective["time"], protective["average_connectedness"], marker="o", label="connectedness")
    plt.plot(protective["time"], protective["average_stigma"], marker="o", label="stigma")
    plt.xlabel("Time")
    plt.ylabel("Average index")
    plt.title("Synthetic Protective Context and Stigma Over Time")
    plt.legend(fontsize=8)
    plt.tight_layout()
    plt.savefig(OUTPUTS_DIR / "python_protective_context_trajectory.png", dpi=160)
    plt.close()

    profile_summary = panel.groupby("development_profile", as_index=False).agg(
        adolescents=("id", "nunique"),
        average_adjustment=("adjustment_score", "mean"),
        average_protective_context=("protective_context", "mean"),
        average_stigma=("current_stigma", "mean"),
        average_family_support=("current_family_support", "mean"),
        average_recognition=("current_recognition", "mean"),
        average_consent_knowledge=("current_consent_knowledge", "mean"),
        average_connectedness=("current_connectedness", "mean"),
    )
    profile_summary.to_csv(OUTPUTS_DIR / "python_adolescent_development_profiles.csv", index=False)

    print("Wrote Python gender/sexual development model outputs.")


if __name__ == "__main__":
    main()
