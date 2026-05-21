#!/usr/bin/env python3
"""Generate synthetic gender/sexual development and adolescent adjustment panel data.

The data represent a teaching/research scaffold for modeling gender development
and sexual development as distinct but interacting developmental processes
shaped by puberty, family support, social recognition, consent knowledge,
school connectedness, school climate, health education quality, anti-harassment
support, stigma exposure, and protective context.
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
    n_adolescents: int = 900,
    n_periods: int = 10,
    n_schools: int = 38,
    seed: int = 2026,
) -> pd.DataFrame:
    rng = np.random.default_rng(seed)

    adolescents = pd.DataFrame({
        "id": np.arange(1, n_adolescents + 1),
        "school_id": rng.integers(1, n_schools + 1, n_adolescents),
        "baseline_adjustment": rng.normal(50, 8, n_adolescents),
        "family_support": rng.normal(0, 1, n_adolescents),
        "social_recognition": rng.normal(0, 1, n_adolescents),
        "consent_knowledge": rng.normal(0, 1, n_adolescents),
        "school_connectedness": rng.normal(0, 1, n_adolescents),
        "chronic_stigma": rng.binomial(1, 0.24, n_adolescents),
    })

    schools = pd.DataFrame({
        "school_id": np.arange(1, n_schools + 1),
        "school_climate": rng.normal(0, 0.6, n_schools),
        "health_education_quality": rng.normal(0, 0.6, n_schools),
        "anti_harassment_support": rng.normal(0, 0.5, n_schools),
    })

    panel = adolescents.loc[adolescents.index.repeat(n_periods)].copy()
    panel["time"] = np.tile(np.arange(n_periods), n_adolescents)
    panel = panel.merge(schools, on="school_id", how="left")

    panel["pubertal_progress"] = panel["time"] + rng.normal(0, 0.40, len(panel))
    panel["current_family_support"] = rng.normal(panel["family_support"], 0.70)
    panel["current_recognition"] = rng.normal(panel["social_recognition"], 0.70)
    panel["current_consent_knowledge"] = rng.normal(panel["consent_knowledge"], 0.70)
    panel["current_connectedness"] = rng.normal(panel["school_connectedness"], 0.70)
    panel["current_stigma"] = rng.normal(0.40 * panel["chronic_stigma"], 0.70)

    panel["protective_context"] = (
        panel["current_family_support"]
        + panel["current_recognition"]
        + panel["current_consent_knowledge"]
        + panel["current_connectedness"]
        + panel["school_climate"]
        + panel["health_education_quality"]
        + panel["anti_harassment_support"]
    )

    panel = panel.sort_values(["id", "time"]).reset_index(drop=True)
    panel["adjustment_score"] = np.nan

    for _, rows in panel.groupby("id", sort=False):
        previous_score = rows["baseline_adjustment"].iloc[0] + rng.normal(0, 2)

        for idx in rows.index:
            puberty = panel.at[idx, "pubertal_progress"]
            family = panel.at[idx, "current_family_support"]
            recognition = panel.at[idx, "current_recognition"]
            consent = panel.at[idx, "current_consent_knowledge"]
            connectedness = panel.at[idx, "current_connectedness"]
            climate = panel.at[idx, "school_climate"]
            education = panel.at[idx, "health_education_quality"]
            anti_harassment = panel.at[idx, "anti_harassment_support"]
            stigma = panel.at[idx, "current_stigma"]
            chronic = panel.at[idx, "chronic_stigma"]
            protective = panel.at[idx, "protective_context"]

            current_score = (
                0.70 * previous_score
                + 0.75 * puberty
                + 1.15 * family
                + 1.05 * recognition
                + 1.00 * consent
                + 0.95 * connectedness
                + 0.70 * climate
                + 0.70 * education
                + 0.65 * anti_harassment
                - 1.40 * stigma
                - 0.90 * chronic
                - 0.35 * stigma * protective
                + rng.normal(0, 2.5)
            )

            panel.at[idx, "adjustment_score"] = current_score
            previous_score = current_score

    profile = panel.groupby("id", as_index=False).agg(
        average_protective_context=("protective_context", "mean"),
        average_stigma=("current_stigma", "mean"),
        average_adjustment=("adjustment_score", "mean"),
        final_adjustment=("adjustment_score", "last"),
    )

    protective_median = profile["average_protective_context"].median()
    stigma_median = profile["average_stigma"].median()

    profile["development_profile"] = np.select(
        [
            (profile["average_protective_context"] >= protective_median) & (profile["average_stigma"] < stigma_median),
            (profile["average_protective_context"] >= protective_median) & (profile["average_stigma"] >= stigma_median),
            (profile["average_protective_context"] < protective_median) & (profile["average_stigma"] < stigma_median),
        ],
        [
            "higher_protection_lower_stigma",
            "higher_protection_higher_stigma",
            "lower_protection_lower_stigma",
        ],
        default="lower_protection_higher_stigma",
    )

    panel = panel.merge(
        profile[["id", "development_profile"]],
        on="id",
        how="left",
    )

    schools.to_csv(DATA_DIR / "school_context_metadata.csv", index=False)
    profile.to_csv(DATA_DIR / "adolescent_development_profiles.csv", index=False)
    return panel


def main() -> None:
    panel = generate_panel()
    panel_path = DATA_DIR / "gender_sexual_development_panel.csv"
    panel.to_csv(panel_path, index=False)

    trajectory = panel.groupby(["time", "chronic_stigma"], as_index=False).agg(
        average_adjustment=("adjustment_score", "mean"),
        average_protective_context=("protective_context", "mean"),
        average_stigma=("current_stigma", "mean"),
        average_family_support=("current_family_support", "mean"),
        average_recognition=("current_recognition", "mean"),
        average_consent_knowledge=("current_consent_knowledge", "mean"),
        average_connectedness=("current_connectedness", "mean"),
    )
    trajectory.to_csv(OUTPUTS_DIR / "generated_gender_sexual_development_trajectory.csv", index=False)

    print(f"Wrote {panel_path}")
    print(f"Rows: {len(panel):,}")
    print(f"Adolescents: {panel['id'].nunique():,}")
    print(f"Schools: {panel['school_id'].nunique():,}")


if __name__ == "__main__":
    main()
