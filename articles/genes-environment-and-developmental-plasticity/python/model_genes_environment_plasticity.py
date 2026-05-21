#!/usr/bin/env python3
"""Model synthetic gene-environment interaction and developmental plasticity."""

from __future__ import annotations

from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd
import statsmodels.formula.api as smf

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "genes_environment_plasticity_panel.csv"
OUTPUTS_DIR = ROOT / "outputs"
OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)


def main() -> None:
    if not DATA_PATH.exists():
        raise FileNotFoundError("Run python/generate_genes_environment_panel.py first.")

    panel = pd.read_csv(DATA_PATH).sort_values(["child_id", "time"]).reset_index(drop=True)
    panel["lag_score"] = panel.groupby("child_id")["development_score"].shift(1)
    model_data = panel.dropna(subset=["lag_score"]).copy()

    development_model = smf.ols(
        """
        development_score ~ lag_score + time + bio_sensitivity +
        current_care + current_stress + current_nutrition +
        school_support + neighborhood_safety + service_access +
        early_exposure + timing_weight + embedded_stress +
        embedded_support + intervention_support +
        bio_sensitivity:current_care + bio_sensitivity:current_stress
        """,
        data=model_data,
    ).fit(cov_type="HC3")

    embedding_model = smf.ols(
        """
        embedded_stress ~ time + current_stress + current_care +
        current_nutrition + school_support + neighborhood_safety +
        service_access + bio_sensitivity + intervention_support
        """,
        data=panel,
    ).fit(cov_type="HC3")

    with open(OUTPUTS_DIR / "python_plasticity_model_summary.txt", "w", encoding="utf-8") as f:
        f.write("DYNAMIC DEVELOPMENT MODEL\n")
        f.write("=" * 80 + "\n")
        f.write(development_model.summary().as_text())
        f.write("\n\nEMBEDDED STRESS MODEL\n")
        f.write("=" * 80 + "\n")
        f.write(embedding_model.summary().as_text())

    trajectory = panel.groupby(["time", "early_exposure"], as_index=False).agg(
        average_development=("development_score", "mean"),
        standard_error=("development_score", lambda x: x.std() / (len(x) ** 0.5)),
    )
    trajectory["lower"] = trajectory["average_development"] - 1.96 * trajectory["standard_error"]
    trajectory["upper"] = trajectory["average_development"] + 1.96 * trajectory["standard_error"]
    trajectory["group"] = trajectory["early_exposure"].map({0: "No early exposure", 1: "Early exposure"})
    trajectory.to_csv(OUTPUTS_DIR / "python_development_trajectory.csv", index=False)

    plt.figure(figsize=(8, 5))
    for group_name, group in trajectory.groupby("group"):
        plt.plot(group["time"], group["average_development"], marker="o", label=group_name)
    plt.xlabel("Time")
    plt.ylabel("Average development score")
    plt.title("Synthetic Genes, Environment, and Developmental Plasticity")
    plt.legend()
    plt.tight_layout()
    plt.savefig(OUTPUTS_DIR / "python_development_trajectory.png", dpi=160)
    plt.close()

    embedded = panel.groupby("time", as_index=False).agg(
        average_embedded_stress=("embedded_stress", "mean"),
        average_embedded_support=("embedded_support", "mean"),
        average_stress=("current_stress", "mean"),
        average_care=("current_care", "mean"),
    )
    embedded.to_csv(OUTPUTS_DIR / "python_embedded_exposure_trajectory.csv", index=False)

    plt.figure(figsize=(8, 5))
    plt.plot(embedded["time"], embedded["average_embedded_stress"], marker="o", label="embedded stress")
    plt.plot(embedded["time"], embedded["average_embedded_support"], marker="o", label="embedded support")
    plt.xlabel("Time")
    plt.ylabel("Average embedded exposure")
    plt.title("Synthetic Embedded Stress and Support")
    plt.legend()
    plt.tight_layout()
    plt.savefig(OUTPUTS_DIR / "python_embedded_exposure_trajectory.png", dpi=160)
    plt.close()

    profile_summary = panel.groupby("sensitivity_stress_profile", as_index=False).agg(
        children=("child_id", "nunique"),
        average_development=("development_score", "mean"),
        average_embedded_stress=("embedded_stress", "mean"),
        average_embedded_support=("embedded_support", "mean"),
        average_care=("current_care", "mean"),
        average_stress=("current_stress", "mean"),
    )
    profile_summary.to_csv(OUTPUTS_DIR / "python_sensitivity_stress_profiles.csv", index=False)

    print("Wrote Python plasticity model outputs.")


if __name__ == "__main__":
    main()
