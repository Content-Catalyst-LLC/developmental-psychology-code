#!/usr/bin/env python3
"""Generate synthetic prenatal development panel data.

The data represent a teaching/research scaffold for modeling prenatal
development as an ecological process shaped by gestational timing, maternal
health, prenatal care, nutrition support, social support, chronic stress,
toxic exposure, healthcare access, environmental burden, economic security,
effective care, and developmental risk.
"""

from __future__ import annotations

from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
OUTPUTS_DIR = ROOT / "outputs"
DATA_DIR.mkdir(parents=True, exist_ok=True)
OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)


def generate_panel(
    n_cases: int = 1500,
    n_neighborhoods: int = 55,
    seed: int = 2026,
) -> pd.DataFrame:
    rng = np.random.default_rng(seed)

    prenatal = pd.DataFrame({
        "case_id": np.arange(1, n_cases + 1),
        "neighborhood_context": rng.integers(1, n_neighborhoods + 1, n_cases),
        "gestational_weeks": np.round(rng.normal(39, 1.8, n_cases), 1),
        "maternal_health": rng.normal(0, 1, n_cases),
        "prenatal_care": rng.normal(0, 1, n_cases),
        "chronic_stress": rng.normal(0, 1, n_cases),
        "toxic_exposure": rng.normal(0, 1, n_cases),
        "nutrition_support": rng.normal(0, 1, n_cases),
        "social_support": rng.normal(0, 1, n_cases),
    })

    neighborhoods = pd.DataFrame({
        "neighborhood_context": np.arange(1, n_neighborhoods + 1),
        "healthcare_access": rng.normal(0, 0.6, n_neighborhoods),
        "environmental_burden": rng.normal(0, 0.6, n_neighborhoods),
        "economic_security": rng.normal(0, 0.5, n_neighborhoods),
    })

    prenatal = prenatal.merge(neighborhoods, on="neighborhood_context", how="left")

    prenatal["effective_care"] = (
        prenatal["prenatal_care"]
        + prenatal["healthcare_access"]
        + 0.30 * prenatal["social_support"]
    )

    prenatal["developmental_risk"] = (
        prenatal["chronic_stress"]
        + prenatal["toxic_exposure"]
        + prenatal["environmental_burden"]
        - 0.40 * prenatal["economic_security"]
    )

    prenatal["early_outcome"] = (
        10
        + 0.85 * prenatal["gestational_weeks"]
        + 1.60 * prenatal["maternal_health"]
        + 1.35 * prenatal["effective_care"]
        + 1.10 * prenatal["nutrition_support"]
        + 0.85 * prenatal["social_support"]
        - 1.55 * prenatal["chronic_stress"]
        - 1.45 * prenatal["toxic_exposure"]
        - 1.10 * prenatal["environmental_burden"]
        + 0.70 * prenatal["maternal_health"] * prenatal["effective_care"]
        - 0.60 * prenatal["maternal_health"] * prenatal["chronic_stress"]
        - 0.55 * prenatal["developmental_risk"] * prenatal["effective_care"]
        + rng.normal(0, 2.6, n_cases)
    )

    case_summary = prenatal[[
        "case_id",
        "effective_care",
        "developmental_risk",
        "early_outcome",
        "gestational_weeks",
    ]].copy()

    care_median = case_summary["effective_care"].median()
    risk_median = case_summary["developmental_risk"].median()

    case_summary["prenatal_profile"] = np.select(
        [
            (case_summary["effective_care"] >= care_median) & (case_summary["developmental_risk"] < risk_median),
            (case_summary["effective_care"] >= care_median) & (case_summary["developmental_risk"] >= risk_median),
            (case_summary["effective_care"] < care_median) & (case_summary["developmental_risk"] < risk_median),
        ],
        [
            "higher_care_lower_risk",
            "higher_care_higher_risk",
            "lower_care_lower_risk",
        ],
        default="lower_care_higher_risk",
    )

    prenatal = prenatal.merge(
        case_summary[["case_id", "prenatal_profile"]],
        on="case_id",
        how="left",
    )

    neighborhoods.to_csv(DATA_DIR / "neighborhood_context_metadata.csv", index=False)
    case_summary.to_csv(DATA_DIR / "prenatal_case_profiles.csv", index=False)
    return prenatal


def main() -> None:
    prenatal = generate_panel()
    panel_path = DATA_DIR / "prenatal_development_foundations_panel.csv"
    prenatal.to_csv(panel_path, index=False)

    neighborhood_summary = prenatal.groupby("neighborhood_context", as_index=False).agg(
        cases=("case_id", "count"),
        average_outcome=("early_outcome", "mean"),
        average_effective_care=("effective_care", "mean"),
        average_developmental_risk=("developmental_risk", "mean"),
        average_healthcare_access=("healthcare_access", "mean"),
        average_environmental_burden=("environmental_burden", "mean"),
        average_economic_security=("economic_security", "mean"),
    )
    neighborhood_summary.to_csv(OUTPUTS_DIR / "generated_prenatal_neighborhood_summary.csv", index=False)

    print(f"Wrote {panel_path}")
    print(f"Rows: {len(prenatal):,}")
    print(f"Neighborhood contexts: {prenatal['neighborhood_context'].nunique():,}")


if __name__ == "__main__":
    main()
