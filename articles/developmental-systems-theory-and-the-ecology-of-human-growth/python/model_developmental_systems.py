#!/usr/bin/env python3
"""Model synthetic developmental systems theory and ecological development."""

from __future__ import annotations

from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd
import statsmodels.formula.api as smf

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "developmental_systems_panel.csv"
OUTPUTS_DIR = ROOT / "outputs"
OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)


def main() -> None:
    if not DATA_PATH.exists():
        raise FileNotFoundError("Run python/generate_developmental_systems_panel.py first.")

    panel = pd.read_csv(DATA_PATH).sort_values(["child_id", "time"]).reset_index(drop=True)
    panel["lag_score"] = panel.groupby("child_id")["development_score"].shift(1)
    model_data = panel.dropna(subset=["lag_score"]).copy()

    development_model = smf.ols(
        """
        development_score ~ lag_score + time + biological_sensitivity +
        current_family + current_peer + school_climate +
        curriculum_opportunity + neighborhood_safety + service_access +
        material_security + intervention_exposure + ecological_stress +
        biological_sensitivity:current_family +
        biological_sensitivity:ecological_stress
        """,
        data=model_data,
    ).fit(cov_type="HC3")

    stress_model = smf.ols(
        """
        ecological_stress ~ time + current_family + current_peer +
        school_climate + curriculum_opportunity + neighborhood_safety +
        service_access + material_security + intervention_exposure
        """,
        data=panel,
    ).fit(cov_type="HC3")

    with open(OUTPUTS_DIR / "python_developmental_systems_model_summary.txt", "w", encoding="utf-8") as f:
        f.write("DYNAMIC DEVELOPMENT MODEL\n")
        f.write("=" * 80 + "\n")
        f.write(development_model.summary().as_text())
        f.write("\n\nECOLOGICAL STRESS MODEL\n")
        f.write("=" * 80 + "\n")
        f.write(stress_model.summary().as_text())

    trajectory = panel.groupby(["time", "intervention_exposure"], as_index=False).agg(
        average_development=("development_score", "mean"),
        average_ecological_support=("ecological_support", "mean"),
        average_ecological_stress=("ecological_stress", "mean"),
        standard_error=("development_score", lambda x: x.std() / (len(x) ** 0.5)),
    )
    trajectory["lower"] = trajectory["average_development"] - 1.96 * trajectory["standard_error"]
    trajectory["upper"] = trajectory["average_development"] + 1.96 * trajectory["standard_error"]
    trajectory["group"] = trajectory["intervention_exposure"].map({0: "No intervention", 1: "Intervention"})
    trajectory.to_csv(OUTPUTS_DIR / "python_development_trajectory.csv", index=False)

    plt.figure(figsize=(8, 5))
    for group_name, group in trajectory.groupby("group"):
        plt.plot(group["time"], group["average_development"], marker="o", label=group_name)
    plt.xlabel("Time")
    plt.ylabel("Average development score")
    plt.title("Synthetic Developmental Systems Trajectories")
    plt.legend()
    plt.tight_layout()
    plt.savefig(OUTPUTS_DIR / "python_development_trajectory.png", dpi=160)
    plt.close()

    support_trajectory = panel.groupby("time", as_index=False).agg(
        average_ecological_support=("ecological_support", "mean"),
        average_ecological_stress=("ecological_stress", "mean"),
        average_family=("current_family", "mean"),
        average_peer=("current_peer", "mean"),
    )
    support_trajectory.to_csv(OUTPUTS_DIR / "python_ecological_support_trajectory.csv", index=False)

    plt.figure(figsize=(8, 5))
    plt.plot(support_trajectory["time"], support_trajectory["average_ecological_support"], marker="o", label="ecological support")
    plt.plot(support_trajectory["time"], support_trajectory["average_ecological_stress"], marker="o", label="ecological stress")
    plt.xlabel("Time")
    plt.ylabel("Average ecological index")
    plt.title("Synthetic Ecological Support and Stress")
    plt.legend()
    plt.tight_layout()
    plt.savefig(OUTPUTS_DIR / "python_ecological_support_trajectory.png", dpi=160)
    plt.close()

    profile_summary = panel.groupby("ecological_support_profile", as_index=False).agg(
        children=("child_id", "nunique"),
        average_development=("development_score", "mean"),
        average_ecological_support=("ecological_support", "mean"),
        average_ecological_stress=("ecological_stress", "mean"),
        average_family=("current_family", "mean"),
        average_peer=("current_peer", "mean"),
    )
    profile_summary.to_csv(OUTPUTS_DIR / "python_ecological_support_profiles.csv", index=False)

    print("Wrote Python developmental systems model outputs.")


if __name__ == "__main__":
    main()
