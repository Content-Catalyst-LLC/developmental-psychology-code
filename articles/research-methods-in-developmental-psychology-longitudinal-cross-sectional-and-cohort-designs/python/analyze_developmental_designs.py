#!/usr/bin/env python3
"""Analyze synthetic developmental research designs.

This script compares cross-sectional, longitudinal, and cohort-aware models
using synthetic data.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import statsmodels.formula.api as smf


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
OUTPUTS_DIR = ROOT / "outputs"
OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)

PANEL_PATH = DATA_DIR / "developmental_design_panel.csv"
CROSS_SECTIONAL_PATH = DATA_DIR / "cross_sectional_sample.csv"


def main() -> None:
    if not PANEL_PATH.exists():
        raise FileNotFoundError(
            f"Missing {PANEL_PATH}. Run python/generate_developmental_designs.py first."
        )

    panel = pd.read_csv(PANEL_PATH)
    observed_panel = panel.loc[panel["observed"] == 1].copy()

    if CROSS_SECTIONAL_PATH.exists():
        cross_section = pd.read_csv(CROSS_SECTIONAL_PATH)
    else:
        cross_section = panel.loc[panel["period"] == panel["period"].min()].copy()

    cross_section = cross_section.loc[cross_section["observed"] == 1].copy()

    cross_sectional_model = smf.ols(
        """
        development_score ~ age + I(age ** 2) + support + risk + context_quality
        """,
        data=cross_section,
    ).fit(cov_type="HC3")

    longitudinal_model = smf.ols(
        """
        development_score ~ age + I(age ** 2) + support + risk +
        baseline_trait + context_quality
        """,
        data=observed_panel,
    ).fit(cov_type="HC3")

    cohort_aware_model = smf.ols(
        """
        development_score ~ age + I(age ** 2) + C(birth_cohort) +
        C(period) + support + risk + baseline_trait + context_quality
        """,
        data=observed_panel,
    ).fit(cov_type="HC3")

    with open(OUTPUTS_DIR / "python_design_model_summary.txt", "w", encoding="utf-8") as f:
        f.write("CROSS-SECTIONAL MODEL\n")
        f.write("=" * 80 + "\n")
        f.write(cross_sectional_model.summary().as_text())
        f.write("\n\nLONGITUDINAL MODEL\n")
        f.write("=" * 80 + "\n")
        f.write(longitudinal_model.summary().as_text())
        f.write("\n\nCOHORT-AWARE MODEL\n")
        f.write("=" * 80 + "\n")
        f.write(cohort_aware_model.summary().as_text())

    trajectory = observed_panel.groupby(["birth_cohort", "age"], as_index=False).agg(
        mean_development_score=("development_score", "mean"),
        observation_rate=("observed", "mean"),
        people=("person_id", "nunique"),
    )
    trajectory.to_csv(OUTPUTS_DIR / "python_growth_trajectory.csv", index=False)

    missingness = panel.groupby("study_wave", as_index=False).agg(
        observation_rate=("observed", "mean"),
        observations=("observed", "sum"),
        possible_observations=("observed", "count"),
    )
    missingness.to_csv(OUTPUTS_DIR / "python_missingness_by_wave.csv", index=False)

    plt.figure(figsize=(9, 5.5))
    for cohort, group in trajectory.groupby("birth_cohort"):
        plt.plot(
            group["age"],
            group["mean_development_score"],
            marker="o",
            label=f"Cohort {cohort}",
        )
    plt.xlabel("Age")
    plt.ylabel("Average development score")
    plt.title("Synthetic Cohort-Sequential Developmental Trajectories")
    plt.legend()
    plt.tight_layout()
    plt.savefig(OUTPUTS_DIR / "python_design_comparison.png", dpi=160)
    plt.close()

    plt.figure(figsize=(8, 5))
    plt.plot(missingness["study_wave"], missingness["observation_rate"], marker="o")
    plt.xlabel("Study wave")
    plt.ylabel("Observation rate")
    plt.title("Synthetic Attrition / Observation Rate by Wave")
    plt.tight_layout()
    plt.savefig(OUTPUTS_DIR / "python_missingness_by_wave.png", dpi=160)
    plt.close()

    print("Wrote outputs/python_design_model_summary.txt")
    print("Wrote outputs/python_growth_trajectory.csv")
    print("Wrote outputs/python_design_comparison.png")
    print("Wrote outputs/python_missingness_by_wave.csv")
    print("Wrote outputs/python_missingness_by_wave.png")


if __name__ == "__main__":
    main()
