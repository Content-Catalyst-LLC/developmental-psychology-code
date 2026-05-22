#!/usr/bin/env python3
from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd
import statsmodels.formula.api as smf

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "language_development_panel.csv"
OUT = ROOT / "outputs"
OUT.mkdir(exist_ok=True)

def main() -> None:
    panel = pd.read_csv(DATA).sort_values(["child_id", "time"])
    panel["lag_score"] = panel.groupby("child_id")["language_score"].shift(1)
    model_data = panel.dropna(subset=["lag_score"]).copy()

    model = smf.ols(
        """
        language_score ~ lag_score + time + I(time ** 2) +
        current_interaction + current_reading + current_joint_attention +
        current_turn_taking + hearing_support + multilingual_exposure +
        current_stress + chronic_stress + language_ecology_support +
        book_access + early_education_quality + home_language_recognition +
        multilingual_exposure:home_language_recognition +
        language_support_context
        """,
        data=model_data,
    ).fit(cov_type="HC3")

    profile_model = smf.ols(
        """
        language_score ~ time + I(time ** 2) + chronic_stress +
        current_stress + current_interaction + current_reading +
        language_support_context + C(language_profile)
        """,
        data=panel,
    ).fit(cov_type="HC3")

    with open(OUT / "python_language_model_summary.txt", "w", encoding="utf-8") as f:
        f.write("DYNAMIC LANGUAGE DEVELOPMENT MODEL\n")
        f.write("=" * 80 + "\n")
        f.write(model.summary().as_text())
        f.write("\n\nLANGUAGE PROFILE MODEL\n")
        f.write("=" * 80 + "\n")
        f.write(profile_model.summary().as_text())

    trajectory = panel.groupby(["time", "chronic_stress"], as_index=False).agg(
        average_language=("language_score", "mean"),
        average_interaction=("current_interaction", "mean"),
        average_reading=("current_reading", "mean"),
        average_joint_attention=("current_joint_attention", "mean"),
        average_turn_taking=("current_turn_taking", "mean"),
        average_stress=("current_stress", "mean"),
        average_language_support=("language_support_context", "mean"),
        standard_error=("language_score", lambda x: x.std() / (len(x) ** 0.5)),
    )
    trajectory["stress_group"] = trajectory["chronic_stress"].map({
        0: "Lower chronic stress",
        1: "Higher chronic stress",
    })
    trajectory.to_csv(OUT / "python_stress_language_trajectory.csv", index=False)

    plt.figure(figsize=(8, 5))
    for label, group in trajectory.groupby("stress_group"):
        plt.plot(group["time"], group["average_language"], marker="o", label=label)
    plt.xlabel("Time")
    plt.ylabel("Average language score")
    plt.title("Synthetic Language Development Under Support and Stress")
    plt.legend()
    plt.tight_layout()
    plt.savefig(OUT / "python_stress_language_trajectory.png", dpi=160)
    plt.close()

    context = panel.groupby("time", as_index=False).agg(
        average_interaction=("current_interaction", "mean"),
        average_reading=("current_reading", "mean"),
        average_joint_attention=("current_joint_attention", "mean"),
        average_turn_taking=("current_turn_taking", "mean"),
        average_stress=("current_stress", "mean"),
        average_language_support=("language_support_context", "mean"),
        average_language=("language_score", "mean"),
    )
    context.to_csv(OUT / "python_language_context_trajectory.csv", index=False)

    plt.figure(figsize=(8, 5))
    for col, label in [
        ("average_interaction", "responsive interaction"),
        ("average_reading", "shared reading"),
        ("average_joint_attention", "joint attention"),
        ("average_turn_taking", "turn-taking"),
        ("average_stress", "stress"),
        ("average_language_support", "language support"),
    ]:
        plt.plot(context["time"], context[col], marker="o", label=label)
    plt.xlabel("Time")
    plt.ylabel("Average index")
    plt.title("Synthetic Language Context Across Time")
    plt.legend(fontsize=8)
    plt.tight_layout()
    plt.savefig(OUT / "python_language_context_trajectory.png", dpi=160)
    plt.close()

    panel.groupby("language_profile", as_index=False).agg(
        children=("child_id", "nunique"),
        average_language=("language_score", "mean"),
        average_language_support_context=("language_support_context", "mean"),
        average_interaction=("current_interaction", "mean"),
        average_reading=("current_reading", "mean"),
        average_joint_attention=("current_joint_attention", "mean"),
        average_turn_taking=("current_turn_taking", "mean"),
        average_stress=("current_stress", "mean"),
        chronic_stress_rate=("chronic_stress", "mean"),
        multilingual_exposure_rate=("multilingual_exposure", "mean"),
    ).to_csv(OUT / "python_language_development_profiles.csv", index=False)

    panel.groupby("context_id", as_index=False).agg(
        language_ecology_support=("language_ecology_support", "mean"),
        book_access=("book_access", "mean"),
        early_education_quality=("early_education_quality", "mean"),
        home_language_recognition=("home_language_recognition", "mean"),
        average_language=("language_score", "mean"),
        average_stress=("current_stress", "mean"),
        average_language_support=("language_support_context", "mean"),
    ).to_csv(OUT / "python_language_context_summary.csv", index=False)

    print("Wrote Python language model outputs.")

if __name__ == "__main__":
    main()
