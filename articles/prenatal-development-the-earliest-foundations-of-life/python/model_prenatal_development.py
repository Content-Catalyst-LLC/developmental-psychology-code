#!/usr/bin/env python3
"""Model synthetic prenatal development conditions and early outcomes."""

from __future__ import annotations

from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd
import statsmodels.formula.api as smf

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "prenatal_development_foundations_panel.csv"
OUTPUTS_DIR = ROOT / "outputs"
OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)


def main() -> None:
    if not DATA_PATH.exists():
        raise FileNotFoundError("Run python/generate_prenatal_development_panel.py first.")

    prenatal = pd.read_csv(DATA_PATH)

    model = smf.ols(
        """
        early_outcome ~ gestational_weeks + maternal_health + effective_care +
        nutrition_support + social_support + chronic_stress + toxic_exposure +
        environmental_burden + economic_security +
        maternal_health:effective_care +
        maternal_health:chronic_stress +
        developmental_risk:effective_care
        """,
        data=prenatal,
    ).fit(cov_type="HC3")

    neighborhood_model = smf.ols(
        """
        early_outcome ~ gestational_weeks + maternal_health + prenatal_care +
        healthcare_access + nutrition_support + social_support +
        developmental_risk + effective_care + C(prenatal_profile)
        """,
        data=prenatal,
    ).fit(cov_type="HC3")

    with open(OUTPUTS_DIR / "python_prenatal_development_model_summary.txt", "w", encoding="utf-8") as f:
        f.write("PRENATAL DEVELOPMENT EARLY OUTCOME MODEL\n")
        f.write("=" * 80 + "\n")
        f.write(model.summary().as_text())
        f.write("\n\nNEIGHBORHOOD AND PROFILE MODEL\n")
        f.write("=" * 80 + "\n")
        f.write(neighborhood_model.summary().as_text())

    prenatal["stress_group"] = pd.qcut(
        prenatal["chronic_stress"],
        4,
        labels=["Lowest stress", "Moderate-low stress", "Moderate-high stress", "Highest stress"],
    )

    stress_summary = prenatal.groupby("stress_group", as_index=False, observed=True).agg(
        average_outcome=("early_outcome", "mean"),
        average_care=("effective_care", "mean"),
        average_risk=("developmental_risk", "mean"),
        standard_error=("early_outcome", lambda x: x.std() / (len(x) ** 0.5)),
    )
    stress_summary["lower"] = stress_summary["average_outcome"] - 1.96 * stress_summary["standard_error"]
    stress_summary["upper"] = stress_summary["average_outcome"] + 1.96 * stress_summary["standard_error"]
    stress_summary.to_csv(OUTPUTS_DIR / "python_prenatal_stress_summary.csv", index=False)

    plt.figure(figsize=(8, 5))
    x = stress_summary["stress_group"].astype(str)
    plt.plot(x, stress_summary["average_outcome"], marker="o")
    plt.fill_between(x, stress_summary["lower"], stress_summary["upper"], alpha=0.15)
    plt.xlabel("Prenatal stress group")
    plt.ylabel("Average early developmental outcome")
    plt.title("Synthetic Prenatal Stress and Early Developmental Outcome")
    plt.tight_layout()
    plt.savefig(OUTPUTS_DIR / "python_prenatal_stress_summary.png", dpi=160)
    plt.close()

    prenatal["care_group"] = pd.qcut(
        prenatal["effective_care"],
        4,
        labels=["Lowest care", "Moderate-low care", "Moderate-high care", "Highest care"],
    )

    care_summary = prenatal.groupby("care_group", as_index=False, observed=True).agg(
        average_outcome=("early_outcome", "mean"),
        average_risk=("developmental_risk", "mean"),
        average_gestation=("gestational_weeks", "mean"),
        average_maternal_health=("maternal_health", "mean"),
    )
    care_summary.to_csv(OUTPUTS_DIR / "python_effective_care_summary.csv", index=False)

    plt.figure(figsize=(8, 5))
    plt.plot(care_summary["care_group"].astype(str), care_summary["average_outcome"], marker="o")
    plt.xlabel("Effective prenatal care group")
    plt.ylabel("Average early developmental outcome")
    plt.title("Synthetic Effective Prenatal Care and Early Outcome")
    plt.tight_layout()
    plt.savefig(OUTPUTS_DIR / "python_effective_care_summary.png", dpi=160)
    plt.close()

    profile_summary = prenatal.groupby("prenatal_profile", as_index=False).agg(
        cases=("case_id", "count"),
        average_outcome=("early_outcome", "mean"),
        average_effective_care=("effective_care", "mean"),
        average_developmental_risk=("developmental_risk", "mean"),
        average_gestation=("gestational_weeks", "mean"),
        average_maternal_health=("maternal_health", "mean"),
        average_nutrition=("nutrition_support", "mean"),
        average_social_support=("social_support", "mean"),
    )
    profile_summary.to_csv(OUTPUTS_DIR / "python_prenatal_profiles.csv", index=False)

    print("Wrote Python prenatal development model outputs.")


if __name__ == "__main__":
    main()
