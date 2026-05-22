#!/usr/bin/env python3
from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd
import statsmodels.formula.api as smf

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "regulation_development_panel.csv"
OUT = ROOT / "outputs"
OUT.mkdir(exist_ok=True)

def main() -> None:
    panel = pd.read_csv(DATA).sort_values(["child_id", "time"])
    panel["lag_score"] = panel.groupby("child_id")["regulation_score"].shift(1)
    model_data = panel.dropna(subset=["lag_score"]).copy()

    model = smf.ols(
        """
        regulation_score ~ lag_score + time + current_support + current_structure +
        current_sleep + school_climate + regulation_scaffolding +
        transition_predictability + disability_support_need +
        disability_accommodation + intervention_exposure +
        acute_stress + chronic_stress + temperament_reactivity +
        temperament_reactivity:current_support +
        temperament_reactivity:acute_stress +
        regulatory_support_context
        """,
        data=model_data,
    ).fit(cov_type="HC3")

    profile_model = smf.ols(
        """
        regulation_score ~ time + chronic_stress + acute_stress +
        current_sleep + intervention_exposure + regulatory_support_context +
        C(regulation_profile)
        """,
        data=panel,
    ).fit(cov_type="HC3")

    with open(OUT / "python_regulation_model_summary.txt", "w", encoding="utf-8") as f:
        f.write("DYNAMIC REGULATION MODEL\n")
        f.write("=" * 80 + "\n")
        f.write(model.summary().as_text())
        f.write("\n\nREGULATION PROFILE MODEL\n")
        f.write("=" * 80 + "\n")
        f.write(profile_model.summary().as_text())

    trajectory = panel.groupby(["time", "chronic_stress"], as_index=False).agg(
        average_regulation=("regulation_score", "mean"),
        average_regulatory_context=("regulatory_support_context", "mean"),
        average_support=("current_support", "mean"),
        average_structure=("current_structure", "mean"),
        average_sleep=("current_sleep", "mean"),
        average_stress=("acute_stress", "mean"),
        intervention_rate=("intervention_exposure", "mean"),
        standard_error=("regulation_score", lambda x: x.std() / (len(x) ** 0.5)),
    )
    trajectory["stress_group"] = trajectory["chronic_stress"].map({
        0: "Lower chronic stress",
        1: "Higher chronic stress",
    })
    trajectory.to_csv(OUT / "python_stress_regulation_trajectory.csv", index=False)

    plt.figure(figsize=(8, 5))
    for label, group in trajectory.groupby("stress_group"):
        plt.plot(group["time"], group["average_regulation"], marker="o", label=label)
    plt.xlabel("Time")
    plt.ylabel("Average regulation score")
    plt.title("Synthetic Self-Regulation Across Development")
    plt.legend()
    plt.tight_layout()
    plt.savefig(OUT / "python_stress_regulation_trajectory.png", dpi=160)
    plt.close()

    context = panel.groupby("time", as_index=False).agg(
        average_support=("current_support", "mean"),
        average_structure=("current_structure", "mean"),
        average_sleep=("current_sleep", "mean"),
        average_stress=("acute_stress", "mean"),
        intervention_rate=("intervention_exposure", "mean"),
        average_regulatory_context=("regulatory_support_context", "mean"),
        average_regulation=("regulation_score", "mean"),
    )
    context.to_csv(OUT / "python_regulation_context_trajectory.csv", index=False)

    plt.figure(figsize=(8, 5))
    for col, label in [
        ("average_support", "caregiving support"),
        ("average_structure", "classroom structure"),
        ("average_sleep", "sleep quality"),
        ("average_stress", "acute stress"),
        ("intervention_rate", "intervention rate"),
        ("average_regulatory_context", "regulatory context"),
    ]:
        plt.plot(context["time"], context[col], marker="o", label=label)
    plt.xlabel("Time")
    plt.ylabel("Average index")
    plt.title("Synthetic Regulation Context Across Time")
    plt.legend(fontsize=8)
    plt.tight_layout()
    plt.savefig(OUT / "python_regulation_context_trajectory.png", dpi=160)
    plt.close()

    panel.groupby("regulation_profile", as_index=False).agg(
        children=("child_id", "nunique"),
        average_regulation=("regulation_score", "mean"),
        average_regulatory_support_context=("regulatory_support_context", "mean"),
        average_stress=("acute_stress", "mean"),
        average_sleep=("current_sleep", "mean"),
        intervention_rate=("intervention_exposure", "mean"),
        chronic_stress_rate=("chronic_stress", "mean"),
        disability_support_need_rate=("disability_support_need", "mean"),
    ).to_csv(OUT / "python_regulation_profiles.csv", index=False)

    panel.groupby("school_id", as_index=False).agg(
        school_climate=("school_climate", "mean"),
        regulation_scaffolding=("regulation_scaffolding", "mean"),
        disability_accommodation=("disability_accommodation", "mean"),
        transition_predictability=("transition_predictability", "mean"),
        average_regulation=("regulation_score", "mean"),
        average_stress=("acute_stress", "mean"),
        average_sleep=("current_sleep", "mean"),
        average_regulatory_context=("regulatory_support_context", "mean"),
    ).to_csv(OUT / "python_school_regulation_context_summary.csv", index=False)

    print("Wrote Python regulation model outputs.")

if __name__ == "__main__":
    main()
