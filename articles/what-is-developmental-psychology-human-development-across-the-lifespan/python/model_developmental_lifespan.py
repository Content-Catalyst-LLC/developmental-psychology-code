#!/usr/bin/env python3
"""Model synthetic developmental lifespan trajectories."""

from __future__ import annotations

from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd
import statsmodels.formula.api as smf

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "developmental_lifespan_panel.csv"
OUT = ROOT / "outputs"
OUT.mkdir(exist_ok=True)


def main() -> None:
    panel = pd.read_csv(DATA).sort_values(["child_id", "time"])
    panel["lag_score"] = panel.groupby("child_id")["development_score"].shift(1)
    model_data = panel.dropna(subset=["lag_score"]).copy()

    model = smf.ols(
        """
        development_score ~ lag_score + time + caregiver_support + family_support +
        school_support + school_climate + disability_support_need +
        disability_accommodation + counseling_access + language_access +
        community_resource_index + structural_risk + acute_stress +
        current_support + intervention + protective_context
        """,
        data=model_data,
    ).fit(cov_type="HC3")

    profile_model = smf.ols(
        """
        development_score ~ time + structural_risk + disability_support_need +
        acute_stress + current_support + protective_context + C(development_profile)
        """,
        data=panel,
    ).fit(cov_type="HC3")

    with open(OUT / "python_developmental_lifespan_model_summary.txt", "w", encoding="utf-8") as f:
        f.write("DYNAMIC DEVELOPMENTAL LIFESPAN MODEL\n")
        f.write("=" * 80 + "\n")
        f.write(model.summary().as_text())
        f.write("\n\nDEVELOPMENT PROFILE MODEL\n")
        f.write("=" * 80 + "\n")
        f.write(profile_model.summary().as_text())

    trajectory = panel.groupby(["time", "structural_risk"], as_index=False).agg(
        average_development=("development_score", "mean"),
        average_support=("current_support", "mean"),
        average_stress=("acute_stress", "mean"),
        average_protective_context=("protective_context", "mean"),
        standard_error=("development_score", lambda x: x.std() / (len(x) ** 0.5)),
    )
    trajectory["risk_group"] = trajectory["structural_risk"].map({
        0: "Lower structural risk",
        1: "Higher structural risk",
    })
    trajectory.to_csv(OUT / "python_structural_risk_trajectory.csv", index=False)

    plt.figure(figsize=(8, 5))
    for label, group in trajectory.groupby("risk_group"):
        plt.plot(group["time"], group["average_development"], marker="o", label=label)
    plt.xlabel("Time")
    plt.ylabel("Average development score")
    plt.title("Synthetic Developmental Trajectories by Structural Risk")
    plt.legend()
    plt.tight_layout()
    plt.savefig(OUT / "python_structural_risk_trajectory.png", dpi=160)
    plt.close()

    support = panel.groupby("time", as_index=False).agg(
        average_support=("current_support", "mean"),
        average_stress=("acute_stress", "mean"),
        average_intervention=("intervention", "mean"),
        average_protective_context=("protective_context", "mean"),
        average_development=("development_score", "mean"),
    )
    support.to_csv(OUT / "python_support_context_trajectory.csv", index=False)

    plt.figure(figsize=(8, 5))
    for col, label in [
        ("average_support", "support"),
        ("average_stress", "stress"),
        ("average_intervention", "intervention"),
        ("average_protective_context", "protective context"),
    ]:
        plt.plot(support["time"], support[col], marker="o", label=label)
    plt.xlabel("Time")
    plt.ylabel("Average index")
    plt.title("Synthetic Developmental Context Across Time")
    plt.legend(fontsize=8)
    plt.tight_layout()
    plt.savefig(OUT / "python_support_context_trajectory.png", dpi=160)
    plt.close()

    profile_summary = panel.groupby("development_profile", as_index=False).agg(
        children=("child_id", "nunique"),
        average_development=("development_score", "mean"),
        average_protective_context=("protective_context", "mean"),
        average_support=("current_support", "mean"),
        average_stress=("acute_stress", "mean"),
        structural_risk_rate=("structural_risk", "mean"),
        disability_support_need_rate=("disability_support_need", "mean"),
    )
    profile_summary.to_csv(OUT / "python_developmental_profiles.csv", index=False)

    school_summary = panel.groupby("school_id", as_index=False).agg(
        school_climate=("school_climate", "mean"),
        disability_accommodation=("disability_accommodation", "mean"),
        counseling_access=("counseling_access", "mean"),
        language_access=("language_access", "mean"),
        community_resource_index=("community_resource_index", "mean"),
        average_development=("development_score", "mean"),
        average_support=("current_support", "mean"),
        average_stress=("acute_stress", "mean"),
        average_protective_context=("protective_context", "mean"),
    )
    school_summary.to_csv(OUT / "python_school_context_summary.csv", index=False)

    print("Wrote Python developmental lifespan model outputs.")


if __name__ == "__main__":
    main()
